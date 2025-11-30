
# Flask Booking API

This is a Python Flask-based REST API that supports user registration, authentication, and booking slot retrieval. It uses JWT authentication, a PostgreSQL database, SQLAlchemy ORM, and includes built-in Swagger documentation.

---

##  Project Structure

```
project
│── app.py
│── requirements.txt
│── README.md
```
---

## Features

- User registration with secure hashed passwords  
- JWT-based authentication  
- Retrieve available booking slots  
- Database persistence using **Flask-SQLAlchemy**
- Database migrations using **Flask-Migrate**
- Swagger auto-generated API documentation
- CORS enabled for external clients

---

## Requirements

See `requirements.txt`:

```
sqlalchemy
flask~=3.1.1
gunicorn
Flask-SQLAlchemy
Flask-Migrate
Flask-JWT-Extended
psycopg2-binary
flasgger~=0.9.7.1
pyyaml~=6.0.2
werkzeug~=3.1.3
flask-cors
```
---

## Environment Variables

Before running, create a `.env` file or configure environment variables:

| Variable | Description | Example |
|---------|-------------|---------|
| `SECRET_KEY` | App session key | `supersecretkey123` |
| `JWT_SECRET_KEY` | JWT signing key | `jwtsecretkey` |
| `DATABASE_URL` | DB connection string | `postgresql://user:pass@localhost/dbname` |

---

##  Running the Application

###  Install dependencies:

```sh
pip install -r requirements.txt
```


###  Initialize database:

```sh
flask db init
flask db migrate
flask db upgrade
```

###  Start the server:

```sh
python app.py
```

The API will run at:

```
http://localhost:5000
```

---

## API Documentation (Swagger)

Once the server is running, open:

```
http://localhost:5000/apidocs
```

---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|-----------|-------------|
| `POST` | `/register` |  No | Create a new user |
| `POST` | `/login` |  No | Authenticate user & receive JWT token |
| `GET` | `/slots` | Yes | Retrieve available slots |

---

### Example Request: Register

```json
POST /register
{
  "username": "test",
  "password": "mypassword"
}
```

---

### Example Request: Login

```json
POST /login
{
  "username": "test",
  "password": "mypassword"
}
```

Response:

```json
{
  "access_token": "your.jwt.token"
}
```

---

### Example Request: Get Slots

Headers:

```
Authorization: Bearer <access_token>
```

---

## Production Deployment

A production-ready WSGI server is included via **Gunicorn**:

```sh
gunicorn app:app --bind 0.0.0.0:5000
```

---

## Testing

You can test endpoints using:

- Postman
- Curl
- Swagger UI

---

## Error Handling

The API returns structured JSON error responses for:

- Validation errors
- Unauthorized access
- Database failures
- Unexpected server errors

---

