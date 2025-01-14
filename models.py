from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




db = SQLAlchemy()


class User(UserMixin,db.Model):
    def __init__(self, password, email, address, role, firstname, lastname, pincode):
        self.password = password
        self.email = email
        self.address = address
        self.role = role
        self.firstname = firstname
        self.lastname = lastname
        self.pincode = pincode


    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    pincode = db.Column(db.Float, nullable=False)

    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    
# Product Model (new)
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)  # Product name
#     description = db.Column(db.Text, nullable=False)  # Product description
#     price = db.Column(db.Float, nullable=False)  # Price in decimal format
#     stock_quantity = db.Column(db.Integer, nullable=False)  # Stock quantity
#     brand = db.Column(db.String(100), nullable=False)  # Product brand
#     category = db.Column(db.String(100), nullable=False)  # Product category
#     rating = db.Column(db.Float, nullable=False)  # Product rating (1-5 scale)
#     ratting = db.Column(db.String(100), nullable=False)  # Rating description (e.g., "Excellent")
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    target_user = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    details = db.Column(db.Text)
    rating=db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100),nullable=False)




class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Float, nullable=False)

    district = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)


class Stats(db.Model):
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    total_orders = db.Column(db.Integer, default=0)
    delivered = db.Column(db.Integer, default=0)
    in_transit = db.Column(db.Integer, default=0)
    failed = db.Column(db.Integer, default=0)


