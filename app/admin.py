from flask import Blueprint, render_template, get_flashed_messages, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, User
from .decorators import is_admin

bp = Blueprint('admin', __name__)


@bp.route('/admin/approveDelivery')
@login_required
@is_admin
def approve_delivery():

    delivery_user_request = User.query.filter_by(role='delivery', approved = False).all()

    get_flashed_messages()
    

    return redirect(url_for('views.home'))


@bp.route('/admin/make_me_admin')
@login_required
def make_me_admin():
    if not current_user.isAdmin():
        current_user.role = 'admin'
        db.session.commit()
    return redirect(url_for('views.home'))