from flask import Flask, request, jsonify
from form import AddItemForm
from models import Product
from app import db  # Assuming your DB instance is in `app.py`

@app.route("/admin/api/additems", methods=['POST'])
def add_items():
    form = AddItemForm(meta={'csrf': False})  # Disable CSRF for API requests

    if not form.validate_on_submit():
        return jsonify({'message': 'Validation failed', 'errors': form.errors}), 400

    try:
        # Create a new product from form data
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            brand=form.brand.data,
            image=form.image.data if form.image.data else None
        )

        # Add to database
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
