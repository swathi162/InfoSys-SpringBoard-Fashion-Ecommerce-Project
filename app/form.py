from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateTimeField, FileField
from wtforms.validators import DataRequired, InputRequired, NumberRange
from datetime import datetime

class AddItemForm(FlaskForm):
    """Form for adding items to the shop."""
    name = StringField('Name', validators=[DataRequired(message="Name is required.")])
    
    description = StringField('Description', validators=[DataRequired(message="Description is required.")])
    
    price = FloatField('Price', validators=[
        InputRequired(message="Price is required."),
        NumberRange(min=0, message="Price must be a positive number.")
    ])
    
    stock_quantity = IntegerField('Stock Quantity', validators=[
        InputRequired(message="Stock quantity is required."),
        NumberRange(min=0, message="Stock quantity must be a non-negative number.")
    ])
    
    brand = StringField('Brand', validators=[DataRequired(message="Brand is required.")])
    
    category = StringField('Category', validators=[DataRequired(message="Category is required.")])
    
    updated_at = DateTimeField('Updated At', default=datetime.utcnow)  # Optional, auto-populates with current time
    
    rating = FloatField('Rating', validators=[
        NumberRange(min=0, max=5, message="Rating must be between 0 and 5.")
    ])
    
    ratting = StringField('Ratting', validators=[DataRequired(message="Ratting is required.")])
