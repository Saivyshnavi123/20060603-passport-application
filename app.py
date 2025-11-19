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


# -------------------------------------
# MODELS
# -------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin/user
    email = db.Column(db.String(200), nullable=False)


class PassportApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
