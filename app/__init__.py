from flask import Flask, session, jsonify, redirect, url_for # added for appinit endpoint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from .models import db, User
from itsdangerous import URLSafeTimedSerializer

# for appinit endpoint
import random
import string
from sqlalchemy.exc import IntegrityError
from .models import db, User, Product, Order
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash



login_manager = LoginManager()
migrate = Migrate()

# Initialize the serializer globally (used for URL token generation)
URL_SERIALIZER = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class="Config"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load the configuration from config.py
    app.config.from_object(f"config.{config_class}")

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set the login view for flask-login
    
    # Initialize migration
    migrate.init_app(app, db)
    
    # Initialize URL serializer (used for token generation)
    global URL_SERIALIZER
    URL_SERIALIZER = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # Register Blueprints
    from .views import bp as views_bp
    from .auth import auth as auth_bp
    from .admin import admin as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create the tables (if needed)
    with app.app_context():
        db.create_all()

    @app.route('/appinit')
    # @login_required
    def appinit():
        dummy_users = []
        failed_users = []
        dummy_products = []
        created_order_ids = []

        # Create two manual users
        try:
            admin_user = User(
                firstname="Admin",
                lastname="Springboard",
                email="admin@springboard.com",
                address_line_1="Random Address",
                state="State1",
                city="City1",
                role="admin",
                pincode=123456,
                password=generate_password_hash('admin')
            )
            user_user = User(
                firstname="User",
                lastname="User",
                email="user@user.com",
                address_line_1="Random Address",
                state="State2",
                city="City2",
                role="user",
                pincode=654321,
                password=generate_password_hash('user')
            )
            db.session.add(admin_user)
            db.session.add(user_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        # Add 100 dummy users
        for _ in range(100):
            firstname, lastname, email, address_line_1, state, city, role, pincode, password = generate_random_user_data()
            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                address_line_1=address_line_1,
                state=state,
                city=city,
                role=role,
                pincode=pincode,
                password=password
            )
            try:
                db.session.add(user)
                db.session.commit()
                dummy_users.append(email)
            except IntegrityError:
                db.session.rollback()
                failed_users.append(email)

        # Create 50 dummy products
        for _ in range(50):
            name, price, stock_quantity, brand, size, target_user, type_, image, description, details, colour, category = generate_random_product_data()
            product = Product(
                name=name,
                price=price,
                stock_quantity=stock_quantity,
                brand=brand,
                size=size,
                target_user=target_user,
                type=type_,
                image=image,
                description=description,
                details=details,
                colour=colour,
                rating=1,
                category=category
            )
            try:
                db.session.add(product)
                db.session.commit()
                dummy_products.append(name)
            except IntegrityError:
                db.session.rollback()

        # Create dummy orders
        users = User.query.all()
        products = Product.query.all()

        if users and products:
            today = datetime.now(timezone.utc)
            start_date = today - timedelta(days=90)  # 3 months ago

            for delta in range(91):  # Generate orders for each day in the last 3 months
                order_date = start_date + timedelta(days=delta)

                for _ in range(random.randint(30, 40)):  # 30 to 40 orders per day
                    customer = random.choice(users)
                    product = random.choice(products)

                    customer_name = f"Customer_{customer.id}"
                    place = random.choice(['Area1', 'Area2', 'Area3', 'Area4'])
                    state = random.choice(['State1', 'State2', 'State3'])
                    pincode = round(random.uniform(100000, 999999), 0)
                    district = random.randint(1, 99)
                    city = random.choice(['City1', 'City2', 'City3'])
                    price = round(random.uniform(10, 500), 2)
                    status = random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
                    mail = f"customer{customer.id}@example.com"

                    order = Order(
                        customer_id=customer.id,
                        customer_name=customer_name,
                        place=place,
                        state=state,
                        pincode=pincode,
                        district=district,
                        city=city,
                        price=price,
                        status=status,
                        product_id=product.id,
                        order_date=order_date,
                        mail=mail
                    )

                    try:
                        db.session.add(order)
                        db.session.commit()
                        created_order_ids.append(order.id)
                    except IntegrityError:
                        db.session.rollback()

        return jsonify({
            "message": "App initialization complete.",
            "manual_users": ["admin@springboard.com", "user@user.com"],
            "created_users": dummy_users,
            "failed_users": failed_users,
            "created_products": dummy_products,
            "created_orders": created_order_ids
        })

    @app.route('/make_me_admin')
    @login_required
    def make_me_admin():
        if not current_user.isAdmin():
            current_user.role = 'admin'
            db.session.commit()
        return redirect(url_for('views.home'))


    return app


# Generate random data for users
def generate_random_user_data():
    firstname = ''.join(random.choices(string.ascii_letters, k=8)).capitalize()
    lastname = ''.join(random.choices(string.ascii_letters, k=10)).capitalize()
    email = f"{firstname.lower()}.{lastname.lower()}@example.com"
    address_line_1 = f"{random.randint(1, 999)} {random.choice(['Main St', 'Second St', 'Broadway'])}"
    state = random.choice(['State1', 'State2', 'State3', 'State4'])
    city = random.choice(['CityA', 'CityB', 'CityC', 'CityD'])
    role = "user"
    pincode = f"{random.randint(10000, 99999)}"
    password = generate_password_hash('password123')  # You can change the password
    return firstname, lastname, email, address_line_1, state, city, role, pincode, password

# Helper function to generate random product data
def generate_random_product_data():
    name = f"Product {''.join(random.choices(string.ascii_uppercase, k=3))}"
    price = round(random.uniform(10, 1000), 2)
    stock_quantity = random.randint(1, 100)
    brand = random.choice(["BrandA", "BrandB", "BrandC"])
    size = random.choice(["Small", "Medium", "Large"])
    target_user = random.choice(["Men", "Women", "Kids"])
    type_ = random.choice(["Type1", "Type2", "Type3"])
    image = "https://via.placeholder.com/150"
    description = "Lorem ipsum dolor sit amet."
    details = "Detailed description here."
    colour = random.choice(["Red", "Blue", "Green", "Black"])
    category = random.choice(["Category1", "Category2", "Category3"])
    return name, price, stock_quantity, brand, size, target_user, type_, image, description, details, colour, category

