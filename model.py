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

class Today_Services(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    customer_name=db.Column(db.String(256),nullable=False)
    contact_no=db.Column(db.Integer,nullable=False,unique=True)
    location=db.Column(db.String,nullable=True)

class Closed_Services(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    customer_name=db.Column(db.String(256),nullable=False)
    contact_no=db.Column(db.Integer,nullable=False,unique=True)
    location=db.Column(db.String,nullable=False)
    date=db.Column(db.Date,nullable=False)
    rating=db.Column(db.Integer)