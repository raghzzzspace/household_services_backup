
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from model import db, Customer, Professional, Admin
import secrets
from flask_migrate import Migrate
import sqlite3

app = Flask(__name__, instance_relative_config=True)
app.secret_key = secrets.token_hex(16)

# Set the database URI (using the correct SQLite URI format)
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:/Users/Ishita Tayal/Desktop/household_services.db"  # Absolute path for SQLite

# Disable track modifications (optional)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Create the tables (Only needed on the first run)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect('C:/Users/Ishita Tayal/Desktop/household_services.db')
        cursor = connection.cursor()
        cursor.execute("SELECT customer_id FROM customer WHERE email = ? AND password = ?", (email, password))
        customerq = cursor.fetchone()

        # Check if the user is a Customer
        customer = Customer.query.filter_by(email=email, password=password).first()
        if customer:
            session['customer_id'] = customerq[0]
            flash(f'Welcome back, {customer.full_name}!', 'success')
            return redirect(url_for('cust_dashboard'))  # Redirect to Customer Dashboard

        # Check if the user is a Professional
        professional = Professional.query.filter_by(email=email, password=password).first()
        if professional:
            flash(f'Welcome back, {professional.full_name}!', 'success')
            return redirect(url_for('professional_dashboard'))  # Redirect to Professional Dashboard

        # Check if the user is an Admin
        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            flash(f'Welcome back, {admin.email}!', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirect to Admin Dashboard

        # If no match is found, flash an error message
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('user_login'))  # Redirect back to login page

    return render_template('user/login.html')


@app.route('/user/customer_dashboard', methods=['GET'])
def cust_dashboard():
    return render_template('user/customer_dashboard.html')

@app.route('/user/customer_profile', methods=['GET'])
def cust_profile():
    customer_id = session['customer_id']  # Retrieve customer_id from session
    connection = sqlite3.connect('C:/Users/Ishita Tayal/Desktop/household_services.db')
    cursor = connection.cursor()
    cursor.execute("SELECT email, full_name, address, pincode FROM customer WHERE customer_id = ?", (customer_id,))
    customer_data = cursor.fetchone()

    if not customer_data:
        return "Customer not found", 404

    customer = {
        "email": customer_data[0],
        "fullname": customer_data[1],
        "address": customer_data[2],
        "pincode": customer_data[3]
    }
    return render_template('user/customer_profile.html', customer=customer)

@app.route('/user/customer_remarks', methods=['GET'])
def cust_remarks():
    return render_template('user/customer_remarks.html')

@app.route('/user/customer_search', methods=['GET'])
def cust_search():
    return render_template('user/customer_search.html')

@app.route('/user/customer_summary', methods=['GET'])
def cust_summary():
    return render_template('user/customer_summary.html')

@app.route('/professional/login', methods=['GET'])
def service_professional_login():
    return render_template('user/login.html')

@app.route('/admin/login', methods=['GET'])
def admin_login():
    return render_template('user/login.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']

        # Check if the email exists in the Customer table
        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/register.html')  # Render the same page with the flash message

        # Check if the email exists in the Professional table
        existing_professional = Professional.query.filter_by(email=email).first()
        if existing_professional:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/register.html')  # Render the same page with the flash message

        # Create a new Customer object
        new_customer = Customer(
            email=email,
            password=password,
            full_name=full_name,
            address=address,
            pincode=pincode,
            role='customer'
        )

        # Add to the database
        db.session.add(new_customer)
        db.session.commit()

        flash('Registered Successfully! Please login to continue.', 'success')
        return render_template('user/register.html')  # Render the same page with the success message

    return render_template('user/register.html')


@app.route('/user/service_prof_signup', methods=['GET','POST'])
def service_prof_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['fullname']
        service_name = request.form['service_name']
        experience = request.form['experience']
        document = request.files['documents']
        address = request.form['address']
        pincode = request.form['pincode']

        # Check if the email exists in the Customer table
        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/service_prof_signup.html')  # Render the same page with the flash message

        # Check if the email exists in the Professional table
        existing_professional = Professional.query.filter_by(email=email).first()
        if existing_professional:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/service_prof_signup.html')  # Render the same page with the flash message

        # Save the document as binary data if necessary
        document_data = document.read() if document else None

        # Create a new Professional object
        new_professional = Professional(
            email=email,
            password=password,
            full_name=full_name,
            service_name=service_name,
            experience=experience,
            document=document_data,  # Store PDF as binary data
            address=address,
            pincode=pincode,
            role='professional'
        )

        # Add to the database
        db.session.add(new_professional)
        db.session.commit()

        flash('Registered Successfully! Please login to continue.', 'success')
        return render_template('user/service_prof_signup.html')  # Render the same page with the success message

    return render_template('user/service_prof_signup.html')


@app.route('/user/professional_dashboard', methods=['GET'])
def professional_dashboard():
    return render_template('user/professional_dashboard.html')

@app.route('/user/professional_search', methods=['GET'])
def professional_search():
    return render_template('user/professional_search.html')

@app.route('/user/professional_summary', methods=['GET'])
def professional_summary():
    return render_template('user/professional_summary.html')

@app.route('/user/admin_dashboard', methods=['GET'])
def admin_dashboard():
    return render_template('user/admin_dashboard.html')

@app.route('/user/admin_search', methods=['GET'])
def admin_search():
    return render_template('user/admin_search.html')

@app.route('/user/admin_summary', methods=['GET'])
def admin_summary():
    return render_template('user/admin_summary.html')

from flask import session

@app.route('/logout')
def logout():
    session.clear()  # Clears session data
    resp = redirect(url_for('user_login'))
    resp.set_cookie('session', '', expires=0)  # Clear session cookie
    flash('You have been logged out successfully.', 'info')
    return resp



@app.route('/user/admin_profile', methods=['GET'])
def admin_profile():
    return render_template('/user/admin_profile.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7000)
