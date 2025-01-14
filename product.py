from flask_sqlalchemy import SQLAlchemy

from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product, db


bp = Blueprint('product', __name__)

#
# @bp.route('/products')
# def show_products():
#     products = Product.query.all()
#     return render_template('delivery-items.html', products=products)
#
#
# @bp.route('/product/update/<int:id>', methods=['GET', 'POST'])
# def update_product(id):
#     product = Product.query.get(id)
#     if not product:
#         return "Product not found", 404
#
#     if request.method == 'POST':
#         product.name = request.form['name']
#         product.price = float(request.form['price'])
#         product.category = request.form['category']
#         product.brand = request.form['brand']
#         product.image = request.form.get('image', product.image)
#
#         db.session.commit()
#         return redirect(url_for('product.show_products'))
#
#     return render_template('update-details.html', product=product)
#
# # init.py ->     from .auth import auth
# #     from .views import views
# #     from .admin import admin
# #     app.register_blueprint(views, url_prefix='/')
# #     app.register_blueprint(auth, url_prefix='/auth')
# #     app.register_blueprint(admin, url_prefix='/admin')
#
# # Fadmin.py ->admin = Blueprint('admin', __name__)
#
#
#
