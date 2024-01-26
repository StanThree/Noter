#resources.py
from flask_restful import Resource, reqparse, fields, marshal_with
from models import Student, Class, Note
from datetime import datetime
from extensions import bcrypt, db, jwt

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

# Resource for a single student
class StudentResource(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.get(student_id)
        if student:
            return student
        else:
            return {'message': 'Student not found'}, 404
        
    @marshal_with(student_fields)
    def put(self, student_id):
        args = student_parser.parse_args()
        student = Student.query.get(student_id)
        if student:
            student.username = args['username'] if args['username'] else student.username
            student.email = args['email'] if args['email'] else student.email
            student.password_hash = args['password']  # Hash the password properly
            db.session.commit()
            return student
        else:
            return {'message': 'Student not found'}, 404

    def delete(self, student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {'message': 'Student deleted'}
        else:
            return {'message': 'Student not found'}, 404
    # Add methods for PUT and DELETE as needed

# Resource for student list
class StudentListResource(Resource):
    @marshal_with(student_fields)
    def post(self):
        args = student_parser.parse_args()
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
        
        student = Student(username=args['username'], email=args['email'], password_hash=hashed_password)
        db.session.add(student)
        db.session.commit()
        return student, 201

# Resource for a single class
class ClassResource(Resource):
    @marshal_with(class_fields)
    def get(self, class_id):
        _class = Class.query.get(class_id)
        if _class:
            return _class
        else:
            return {'message': 'Class not found'}, 404
        
    @marshal_with(class_fields)   
    def put(self, class_id):
        args = class_parser.parse_args()
        _class = Class.query.get(class_id)
        if _class:
            _class.class_name = args['class_name'] if args['class_name'] else _class.class_name
            _class.instructor = args['instructor'] if args['instructor'] else _class.instructor
            _class.room = args['room'] if args['room'] else _class.room
            _class.time = args['time'] if args['time'] else _class.time
            _class.semester = args['semester'] if args['semester'] else _class.semester
            db.session.commit()
            return _class
        else:
            return {'message': 'Class not found'}, 404

    def delete(self, class_id):
        _class = Class.query.get(class_id)
        if _class:
            db.session.delete(_class)
            db.session.commit()
            return {'message': 'Class deleted'}
        else:
            return {'message': 'Class not found'}, 404

# Resource for class list
class ClassListResource(Resource):
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

# Resource for a single note
class NoteResource(Resource):
    @marshal_with(note_fields)
    def get(self, note_id):
        note = Note.query.get(note_id)
        if note:
            return note
        else:
            return {'message': 'Note not found'}, 404

    @marshal_with(note_fields)
    def put(self, note_id):
        args = note_parser.parse_args()
        note = Note.query.get(note_id)
        if note:
            note.title = args['title'] if args['title'] else note.title
            note.content = args['content'] if args['content'] else note.content
            # Update class_id if you want to allow changing the note's class
            db.session.commit()
            return note
        else:
            return {'message': 'Note not found'}, 404

    def delete(self, note_id):
        note = Note.query.get(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return {'message': 'Note deleted'}
        else:
            return {'message': 'Note not found'}, 404

# Resource for note list
class NoteListResource(Resource):
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