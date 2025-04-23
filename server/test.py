from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # This creates tables if models are defined
    print("PostgreSQL connected successfully! ✅")
