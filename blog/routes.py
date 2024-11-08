from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from blog.models import User, db, Blog, Author, Course, Student, student_course
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.orm import joinedload

blog_blueprint = Blueprint('blog_blueprint', '__name__', url_prefix='/blog')
blog = blog_blueprint

  
@blog.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog_blueprint.index'))
    
    if request.method == 'POST':
        name = request.form.get('name').strip()
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        user = User(name=name, username=username, password=password)
        # Add the user to the database
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registration successful!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Username might already be taken.', 'error')
            return redirect(url_for('blog_blueprint.register'))
        
        return redirect(url_for('blog_blueprint.login'))
        
    else:
        return render_template('auth/register.html')
    
@blog.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog_blueprint.index'))
    
    if request.method == 'POST':     
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        user = User.query.filter_by(username=username).first()
        
        if user.password == password:
            # Use the login_user method to log in the user
            login_user(user)
            return redirect('/blog')
        else:
            flash('Login failed. Password Invalid.', 'error')
            return redirect(url_for('blog_blueprint.login'))
    else:
        return render_template('auth/login.html')
    
@blog.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog_blueprint.index'))


@blog.route('/', methods=['GET', 'POST'])
# @login_required  # Protect this route with the login_required decorator
def index():
    # alternate ways
    if not current_user.is_authenticated:
        return redirect(url_for('blog_blueprint.login'))
    if request.method=='POST':
        auther_id = request.form.get('auther')
        content = request.form.get('content')
        
        new_blog = Blog(author_id=auther_id, content=content)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('blog_blueprint.index'))
    
    # users = User.query.all()
    # blogs = Blog.query.all()
    blogs = db.session.query(Blog).all()
    users = db.session.query(User).all()
    auther = db.session.query(Author).all()
    # auther.user.name
    
    return render_template('blog/blog.html', Blogs=blogs, users=users, auther=auther)


@blog.route('/update/<int:id>/', methods=['GET','POST'])
def update_blog(id):
    blog = Blog.query.get_or_404(id)
    if request.method == 'POST':
        blog.author_id = request.form.get('auther')
        blog.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('blog_blueprint.index'))
    auther = db.session.query(Author).all()
    return render_template('blog/blog_update.html', auther=auther, blog=blog)    

@blog.route('/delete/<int:id>/')
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blog_blueprint.index'))


@blog.route('/auther', methods=['GET', 'POST'])
@login_required  # Protect this route with the login_required decorator
def auther():
    # alternate ways
    if not current_user.is_authenticated:
        return redirect(url_for('blog_blueprint.login'))
    if request.method=='POST':
        user_id = request.form.get('user')
        bio = request.form.get('bio')
        
        new_author = Author(user_id=user_id, bio=bio)
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('blog_blueprint.index'))

    users = db.session.query(User).all()
    auther = db.session.query(Author).all()
    # auther.user.name
    return render_template('blog/auther.html', Authers=auther, users=users)

@blog.route('/update/auther/<int:id>/', methods=['POST','GET'])
def update_auther(id):
    auther = Author.query.get_or_404(id)
    if request.method == 'POST':
        auther.user_id=request.form.get('user')
        auther.bio=request.form.get('bio')
        db.session.commit()
        return redirect(url_for('blog_blueprint.auther'))
    
    users=db.session.query(User).all()
    return render_template('blog/auther_update.html', auther=auther, users=users) 

@blog.route('/delete/auther/<int:id>/')
def delete_auther(id):
    auther = Author.query.get_or_404(id)
    db.session.delete(auther)
    db.session.commit()
    return redirect(url_for('blog_blueprint.auther'))



# many to many relationship examples ---+>

@blog.route('/course', methods=['GET', 'POST'])
def course():
        # Create instances of 5 courses
    course1 = Course(course_name="Mathematics")
    course2 = Course(course_name="Science")
    course3 = Course(course_name="History")
    course4 = Course(course_name="Literature")
    course5 = Course(course_name="Computer Science")

    # Add courses to the session
    db.session.add_all([course1, course2, course3, course4, course5])
    db.session.commit()

    return "course created successfully"

@blog.route('/view/courses', methods=['GET'])
def get_courses():
    # Query all courses from the database
    courses = Course.query.all()

    # Convert the courses to a list of dictionaries to make them JSON serializable
    courses_list = [{"id": course.id, "course_name": course.course_name} for course in courses]

    # Return the list of courses as a JSON response
    return jsonify(courses_list)

@blog.route('/student', methods=['GET'])
def student():
    
    course1 = Course.query.get_or_404(1)
    course2 = Course.query.get_or_404(2)
    course3 = Course.query.get_or_404(3)
    course4 = Course.query.get_or_404(4)
    course5 = Course.query.get_or_404(5)

    
    student1 = Student(name="Alice")
    student2 = Student(name="Bob")
    student3 = Student(name="Charlie")
    student4 = Student(name="David")
    student5 = Student(name="Eve")

    # Associate students with courses (many-to-many relationship)
    # Each student will take some courses. Here, I am assigning random courses to students.

    student1.courses = [course1, course2]
    student2.courses = [course2, course3]
    student3.courses = [course3, course4]
    student4.courses = [course4, course5]
    student5.courses = [course1, course5]

    # Add students to the session
    db.session.add_all([student1, student2, student3, student4, student5])
    db.session.commit()

    return "student created successfully"

@blog.route('/view/students', methods=['GET'])
def get_students():
    # Query all students and eagerly load their associated courses
    students = Student.query.options(joinedload(Student.courses)).all()
    
    # Convert students to a list of dictionaries, including courses
    students_list = [
        {
            "id": student.id,
            "name": student.name,
            "courses": [{"id": course.id, "course_name": course.course_name} for course in student.courses]
        }
        for student in students
    ]

    # Return the list of students with courses as a JSON response
    return jsonify(students_list), 200


@blog.route('/remove/course/from/student/<student_id>/<int:course_id>/', methods=['GET'])
def remove_course_from_student(student_id, course_id):
    # Find the student by ID
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Find the course by ID
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    # Check if the student is enrolled in the course
    if course not in student.courses:
        return jsonify({"message": "Student is not enrolled in this course"}), 400

    # Remove the course from the student's list of courses
    student.courses.remove(course)

    # Commit the transaction to the database
    db.session.commit()

    return jsonify({"message": "Course removed from student successfully"}), 200