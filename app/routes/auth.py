from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db  

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    address = data.get('address')
    role = data.get('role', 'customer')  # Default to customer

    if not all([name, email, password]):
        flash('Name, email, and password are required!', 'error')
        return redirect(url_for('auth.register_form'))

    if User.query.filter_by(email=email).first():
        flash('Email already exists!', 'error')
        return redirect(url_for('auth.register_form'))

    hashed_password = generate_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        phone=phone,
        address=address,
        role=role
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login_form'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error during registration: {str(e)}', 'error')
        return redirect(url_for('auth.register_form'))

@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = user.role
        flash('Login successful!', 'success')
        if user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif user.role == 'delivery':
            return redirect(url_for('main.delivery_dashboard'))
        else:
            return redirect(url_for('main.customer_dashboard'))
    else:
        flash('Invalid email or password!', 'error')
        return redirect(url_for('auth.login_form'))

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login_form'))