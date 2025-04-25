from flask import Blueprint, request, jsonify, url_for
from app import db, mail
from app.models import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from ..utils.jwt_utils import generate_token

auth_bp = Blueprint('auth', __name__)

# Serializer for email verification token
s = URLSafeTimedSerializer('SECRET_KEY')  # Replace SECRET_KEY with your actual secret key

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')  # 🟡 Optional role field

    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    # Create a new user
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)

    # Save to DB
    db.session.add(new_user)
    db.session.commit()

    # Generate verification token
    token = s.dumps(email, salt='email-confirm')
    
    # Create verification link
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    
    # Send email
    send_confirmation_email(email, confirm_url)

    # Generate JWT Token (using generate_token utility)
    access_token = generate_token(new_user.id, new_user.role)

    return jsonify({"msg": "User registered successfully. Please check your email to verify your account.", "access_token": access_token}), 201

def send_confirmation_email(to, confirm_url):
    """Function to send the confirmation email"""
    msg = Message('Please Confirm Your Email Address',
                  sender='your-email@example.com',  # Replace with your email
                  recipients=[to])
    msg.body = f'Your confirmation link is: {confirm_url}'
    mail.send(msg)

@auth_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # Token valid for 1 hour
    except Exception as e:
        return jsonify({"msg": "The confirmation link is invalid or has expired."}), 400

    user = User.query.filter_by(email=email).first_or_404()

    if user.is_verified:
        return jsonify({"msg": "Your email has already been confirmed."}), 200

    user.is_verified = True
    db.session.commit()

    return jsonify({"msg": "Your email has been successfully confirmed!"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    if not user.is_verified:
        return jsonify({"msg": "Please verify your email first!"}), 403

    # Generate JWT Token (using generate_token utility)
    access_token = generate_token(user.id, user.role)

    return jsonify({"msg": "Login successful", "access_token": access_token}), 200


   