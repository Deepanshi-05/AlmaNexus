# app/routes/auth.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Registration logic here
    return 'Register route'

@auth_bp.route('/login', methods=['POST'])
def login():
    # Login logic here
    return 'Login route'

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return 'Register route'

