from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from functools import wraps
from flask import jsonify

def generate_token(identity, role):
    """
    Creates a JWT access token containing user ID and role.
    Args:
        identity (int): User ID
        role (str): User role (e.g., 'student', 'alumni', 'admin')
    Returns:
        str: JWT access token
    """
    token = create_access_token(
        identity={"id": identity, "role": role},
        expires_delta=timedelta(days=1)
    )
    return token

def get_current_user_id():
    """
    Retrieves the current user's ID from JWT payload.
    Returns:
        int or None: User ID
    """
    identity = get_jwt_identity()
    return identity.get("id") if identity else None

def get_current_user_role():
    """
    Retrieves the current user's role from JWT payload.
    Returns:
        str or None: User role
    """
    identity = get_jwt_identity()
    return identity.get("role") if identity else None

def role_required(required_role):
    """
    Decorator to restrict route access to users with a specific role.
    Usage:
        @app.route('/admin')
        @role_required('admin')
        def admin_panel():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            role = get_current_user_role()
            if role != required_role:
                return jsonify({"error": f"Access denied: {required_role} only"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
