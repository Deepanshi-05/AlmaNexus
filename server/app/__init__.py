from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('config.Config')  # Config class where you store your settings like DB URI

    CORS(app)  # Allow cross-origin requests
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    # Register blueprints here
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    
    @app.route('/')
    def home():
      return "🎉 Welcome to AlmaNexus API – Auth is working!"

    return app

