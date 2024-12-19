from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User
from . import views, auth, admin


# Initialize extensions
db = models.db
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.secret_key = "Infosys-Springboard-5.0"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(admin.admin, url_prefix='/admin')

    # Create tables
    with app.app_context():
        db.create_all()

    return app



#  # Register blueprints
#     app.register_blueprint(auth.bp, url_prefix='/auth')
#     app.register_blueprint(views.bp, url_prefix='/')
#     app.register_blueprint(admin.admin, url_prefix='/admin')