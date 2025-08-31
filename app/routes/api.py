from flask import Blueprint, request, jsonify, session
from app.models.product import Product
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.delivery import Delivery
from app.models.user import User
from app import db  
from datetime import datetime

api_bp = Blueprint('api', __name__)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def admin_required(f):
    def wrap(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def delivery_or_admin_required(f):
    def wrap(*args, **kwargs):
        if session.get('role') not in ['admin', 'delivery']:
            return jsonify({'error': 'Admin or Delivery access required'}), 403
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Product Management
# @api_bp.route('/products', methods=['GET'])
# def get_products():
#     products = Product.query.all()
#     return jsonify([{
#         'id': p.id,
#         'name': p.name,
#         'description': p.description,
#         'price': p.price,
#         'stock': p.stock,
#         'category': p.category
#     } for p in products])

@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category': product.category
    })

@api_bp.route('/products', methods=['POST'])
@admin_required
def create_product():
    data = request.json
    new_product = Product(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        stock=data.get('stock', 0),
        category=data.get('category')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'id': new_product.id}), 201

@api_bp.route('/products/<int:id>', methods=['PUT'])
@admin_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.category = data.get('category', product.category)
    db.session.commit()
    return jsonify({'message': 'Product updated'})

@api_bp.route('/products/<int:id>', methods=['DELETE'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

# Order Management
@api_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'No items in order'}), 400

    total_price = 0
    order_items = []
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            return jsonify({'error': f'Invalid product or insufficient stock for {item["product_id"]}'}), 400
        total_price += product.price * item['quantity']
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item['quantity'],
            price=product.price
        ))

    order = Order(
        user_id=session['user_id'],
        total_price=total_price,
        status='pending',
        created_at=datetime.utcnow()
    )
    db.session.add(order)
    db.session.flush()

    for item in order_items:
        item.order_id = order.id
        db.session.add(item)
        product = Product.query.get(item.product_id)
        product.stock -= item.quantity

    db.session.commit()
    return jsonify({'message': 'Order created', 'id': order.id}), 201

@api_bp.route('/orders/<int:id>', methods=['GET'])
@login_required
def get_order(id):
    order = Order.query.get_or_404(id)
    if session.get('role') != 'admin' and order.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'total_price': order.total_price,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.order_items]
    })

@api_bp.route('/orders/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_orders(user_id):
    if session.get('role') != 'admin' and user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': o.id,
        'total_price': o.total_price,
        'status': o.status,
        'created_at': o.created_at.isoformat()
    } for o in orders])

@api_bp.route('/orders/<int:id>/cancel', methods=['PUT'])
@login_required
def cancel_order(id):
    order = Order.query.get_or_404(id)
    if session.get('role') != 'admin' and order.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    if order.status != 'pending':
        return jsonify({'error': 'Can only cancel pending orders'}), 400
    order.status = 'cancelled'
    for item in order.order_items:
        product = Product.query.get(item.product_id)
        product.stock += item.quantity
    db.session.commit()
    return jsonify({'message': 'Order cancelled'})

@api_bp.route('/orders/<int:id>/accept', methods=['PUT'])
@delivery_or_admin_required
def accept_order(id):
    order = Order.query.get_or_404(id)
    if order.status != 'pending':
        return jsonify({'error': 'Can only accept pending orders'}), 400
    order.status = 'accepted'
    db.session.commit()
    return jsonify({'message': 'Order accepted'})

@api_bp.route('/orders/<int:id>/assign/<int:agent_id>', methods=['PUT'])
@admin_required
def assign_delivery(id, agent_id):
    order = Order.query.get_or_404(id)
    agent = User.query.filter_by(id=agent_id, role='delivery').first()
    if not agent:
        return jsonify({'error': 'Invalid delivery agent'}), 400
    if order.status != 'accepted':
        return jsonify({'error': 'Can only assign accepted orders'}), 400
    
    delivery = Delivery(
        order_id=id,
        delivery_person_id=agent_id,
        delivery_status='assigned'
    )
    db.session.add(delivery)
    order.status = 'out_for_delivery'
    db.session.commit()
    return jsonify({'message': 'Delivery assigned'})

@api_bp.route('/orders/<int:id>/status', methods=['PUT'])
@delivery_or_admin_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    data = request.json
    new_status = data.get('status')
    if new_status not in ['pending', 'accepted', 'out_for_delivery', 'delivered', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    order.status = new_status
    db.session.commit()
    return jsonify({'message': 'Order status updated'})

# Payment Routes
@api_bp.route('/payments', methods=['POST'])
@login_required
def initiate_payment():
    data = request.json
    order_id = data.get('order_id')
    order = Order.query.get_or_404(order_id)
    if order.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    # Implement payment processing logic here
    return jsonify({'message': 'Payment initiated', 'payment_id': f'pay_{order_id}'})

@api_bp.route('/payments/<id>', methods=['GET'])
@login_required
def get_payment_status(id):
    # Implement payment status checking logic
    return jsonify({'payment_id': id, 'status': 'pending'})

@api_bp.route('/payments/<id>/confirm', methods=['PUT'])
@admin_required
def confirm_payment(id):
    # Implement payment confirmation logic
    return jsonify({'message': 'Payment confirmed'})

# Delivery Tracking
@api_bp.route('/delivery/<int:order_id>', methods=['GET'])
@login_required
def track_delivery(order_id):
    delivery = Delivery.query.filter_by(order_id=order_id).first_or_404()
    return jsonify({
        'order_id': delivery.order_id,
        'delivery_person_id': delivery.delivery_person_id,
        'delivery_status': delivery.delivery_status,
        'location': delivery.location
    })

@api_bp.route('/delivery/<int:order_id>/update', methods=['PUT'])
@delivery_or_admin_required
def update_delivery(order_id):
    delivery = Delivery.query.filter_by(order_id=order_id).first_or_404()
    data = request.json
    delivery.delivery_status = data.get('delivery_status', delivery.delivery_status)
    delivery.location = data.get('location', delivery.location)
    if delivery.delivery_status == 'delivered':
        order = Order.query.get(order_id)
        order.status = 'delivered'
    db.session.commit()
    return jsonify({'message': 'Delivery updated'})