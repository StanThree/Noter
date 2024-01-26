from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from models import db, Student  # Import db and Student model
from resources import (
    StudentResource, StudentListResource,  # Import student resources
    ClassResource, ClassListResource,  # Import class resources
    NoteResource, NoteListResource  # Import note resources
)

# Initialize the Flask application and Flask-RESTful API
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Define your API endpoints (routes)
api.add_resource(StudentResource, '/students/<int:student_id>')  # For specific student operations
api.add_resource(StudentListResource, '/students')  # For creating new students
api.add_resource(ClassResource, '/classes/<int:class_id>')  # For specific class operations
api.add_resource(ClassListResource, '/classes')  # For creating new classes
api.add_resource(NoteResource, '/notes/<int:note_id>')  # For specific note operations
api.add_resource(NoteListResource, '/notes')  # For creating new notes

# Login route
@app.route('/login', methods=['POST'])
def login():
    args = request.get_json()
    student = Student.query.filter_by(username=args['username']).first()

    if student and bcrypt.check_password_hash(student.password_hash, args['password']):
        # Login successful
        return jsonify({"message": "Login successful"}), 200
    else:
        # Login failed
        return jsonify({"message": "Invalid username or password"}), 401

# Define a simple route to test that your app is working
@app.route('/')
def hello():
    return 'Hello, Noter App!'

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
