from flask import Flask, render_template, Blueprint, session, redirect, url_for

from app.models.product import Product

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif session['role'] == 'delivery':
            return redirect(url_for('main.delivery_dashboard'))
        else:
            return redirect(url_for('main.customer_dashboard'))
    return redirect(url_for('auth.login_form'))

@main_bp.route('/customer')
def customer_dashboard():
    if 'user_id' not in session or session['role'] != 'customer':
        return redirect(url_for('auth.login_form'))
    return render_template('customer_dashboard.html')

@main_bp.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login_form'))
    return render_template('admin_dashboard.html')

@main_bp.route('/delivery')
def delivery_dashboard():
    if 'user_id' not in session or session['role'] != 'delivery':
        return redirect(url_for('auth.login_form'))
    return render_template('delivery_dashboard.html')

@main_bp.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session or (session['user_id'] != user_id and session['role'] != 'admin'):
        return redirect(url_for('auth.login_form'))
    return render_template('profile.html', user_id=user_id)

@main_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    if 'user_id' not in session or (session['user_id'] != user_id and session['role'] != 'admin'):
        return redirect(url_for('auth.login_form'))
    # TO BE IMPLEMENTED 
    return render_template('profile.html', user_id=user_id)


@main_bp.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_form'))
    products = Product.query.all()
    return render_template('products.html', products=products, user_role=session.get('role'))