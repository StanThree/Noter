from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, Student, Class, Note
from datetime import datetime

# Request parsers
student_parser = reqparse.RequestParser()
student_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
student_parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
student_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

class_parser = reqparse.RequestParser()
class_parser.add_argument('class_name', type=str, required=True, help='Class name cannot be blank')
class_parser.add_argument('instructor', type=str)
class_parser.add_argument('room', type=str)
class_parser.add_argument('time', type=str)
class_parser.add_argument('semester', type=str)

note_parser = reqparse.RequestParser()
note_parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
note_parser.add_argument('content', type=str, required=True, help='Content cannot be blank')
note_parser.add_argument('class_id', type=int, required=True, help='Class ID cannot be blank')

# Response fields
student_fields = {
    'student_id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class_fields = {
    'class_id': fields.Integer,
    'class_name': fields.String,
    'instructor': fields.String,
    'room': fields.String,
    'time': fields.String,
    'semester': fields.String
}

note_fields = {
    'note_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'date_created': fields.DateTime,
    'last_modified': fields.DateTime,
    'class_id': fields.Integer
}

class StudentResource(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.get(student_id)
        if student:
            return student
        else:
            return {'message': 'Student not found'}, 404

    @marshal_with(student_fields)
    def post(self):
        args = student_parser.parse_args()
        student = Student(username=args['username'], email=args['email'], password_hash=args['password'])  # Hash password properly
        db.session.add(student)
        db.session.commit()
        return student, 201

    # Add methods for PUT and DELETE as needed

class ClassResource(Resource):
    @marshal_with(class_fields)
    def get(self, class_id):
        _class = Class.query.get(class_id)
        if _class:
            return _class
        else:
            return {'message': 'Class not found'}, 404

    @marshal_with(class_fields)
    def post(self):
        args = class_parser.parse_args()
        _class = Class(
            class_name=args['class_name'],
            instructor=args['instructor'],
            room=args['room'],
            time=args['time'],
            semester=args['semester']
        )
        db.session.add(_class)
        db.session.commit()
        return _class, 201

    # Add methods for PUT and DELETE as needed

class NoteResource(Resource):
    @marshal_with(note_fields)
    def get(self, note_id):
        note = Note.query.get(note_id)
        if note:
            return note
        else:
            return {'message': 'Note not found'}, 404

    @marshal_with(note_fields)
    def post(self):
        args = note_parser.parse_args()
        note = Note(
            title=args['title'],
            content=args['content'],
            class_id=args['class_id'],
            date_created=datetime.now(),
            last_modified=datetime.now()
        )
        db.session.add(note)
        db.session.commit()
        return note, 201

    # Add methods for PUT and DELETE as needed
