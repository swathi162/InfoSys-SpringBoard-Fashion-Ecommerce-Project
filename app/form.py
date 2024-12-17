from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class AddItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Name is required.")])
    price = FloatField('Price', validators=[
        InputRequired(message="Price is required."),
        NumberRange(min=0, message="Price must be a positive number.")
    ])
    category = StringField('Category', validators=[DataRequired(message="Category is required.")])
    brand = StringField('Brand', validators=[DataRequired(message="Brand is required.")])
    image = FileField('Image (optional)')  # Optional field
