from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum


# Initialize the database
db = SQLAlchemy()


# Define the Customer model
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(Enum('customer', name='role'), default='customer')

# Define the Professional model
class Professional(db.Model):
    professional_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    service_name = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    document = db.Column(db.LargeBinary)  # To store PDF as binary data
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(Enum('professional', name='role'), default='professional')

# Define the Admin model
class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
