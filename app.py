import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import yaml
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------
# CONFIG
# -------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://saichowdhary:7GRUZ6qj7YYjbBmK1Zx3bDNOBYXbHHMR@dpg-d4evgt0gjchc73fpscb0-a.oregon-postgres.render.com/passport_xhof'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {'title': 'Passport Management API', 'uiversion': 3}
CORS(app, resources={r"/*": {"origins": "*"}})

# Load Swagger
with open("swagger.yaml", "r") as f:
    swagger_template = yaml.safe_load(f)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app, template=swagger_template)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), nullable=False)


class PassportApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    place_of_birth = db.Column(db.String(150))
    appointment_date = db.Column(db.String(20), nullable=False)
    passport_number = db.Column(db.String(20), unique=True, nullable=True)
    status = db.Column(db.String(20), default="pending")
    user = db.relationship('User', backref='applications')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    required = ['username', 'password', 'role', 'email']
    if not all(field in data and data[field] for field in required):
        return jsonify({"message": "All fields are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 409

    hashed = generate_password_hash(
        data['password'],
        method='pbkdf2:sha256'
    )

    user = User(
        username=data['username'],
        password=hashed,
        role=data['role'],
        email=data['email']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
