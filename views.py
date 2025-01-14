import os
from flask import Blueprint, render_template, redirect, url_for, request , flash
from flask_login import login_required,current_user

from werkzeug.utils import secure_filename



from . import db
from .models import Product,db
from .models import Stats, db
from .models import Order, db




bp = Blueprint('product', __name__)

bp = Blueprint('views', __name__)




@bp.route('/')
@login_required
def home():
    # Check the role of the logged-in user
    if current_user.role == 'delivery':  # Assuming 'delivery' is the role for delivery partners
        return redirect(url_for('views.dashboard'))  # Redirect to delivery dashboarde
    elif current_user.role == 'admin':
        return redirect(url_for('views.index'))

    return render_template('home.html')


@bp.route('/admin')
@login_required
def index():
    return render_template('admin.html')

@bp.route('/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        try:
            # Extract form fields
            name = request.form['name']
            description = request.form['description']
            details = request.form['details']
            price = float(request.form['price'])
            stock_quantity = int(request.form['stock_quantity'])
            brand = request.form['brand']
            size = request.form['size']
            target_user = request.form['target_user']
            type_ = request.form['type']
            rating = float(request.form['rating'])
            category = request.form['category']

            # Validate required fields
            if not all([name, description, brand, category, size, target_user, type_]):
                return "Missing required fields", 400

            # Handle image upload (if exists)
            image = request.files.get('image')
            image_filename = None
            if image:
                # Ensure the 'static/uploads' directory exists
                uploads_dir = os.path.join('static', 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)  # Create the directory if it doesn't exist

                # Sanitize the image filename and save it
                image_filename = secure_filename(image.filename)
                image_path = os.path.join(uploads_dir, image_filename)
                image.save(image_path)

            # Create the product object
            new_product = Product(
                name=name,
                description=description,
                details=details,
                price=price,
                stock_quantity=stock_quantity,
                brand=brand,
                size=size,
                target_user=target_user,
                type=type_,
                rating=rating,
                category=category,
                image=image_filename
            )

            # Commit to the database
            db.session.add(new_product)
            db.session.commit()

            flash("Product added successfully!", "success")
            return redirect(url_for('views.product_list'))

        except Exception as e:
            db.session.rollback()
            print(f"Error while adding product: {e}")  # Log the error to the console
            return f"Error while adding product: {e}", 500  # Return the error message

    return render_template('add-shop-items.html')
##########
@bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    # Fetch the product from the database by its ID
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # Extract form fields
            name = request.form['name']
            description = request.form['description']
            details = request.form['details']
            price = float(request.form['price'])
            stock_quantity = int(request.form['stock_quantity'])
            brand = request.form['brand']
            size = request.form['size']
            target_user = request.form['target_user']
            type_ = request.form['type']
            rating = float(request.form['rating'])
            category = request.form['category']

            # Validate required fields
            if not all([name, description, brand, category, size, target_user, type_]):
                return "Missing required fields", 400

            # Handle image upload (if exists)
            image_filename = product.image  # Retain the old image filename if no new image is uploaded
            image = request.files.get('image')
            if image:
                # Ensure the 'static/uploads' directory exists
                uploads_dir = os.path.join('static', 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)  # Create the directory if it doesn't exist

                # Sanitize the image filename and save it
                image_filename = secure_filename(image.filename)
                image_path = os.path.join(uploads_dir, image_filename)
                image.save(image_path)

            # Update the product object with new data
            product.name = name
            product.description = description
            product.details = details
            product.price = price
            product.stock_quantity = stock_quantity
            product.brand = brand
            product.size = size
            product.target_user = target_user
            product.type = type_
            product.rating = rating
            product.category = category
            product.image = image_filename  # Update the image (if new image uploaded)

            # Commit to the database
            db.session.commit()

            flash("Product updated successfully!", "success")
            return redirect(url_for('views.product_list'))  # Redirect to the product list page

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while updating product: {e}")
            return f"Error while updating product: {e}", 500  # Internal error

    # If it's a GET request, render the form with the current product data
    return render_template('update-product.html', product=product)
############
@bp.route('/products', methods=['GET'])
def product_list():

    products = Product.query.all()

    # Render the template to display all products
    return render_template('product-list.html', products=products)

###################################
@bp.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    # Fetch the product from the database by its ID
    product = Product.query.get_or_404(id)

    try:
        # Delete the product
        db.session.delete(product)
        db.session.commit()

        print(f"Product {id} deleted successfully")
        return redirect(url_for('views.product_list'))  # Redirect back to the product list page

    except Exception as e:
        print(f"Error occurred while deleting product: {e}")
        db.session.rollback()
        return "Error while deleting product", 500  # Internal server error






#<a href="{{ url_for('views.view_product', id=product.id) }}" class="btn btn-info btn-sm">View</a>




@bp.route('/partner_dash')
def dashboard():
    # Fetch user info (hardcoded for now, you can change this later)
    user = {'name': current_user.firstname, 'pincode':current_user.pincode}

    # Fetch stats from the database
    stats = Stats.query.first()  # Assuming there's only one stats row for simplicity
    if not stats:
        stats = Stats(total_orders=0, delivered=0, in_transit=0, failed=0)
        db.session.add(stats)
        db.session.commit()

    # Fetch orders from the database
    orders = Order.query.filter_by(pincode=user['pincode']).all()

    # Only allow orders in the user's state (California in this case) to be viewed or delivered
    return render_template('delivery_person_dashboard.html', user=user, stats=stats, orders=orders)


@bp.route('/update_status/<int:order_id>', methods=['POST'])
def update_status(order_id):
    new_status = request.form['status']  # Get the selected status from the form
    order = Order.query.get(order_id)  # Fetch the order by ID from the database

    if order:
        # Update the order's status
        order.status = new_status
        db.session.commit()

        # Update stats (optional, but if required to refresh stats)
        update_stats()

    return redirect(url_for('views.dashboard'))  # Redirect back to the dashboard or the orders list


def update_stats():
    # Recalculate stats for the dashboard or stats view
    stats = Stats.query.first()
    stats.total_orders = Order.query.count()
    stats.delivered = Order.query.filter_by(status='Delivered Successfully').count()
    stats.in_transit = Order.query.filter_by(status='In Transit').count()
    stats.failed = Order.query.filter_by(status='Failed').count()
    db.session.commit()


@bp.route('/view_orders', methods=['GET'])

def view_orders():

    orders = Order.query.all()

    # Render the template to display all orders
    return render_template('view_order.html', orders=orders)



