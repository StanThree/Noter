from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db  # Import db here
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

# Define your API endpoints (routes)

# Student endpoints
api.add_resource(StudentResource, '/students/<int:student_id>')  # For specific student operations
api.add_resource(StudentListResource, '/students')  # For creating new students

# Class endpoints
api.add_resource(ClassResource, '/classes/<int:class_id>')  # For specific class operations
api.add_resource(ClassListResource, '/classes')  # For creating new classes

# Note endpoints
api.add_resource(NoteResource, '/notes/<int:note_id>')  # For specific note operations
api.add_resource(NoteListResource, '/notes')  # For creating new notes

# Define a simple route to test that your app is working
@app.route('/')
def hello():
    return 'Hello, Noter App!'

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
