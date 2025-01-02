from flask import request, jsonify
from functools import wraps

def is_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        secret_key = request.args.get('key')  # Get the key from the URL
        if secret_key != 'Deenaja_512':  # Check if the key matches the predefined secret key
            return jsonify({'message': 'Unauthorized'}), 403  # Unauthorized if key is incorrect
        return f(*args, **kwargs)
    return wrapper

def is_delivery_person(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if the current user is a delivery person
        if not getattr(current_user, 'isDeliveryPerson', lambda: False)():
            return redirect(url_for('views.auth_error'))  # Redirect if not authorized
        return f(*args, **kwargs)
    return wrapper
