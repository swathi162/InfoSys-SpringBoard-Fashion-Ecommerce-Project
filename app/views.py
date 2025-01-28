from flask import Blueprint, render_template, get_flashed_messages, redirect, url_for, Response, flash, request, session, jsonify
from flask_login import login_required, current_user
from .models import db
from .forms import UpdateUserForm
from .decorators import is_delivery_person, is_admin
from .constants import STATES_CITY, PRODUCTS
bp = Blueprint('views', __name__)
from .models import Product, Order, Stats
import os
import logging
from werkzeug.utils import secure_filename
from .methods import send_thankyou_email


@bp.route("/")
@bp.route('/home')
@login_required
def home():
    print("going to render homepage...")
    return render_template('home.html', products=PRODUCTS)


@bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product.html', product=product)


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    get_flashed_messages()
    form = UpdateUserForm(obj=current_user)  # Populate the form with the current user's data
    if form.state.data in STATES_CITY:
        form.city.choices = [(city, city) for city in STATES_CITY[form.state.data]]
    else:
        form.city.choices = []

    if request.method == 'POST' and form.validate_on_submit():
        try:
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.address_line_1 = form.address_line_1.data
            current_user.state = form.state.data
            current_user.city = form.city.data
            current_user.role = form.role.data
            current_user.pincode = form.pincode.data

            db.session.commit()
            flash('Details updated successfully!', 'success')
            return redirect(url_for('auth.update_user'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template(
        'update_user.html',
        form=form,
        STATES_CITY=STATES_CITY
    )


@bp.route('/auth_error')
def auth_error():
    return render_template('notAuthorized.html')

@bp.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Ensure product_id is an integer
    try:
        product_id = int(product_id)
    except ValueError:
        return "Invalid product ID", 400

    # Initialize cart in session if not already present
    if 'cart' not in session:
        session['cart'] = {}

    # Initialize cart to hold products as integers
    cart = {int(k): v for k, v in session['cart'].items()}

    # Get the product from the products list
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)

    if product:
        # If product is already in the cart, increment the quantity, but not exceeding stock
        if product_id in cart:
            if cart[product_id] < product['stock']:
                cart[product_id] += 1  # Increment quantity by 1
            else:
                # If the cart quantity reaches stock, don't increase it further
                cart[product_id] = product['stock']
        else:
            # Add the product to the cart with a quantity of 1 if it's not already in the cart
            cart[product_id] = 1

    # Save the updated cart back to the session
    session['cart'] = cart

    # Redirect to the product details page or referrer
    return redirect(request.referrer)


@bp.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total_price = 0  # Initialize total price
    total_items = 0  # Initialize total items count

    # Loop through the cart to get each product and calculate totals
    for product_id, quantity in cart.items():
        product_id = int(product_id)

        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if product:
            product_copy = product.copy()
            product_copy["quantity"] = quantity
            cart_items.append(product_copy)

            # Calculate total price for this product
            total_price += product["price"] * quantity
            total_items += quantity  # Add quantity to total items

    # Pass total price and total items to the template
    return render_template("cart.html", cart_items=cart_items, total_price=total_price, total_items=total_items)

@bp.route("/update_quantity/<int:product_id>", methods=["POST"])
def update_quantity(product_id):
    cart = session.get("cart", {})
    try:
        # Parse new quantity from request data
        new_quantity = int(request.json.get('quantity', 1))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

    product = next((p for p in PRODUCTS if p['id'] == product_id), None)

    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    if new_quantity > product['stock']:
        new_quantity = product['stock']  # Cap quantity to available stock

    if new_quantity < 1:
        cart.pop(str(product_id), None)  # Remove product if quantity is 0 or less
    else:
        cart[str(product_id)] = new_quantity

    session['cart'] = cart

    # Calculate new total price and total items
    total_price = sum(product["price"] * quantity for product_id, quantity in cart.items() if (product := next((p for p in PRODUCTS if p["id"] == int(product_id)), None)))
    total_items = sum(cart.values())  # Total items is the sum of all quantities

    return jsonify({'success': True, 'new_quantity': new_quantity, 'total_price': total_price, 'total_items': total_items})

@bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash("Item removed from cart!", "success")
    return redirect(url_for('views.cart'))



@bp.route('/search')
def search():
    query = request.args.get('query', '').lower()  # Get the search query from the URL parameters
    query_words = query.split()  # Split the query into individual words
    
    if query:
        results = []
        
        # Loop through each product and check if it matches the individual words or combined query
        for p in PRODUCTS:
            try:
                # Combine product attributes into one string for easier matching
                product_str = (
                    str(p.get('name', '')).lower() + ' ' + 
                    str(p.get('description', '')).lower() + ' ' + 
                    str(p.get('brand', '')).lower() + ' ' + 
                    str(p.get('colour', '')).lower() + ' ' + 
                    str(p.get('category', '')).lower() + ' ' + 
                    str(p.get('target_user', '')).lower() + ' ' + 
                    str(p.get('type', '')).lower()
                )
                
                # Check for exact matches for each word in the query
                individual_match = all(word in product_str.split() for word in query_words)
                
                # Check if the entire query (combined) exists in the product attributes (combined search)
                combined_match = query in product_str
                
                if individual_match or combined_match:
                    results.append(p)
            except Exception as e:
                print(f"Error processing product: {p}. Error: {e}")
                continue  # Skip any products that cause an error
                
    else:
        results = []  # No results if query is empty
    
    return render_template('search_results.html', query=query, results=results)


@bp.route('/category/<category>')
def category(category):
    category = category.lower()
    results = [p for p in PRODUCTS if p['category'].lower() == category]
    return render_template('category_results.html', category=category.capitalize(), results=results)

@bp.route('/deliver')
@is_delivery_person
def deliver():
    return Response("Delivered", status=200)



#<a href="{{ url_for('views.view_product', id=product.id) }}" class="btn btn-info btn-sm">View</a>




@bp.route('/partner_dash')
# @is_delivery_person
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

        # If the status is "Delivered Successfully", send a thank-you email
        if new_status == 'Delivered Successfully':
            rating_url = url_for('views.rate_product', order_id=order.id, _external=True)
            print(rating_url)
            send_thankyou_email(order.user.email, order.user.first_name, rating_url=None)

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


# @bp.route('/update_status/<int:order_id>', methods=['POST'])
# def update_status(order_id):
#     new_status = request.form['status']
#     order = Order.query.get(order_id)

#     if order:
#         # Update the order status
#         order.status = new_status
#         db.session.commit()

#         # If status is "Delivered Successfully", send an email to the user
#         if new_status == "Delivered Successfully":
#             send_rating_email(order)

#         # Update stats if needed
#         update_stats()

#     return redirect(url_for('views.dashboard'))
# #
# #
# def send_rating_email(order):
#     user_email = order.user.email  # Get the user's email (assuming the order has a user reference)
#     product = order.product  # Get the product related to the order

#     # Create the message
#     subject = "Your Order has been Delivered! Please Rate Your Product"
#     body = f"""
#     Hi {order.user.first_name},

#     We hope you're enjoying your new product: {product.name}.

#     Could you please rate the product from 1 to 5 (1 being the worst, 5 being the best)?
#     Your feedback helps us improve our products and services!

#     Click the link below to rate the product:
#     {url_for('views.submit_rating', order_id=order.id, _external=True)}

#     Thank you for your support!
#     """

#     # Send the email
#     msg = Message(subject, recipients=[user_email], body=body)
#     mail.send(msg)


####################################mail###################



@bp.route('/rate_product/<int:order_id>', methods=['GET', 'POST'])

def rate_product(order_id):
    # Fetch the order using the order_id
    order = Order.query.get_or_404(order_id)

    # Fetch the product associated with the order
    product = Product.query.get_or_404(order.product_id)

    if request.method == 'POST':
        try:
            # Get the user's rating from the form (rating is expected to be between 1 and 5)
            rating = request.form['rating']  # Assumes the form will send a 'rating' field as 1, 2, 3, 4, or 5
            customer_rating = int(rating)  # Convert rating to integer

            # Check if the product has already been rated
            if product.rating == 'not rated':
                # If not rated yet, store the customer's rating
                product.rating = str(customer_rating)
            else:
                # If rated, calculate the new average rating
                current_rating = float(product.rating)
                new_rating = (current_rating + customer_rating) / 2
                product.rating = str(new_rating)

            # Commit the changes to the database
            db.session.commit()

            # Flash success message and redirect to the product page or a thank-you page
            flash(f"Thank you for rating! Your rating of {customer_rating} has been saved.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while rating the product: {e}")
            flash("An error occurred while submitting your rating. Please try again later.", "danger")
            return redirect(url_for('views.view_product', id=product.id))

    return render_template('rate_product.html', product=product,order=order)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')