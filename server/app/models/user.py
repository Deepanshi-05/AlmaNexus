from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .. import db


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'  # Define the name of the table

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(100), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email address
    password_hash = db.Column(db.String(128), nullable=False)  # Password hash

    def set_password(self, password):
        """Hash the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the password is correct."""
        return bcrypt.check_password_hash(self.password_hash, password)