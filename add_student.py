# add_student.py
from app import app, db
from models import Student

if __name__ == '__main__':
    with app.app_context():
        new_student = Student(username='student1', email='student1@example.com', password_hash='thethousandhash')
        db.session.add(new_student)
        db.session.commit()
