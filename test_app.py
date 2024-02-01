import unittest
from app import app, db
from models import Student

class BasicTests(unittest.TestCase):

    # Executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        # Use a separate test database URI if available
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_noter.db'  # Example URI
        self.app = app.test_client()

        # Setup application context here
        with app.app_context():
            db.create_all()

    # Executed after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test cases...
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_student(self):
        with app.app_context():
            student = Student(username="testuser", email="test@example.com", password_hash="hashedpwd")
            db.session.add(student)
            db.session.commit()
            added_student = Student.query.filter_by(username="testuser").first()
            self.assertIsNotNone(added_student)
            self.assertEqual(added_student.email, "test@example.com")

if __name__ == "__main__":
    unittest.main()
