#app.py
import os
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from extensions import db, bcrypt, jwt
from config import Config
from models import Student
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from resources import (
    StudentResource, StudentListResource,  # Import student resources
    ClassResource, ClassListResource,  # Import class resources
    NoteResource, NoteListResource  # Import note resources
)

# Initialize the Flask application and Flask-RESTful API
app = Flask(__name__)
app.config.from_object(Config)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback_secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Set to False if you don't want the token to expire

api = Api(app)
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

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
        # Login successful, create a new token
        access_token = create_access_token(identity=student.student_id)
        return jsonify(access_token=access_token), 200
    else:
        # Login failed
        return jsonify({"message": "Invalid username or password"}), 401

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

# Define a simple route to test that your app is working
@app.route('/')
def hello():
    return 'Hello, Noter App!'

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
