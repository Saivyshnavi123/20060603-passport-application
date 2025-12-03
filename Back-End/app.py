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

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'postgresql://saichowdhary:7GRUZ6qj7YYjbBmK1Zx3bDNOBYXbHHMR@dpg-d4evgt0gjchc73fpscb0-a.oregon-postgres.render.com/passport_xhof')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {'title': 'Passport Management API', 'uiversion': 3, 'specs_route': '/swagger'}
CORS(app, resources={r"/*": {"origins": "*"}})

# Load Swagger documentation template
with open("swagger.yaml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / user
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
    passport_number = db.Column(db.String(20), unique=True, nullable=True)  # AUTO-GENERATED SEQUENTIAL
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected, completed
    user = db.relationship('User', backref='applications')


# --- DROP & SEED SETTINGS ---
DROP_AND_SEED = True  # set to False in production


def seed_data():
    admin = User(username="admin",
                 password=generate_password_hash("admin123", method="pbkdf2:sha256"),
                 role="admin",
                 email="admin@example.com")

    user = User(username="john",
                password=generate_password_hash("john123", method="pbkdf2:sha256"),
                role="user",
                email="john@example.com")

    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

    print("Seed data inserted")


# ------------------- Helpers -------------------
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


# ------------------- Auth -------------------
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


# ------------------- SLOT CHECK -------------------
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

        date_string = appointment_date.strftime("%Y-%m-%d")

        count = PassportApplication.query.filter_by(
            appointment_date=date_string
        ).count()

        # 5️⃣ Remaining slots
        remaining = max(0, 10 - count)

        return jsonify({
            "date": date_string,
            "booked_count": count,
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
# ------------------- APPLY PASSPORT -------------------

@app.route('/passport/apply', methods=['POST'])
def apply_passport():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        # Validate user_id
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        user = get_user(user_id)
        if not user or user.role != "user":
            return jsonify({"error": "Only users can apply"}), 403

        # Validate required fields
        required = ["full_name", "dob", "nationality", "appointment_date"]
        missing = [f for f in required if not data.get(f)]

        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        # Validate appointment date format
        date_str = data["appointment_date"]
        try:
            datetime.strptime(date_str, "%Y-%m-%d")  # validation only
        except ValueError:
            return jsonify({"error": "Invalid appointment_date format. Use YYYY-MM-DD"}), 400

        # Slot check (string-based query because DB column is string)
        count = PassportApplication.query.filter_by(appointment_date=date_str).count()
        if count >= 10:
            return jsonify({"error": "No slots available for this date"}), 400

        # Auto-generate new passport number
        passport_num = generate_sequential_passport_number()

        # Create application record
        app_rec = PassportApplication(
            user_id=user.id,
            full_name=data["full_name"],
            dob=data["dob"],
            nationality=data["nationality"],
            gender=data.get("gender"),
            place_of_birth=data.get("place_of_birth"),
            appointment_date=date_str,  # stored as string
            passport_number=passport_num
        )

        db.session.add(app_rec)
        db.session.commit()

        return jsonify({
            "message": "Application submitted",
            "passport_number": passport_num
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


@app.route('/user/applications', methods=['GET'])
def user_applications():
    try:
        # Get user_id from query params
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        # Ensure user_id is an integer
        if not str(user_id).isdigit():
            return jsonify({"error": "user_id must be an integer"}), 400

        user = get_user(int(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Only normal users can use this API
        if user.role != "user":
            return jsonify({"error": "Only normal users can view their applications"}), 403

        # Get user's applications
        apps = PassportApplication.query.filter_by(user_id=user.id)\
                                        .order_by(PassportApplication.id.asc())\
                                        .all()

        result = []
        for a in apps:
            result.append({
                "id": a.id,
                "full_name": a.full_name,
                "passport_number": a.passport_number,
                "appointment_date": a.appointment_date,
                "status": a.status,
                "nationality": a.nationality,
                "gender": a.gender,
                "place_of_birth": a.place_of_birth,
                "dob": a.dob
            })

        return jsonify({"applications": result}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

# ------------------- ADMIN ROUTES -------------------
@app.route('/admin/applications', methods=['GET'])
def view_all_applications():
    try:
        # Validate user_id param
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        # Validate user_id is numeric
        if not str(user_id).isdigit():
            return jsonify({"error": "user_id must be an integer"}), 400

        admin = get_user(int(user_id))

        # Ensure admin exists and has role 'admin'
        if not admin or admin.role != 'admin':
            return jsonify({"error": "Only admin can view applications"}), 403

        # Fetch all passport applications
        apps = PassportApplication.query.order_by(PassportApplication.id.asc()).all()

        result = []
        for a in apps:
            result.append({
                "id": a.id,
                "full_name": a.full_name,
                "passport_number": a.passport_number,
                "appointment_date": a.appointment_date,
                "status": a.status,
                "nationality": a.nationality,
                "gender": a.gender,
                "place_of_birth": a.place_of_birth,
                "dob": a.dob,
                "user_id": a.user_id
            })

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


@app.route('/admin/application/<int:app_id>/status', methods=['PATCH'])
def update_status(app_id):
    data = request.json
    admin = get_user(data.get('user_id'))

    if not admin or admin.role != 'admin':
        return jsonify({"message": "Only admin can update status"}), 403

    app_rec = PassportApplication.query.get(app_id)
    if not app_rec:
        return jsonify({"message": "Application not found"}), 404

    new_status = data.get('status')
    if new_status not in ["pending", "approved", "rejected", "completed"]:
        return jsonify({"message": "Invalid status"}), 400

    app_rec.status = new_status
    db.session.commit()

    return jsonify({"message": "Status updated"}), 200


if __name__ == '__main__':
    with app.app_context():
        if DROP_AND_SEED:
            print("Dropping all tables...")
            db.drop_all()
            print("Creating tables...")
            db.create_all()
            print("Seeding initial data...")
            seed_data()
    app.run(debug=True)