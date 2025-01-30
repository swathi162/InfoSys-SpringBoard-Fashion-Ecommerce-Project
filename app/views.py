from flask import Blueprint, render_template, get_flashed_messages, redirect, url_for, Response, flash, request, session, jsonify
from flask_login import login_required, current_user
from .models import db, Wishlist,Order,CartItem,OrderItems
from .forms import UpdateUserForm
from .decorators import is_delivery_person, is_admin
from .constants import STATES_CITY, PRODUCTS
bp = Blueprint('views', __name__)
from .models import Product, Order, Stats
import os
from datetime import datetime,timezone
import logging
from werkzeug.utils import secure_filename
from .methods import send_thankyou_email

OrderItem = OrderItems

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


@bp.route('/wishlist')
@login_required
def view_wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    products_in_wishlist = []
    for item in wishlist_items:
        product = next((p for p in PRODUCTS if p['id'] == item.product_id), None)
        if product:
            products_in_wishlist.append(product)

    return render_template('wishlist.html', products=products_in_wishlist)

@bp.route('/wishlist')
@login_required
def remove_from_wishlist(product_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash("Item removed from wishlist!", "success")
    else:
        flash("Item not found in wishlist.", "error")

    return redirect(url_for('views.view_wishlist'))

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please log in to add items to the cart.", "warning")
        return redirect(url_for('auth.login'))

    # Get the product details
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    # Check if the item already exists in the user's cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        # If the product is already in the cart, update the quantity
        if cart_item.quantity < product['stock']:
            cart_item.quantity += 1
        else:
            flash("Stock limit reached!", "warning")
    else:
        # Add new product to the cart
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash("Product added to cart!", "success")
    return redirect(request.referrer)


@bp.route('/cart')
def cart():
    if not current_user.is_authenticated:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for('auth.login'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    items_in_cart = []
    total_price = 0
    total_items = 0

    for item in cart_items:
        # Match with the dummy products
        product = next((p for p in PRODUCTS if p['id'] == item.product_id), None)
        if product:
            product_copy = product.copy()
            product_copy['quantity'] = item.quantity
            items_in_cart.append(product_copy)
            total_price += product['price'] * item.quantity
            total_items += item.quantity

    return render_template(
        'cart.html',
        cart_items=items_in_cart,
        total_price=total_price,
        total_items=total_items
    )

@bp.route("/update_quantity/<int:product_id>", methods=["POST"])
def update_quantity(product_id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Please log in to update your cart.'}), 403

    # Get the cart item for the user and product
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'success': False, 'message': 'Item not found in cart'}), 404

    try:
        new_quantity = int(request.json.get('quantity', 1))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

    # Check if the new quantity exceeds stock
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    if new_quantity > product['stock']:
        return jsonify({'success': False, 'message': f'Stock limit reached. Maximum available: {product["stock"]}'}), 400

    # Update or delete the cart item
    if new_quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = new_quantity

    db.session.commit()

    # Calculate total price and total items
    total_price = sum(item.quantity * next((p for p in products if p['id'] == item.product_id), {}).get('price', 0)
                      for item in CartItem.query.filter_by(user_id=current_user.id).all())
    total_items = sum(item.quantity for item in CartItem.query.filter_by(user_id=current_user.id).all())

    return jsonify({'success': True, 'new_quantity': cart_item.quantity, 'total_price': total_price, 'total_items': total_items})


@bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please log in to modify your cart.", "warning")
        return redirect(url_for('auth.login'))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
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


# Team 2 Merge

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items_db = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items_db:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('views.cart'))

    # Fetch products and calculate costs from cart
    cart_items = []
    subtotal = 0
    for cart_item in cart_items_db:
        product = next((p for p in PRODUCTS if p["id"] == cart_item.product_id), None)
        if product:
            cart_items.append({
                'id': cart_item.product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': cart_item.quantity
            })
            subtotal += product['price'] * cart_item.quantity

    shipping = subtotal
    tax = subtotal * 1
    total = subtotal + shipping + tax

    # Pass data to the template
    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=round(subtotal, 2),
        shipping=round(shipping, 2),
        tax=round(tax, 2),
        total=round(total, 2)
    )


@bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    user = current_user

    # Fetch the product ID and quantity from the cart
    cart_items_db = CartItem.query.filter_by(user_id=user.id).all()
    if not cart_items_db:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('views.checkout'))

    # Store created orders for refreshing later
    created_orders = []

    for cart_item in cart_items_db:
        # Fetch the product from the dummy data using product_id from the cart
        product = next((p for p in PRODUCTS if p["id"] == cart_item.product_id), None)
        if not product:
            flash(f"Product with ID {cart_item.product_id} not found.", 'danger')
            continue

        # Calculate total cost for the product
        total_cost = product['price'] * cart_item.quantity

        # Create a new order
        new_order = Order(
            user_id=user.id,
            product_id=cart_item.product_id,  # Add the correct product_id here
            address_line_1=user.address_line_1,
            state=user.state,
            city=user.city,
            pincode=user.pincode,
            total_cost=total_cost,
            status="Pending"
        )

        db.session.add(new_order)
        db.session.commit()  # Commit order immediately to get order ID
        db.session.refresh(new_order)  # Refresh to get the latest order ID

        created_orders.append(new_order)

        # Create an OrderItem entry for this order
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=total_cost,
            product_name=product['name'],
            product_image=product['image']
        )
        db.session.add(order_item)
        db.session.commit()  # Commit order item immediately
        db.session.refresh(order_item)  # Refresh order item

    # Clear the user's cart after order placement
    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    flash('Order(s) placed successfully and your cart has been emptied!', 'success')

    return redirect(url_for('views.my_orders'))


@bp.route('/my_orders')
@login_required
def my_orders():
    # Fetch all orders for the current user
    orders = (
        db.session.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )

    # Organizing data to group items under respective orders
    orders_data = []
    for order in orders:
        # Find the product associated with this order from the dummy product data
        product = next((p for p in PRODUCTS if p['id'] == order.product_id), None)
        
        # Fetch related OrderItem details
        order_items = db.session.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        
        total_quantity = sum(item.quantity for item in order_items)
        total_price = order.total_cost  # Ensure total_cost is stored in the Order model

        if product:
            orders_data.append({
                "order": order,
                "product": product,
                "total_quantity": total_quantity,
                "total_price": total_price
            })

    return render_template('my_orders.html', orders_data=orders_data)

@bp.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You can only cancel your own orders.', 'danger')
        return redirect(url_for('views.my_orders'))

    # Update the order status to 'Cancelled'
    order.status = 'Cancelled'
    db.session.commit()

    flash('Order has been cancelled successfully.', 'success')
    return redirect(url_for('views.my_orders'))
