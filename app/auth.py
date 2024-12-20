from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from sqlalchemy.exc import IntegrityError
from .methods import send_token_email
from itsdangerous import SignatureExpired
from app import URL_SERIALIZER

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        address = request.form.get('address')
        role = request.form.get('role')
        pincode = request.form.get('pincode')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(password=hashed_password, email=email, address=address, role=role, pincode=pincode, firstname=firstname, lastname=lastname)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully.', 'success')
            return redirect(url_for('auth.login'))
        
        except IntegrityError :
            flash('Email already exists.', 'danger')

        except Exception as e:
            print(e)
            flash(f'An error occurred!', 'danger')

    return render_template('signup.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@bp.route("/forgetpassword", methods = ["GET", "POST"])
def forgetpassword():
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            
            token = URL_SERIALIZER.dumps(email, salt='email-confirm')

            reset_link = url_for('auth.reset_password', token = token, _external = True)
            try:
                send_token_email(email, user.firstname, reset_link)
            except Exception as e:
                pass

            flash('Password reset link sent to your email.', 'success')
        else:
            flash('Invalid email.', 'danger')
            
    return render_template("forgetpassword.html")
    

@bp.route("/reset-password/<token>", methods = ["GET", "POST"])
def reset_password(token):

    if request.method == "GET":
        return render_template('reset_password.html')
    
    if request.method == "POST":

        try:
            email = URL_SERIALIZER.loads(token, salt='email-confirm', max_age =3600)
        except SignatureExpired:
            return '<h1>The token is Expired!</h1>'
        
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        user = User.query.filter_by(email = email).first()

        user.password = hashed_password

        db.session.commit()

        flash('Your password has been updated successfully!', 'success')
        return redirect(url_for('auth.login'))