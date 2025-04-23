from flask import Blueprint, request, jsonify
from app import db 
from app.models import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Add to the database
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT Token
    access_token = create_access_token(identity=new_user.id)

    return jsonify({"msg": "User registered successfully", "access_token": access_token}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Generate JWT Token
    access_token = create_access_token(identity=user.id)

    return jsonify({"msg": "Login successful", "access_token": access_token}), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    from flask_jwt_extended import get_jwt_identity

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify({"username": user.username, "email": user.email})


