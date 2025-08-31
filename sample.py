from app import create_app, db
from app.models.user import User 
from app.models.product import Product
from werkzeug.security import generate_password_hash

def create_users_and_products():
    # Create the Flask app
    app = create_app()
    
    # Use the app context to interact with the database
    with app.app_context():
        # Check if users already exist
        if User.query.filter_by(email='admin@example.com').first() or User.query.filter_by(email='user@example.com').first():
            print("Admin or User already exists in the database.")
        else:
            # Create Admin
            admin = User(
                name="Admin User",
                email="admin@example.com",
                password=generate_password_hash("adminpassword123"),
                phone="123-456-7890",
                address="123 Admin St, City",
                role="admin"
            )
            
            # Create Regular User (Customer)
            customer = User(
                name="John Doe",
                email="user@example.com",
                password=generate_password_hash("userpassword123"),
                phone="987-654-3210",
                address="456 User Ave, City",
                role="customer"
            )
            
            try:
                # Add users to the database
                db.session.add(admin)
                db.session.add(customer)
                db.session.commit()
                print("Admin and User created successfully!")
                print(f"Admin: {admin.email} (Role: {admin.role})")
                print(f"User: {customer.email} (Role: {customer.role})")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating users: {str(e)}")
                return

        # Check if products already exist
        if Product.query.count() >= 10:
            print("At least 10 products already exist in the database.")
            return

        # Create 10 Products
        products = [
            Product(
                name="Laptop Pro",
                description="High-performance laptop with 16GB RAM and 512GB SSD",
                price=999.99,
                stock=50,
                category="Electronics"
            ),
            Product(
                name="Wireless Headphones",
                description="Noise-cancelling over-ear headphones with 20-hour battery life",
                price=149.99,
                stock=100,
                category="Electronics"
            ),
            Product(
                name="Smartphone X",
                description="Latest smartphone with 128GB storage and 48MP camera",
                price=699.99,
                stock=75,
                category="Electronics"
            ),
            Product(
                name="Running Shoes",
                description="Comfortable running shoes with advanced cushioning",
                price=89.99,
                stock=200,
                category="Footwear"
            ),
            Product(
                name="Backpack",
                description="Durable backpack with multiple compartments",
                price=49.99,
                stock=150,
                category="Accessories"
            ),
            Product(
                name="Coffee Maker",
                description="Programmable coffee maker with 12-cup capacity",
                price=79.99,
                stock=80,
                category="Appliances"
            ),
            Product(
                name="Gaming Mouse",
                description="Ergonomic mouse with customizable RGB lighting",
                price=39.99,
                stock=120,
                category="Electronics"
            ),
            Product(
                name="Yoga Mat",
                description="Non-slip yoga mat with carrying strap",
                price=29.99,
                stock=300,
                category="Fitness"
            ),
            Product(
                name="Stainless Steel Water Bottle",
                description="Insulated water bottle, keeps drinks cold for 24 hours",
                price=24.99,
                stock=250,
                category="Accessories"
            ),
            Product(
                name="Desk Lamp",
                description="LED desk lamp with adjustable brightness",
                price=34.99,
                stock=90,
                category="Home"
            )
        ]

        try:
            # Add products to the database
            for product in products:
                db.session.add(product)
            db.session.commit()
            print("10 products created successfully!")
            for product in products:
                print(f"Product: {product.name} (Price: ${product.price}, Category: {product.category})")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating products: {str(e)}")

if __name__ == "__main__":
    create_users_and_products()