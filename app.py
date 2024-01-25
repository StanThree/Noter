from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db  # Import db here
from resources import StudentResource, ClassResource, NoteResource  # Import resources

# Initialize the Flask application and Flask-RESTful API
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)

# Define your API endpoints (routes)
api.add_resource(StudentResource, '/students/<int:student_id>', endpoint='student')  # Student endpoints
api.add_resource(ClassResource, '/classes/<int:class_id>', endpoint='class')  # Class endpoints
api.add_resource(NoteResource, '/notes/<int:note_id>', endpoint='note')  # Note endpoints

# Define a simple route to test that your app is working
@app.route('/')
def hello():
    return 'Hello, Noter App!'

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
