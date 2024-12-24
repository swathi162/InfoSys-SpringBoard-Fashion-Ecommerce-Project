from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# User Registration Form
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=80)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=120)])
    role = SelectField('Role', choices=[('delivery', 'Delivery'), ('user', 'User')], validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# User Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Update User Information Form
class UpdateUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=80)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=80)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=120)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=10)])
    submit = SubmitField('Update')

# Password Reset Form
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# Forget Password Form
class ForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')