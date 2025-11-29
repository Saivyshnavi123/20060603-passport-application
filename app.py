import os

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import yaml
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


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

def get_user(user_id):
    return User.query.get(user_id)


def generate_sequential_passport_number():
    last = PassportApplication.query.order_by(PassportApplication.id.desc()).first()
    if last and last.passport_number:
        try:
            num = int(last.passport_number[1:]) + 1
        except:
            num = last.id + 1
    else:
        num = 1
    return f"P{num:06d}"


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

@app.route('/login', methods=['POST'])
def login():
    # Try to parse JSON safely
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    # Validate required fields
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Check if user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    # Validate password
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Success
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }), 200


@app.route('/slots', methods=['GET'])
def check_slots():
    try:
        date_str = request.args.get('date')

        if not date_str:
            return jsonify({"error": "date parameter is required"}), 400

        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        count = PassportApplication.query.filter_by(appointment_date=appointment_date).count()

        remaining = max(0, 10 - count)

        return jsonify({
            "date": date_str,
            ""
            "": count,
            "remaining_slots": remaining
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Unexpected server error",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)