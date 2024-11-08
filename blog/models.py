from flask_login import UserMixin
from db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # One-to-One relationship with Author
    author = db.relationship('Author', backref='user', uselist=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(250), nullable=True)
    
    # ForeignKey to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # One-to-Many relationship with Blog
    blogs = db.relationship('Blog', backref='author', lazy=True)
    
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # ForeignKey to Author
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    content = db.Column(db.Text(), nullable=True)


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    # Establish a relationship with the Course model via the student_course association table
    courses = db.relationship('Course', secondary='student_course', back_populates='students')


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=True)
    # Establish a relationship with the Student model via the student_course association table
    students = db.relationship('Student', secondary='student_course', back_populates='courses')


# Join table to associate students and courses
student_course = db.Table(
    'student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)
