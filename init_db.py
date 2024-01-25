# init_db.py
from app import app, db  # Import the app instance directly
from models import Student  # import all other models

# No need to call create_app since we're importing the app instance directly

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
