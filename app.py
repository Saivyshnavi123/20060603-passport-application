import os

import yaml
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://saichowdhary:7GRUZ6qj7YYjbBmK1Zx3bDNOBYXbHHMR@dpg-d4evgt0gjchc73fpscb0-a.oregon-postgres.render.com/passport_xhof')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {'title': 'Passport Management API', 'uiversion': 3}
CORS(app, resources={r"/*": {"origins": "*"}})

# Load Swagger documentation template
with open("swagger.yaml", "r") as f:
    swagger_template = yaml.safe_load(f)

db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
