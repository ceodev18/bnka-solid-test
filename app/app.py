# app/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from app.models import db, User  # Adjust the import statement
from flask_cors import CORS  # Import CORS



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/microservices'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'title': 'User Management API',
    'uiversion': 3,
    'specs_route': '/swagger/',
}
CORS(app)

swagger = Swagger(app)
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

