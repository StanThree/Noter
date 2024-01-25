# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize the SQLAlchemy instance here

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Relationships
    classes = db.relationship('Class', secondary='student_classes', backref='students', lazy='dynamic')
    notes = db.relationship('Note', secondary='student_notes', backref='students', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.username}>'

class Class(db.Model):
    __tablename__ = 'classes'
    
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    instructor = db.Column(db.String(100))
    room = db.Column(db.String(100))
    time = db.Column(db.String(100))
    semester = db.Column(db.String(50))

    # Relationship
    notes = db.relationship('Note', backref='class', lazy='dynamic')

    def __repr__(self):
        return f'<Class {self.class_name}>'

class Note(db.Model):
    __tablename__ = 'notes'
    
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))

    def __repr__(self):
        return f'<Note {self.title}>'

student_classes = db.Table('student_classes',
    db.Column('student_id', db.Integer, db.ForeignKey('students.student_id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.class_id'), primary_key=True),
    db.Column('enrolled_date', db.DateTime, default=db.func.current_timestamp())
)

student_notes = db.Table('student_notes',
    db.Column('student_id', db.Integer, db.ForeignKey('students.student_id'), primary_key=True),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.note_id'), primary_key=True),
    db.Column('contribution_date', db.DateTime, default=db.func.current_timestamp())
)
