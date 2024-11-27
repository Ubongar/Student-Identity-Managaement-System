from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector  # Using the correct MySQL connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something secure

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # MySQL server host
        user="root",  # Your MySQL username
        password="your_password",  # Your MySQL password
        database="StudentIdentityManagement"  # Name of your database 
    )

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Load user callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    connection.close()
    if user_data:
        return User(id=user_data[0], username=user_data[1], role=user_data[3])
    return None

@app.route('/')
def home():
    return render_template('login.html')

# Register Route (Optional)
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    The `register()` function is used to register users.
    """
    if request.method != 'POST':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Check if username exists
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        flash("Username already exists", 'danger')
        connection.close()
        return redirect(url_for('register'))

    password_hash = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                   (username, password_hash, role))
    connection.commit()
    connection.close()

    flash("Registration successful! Please log in.", 'success')
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route hit")  # This will print in the terminal
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data and check_password_hash(user_data[2], password):
            user = User(id=user_data[0], username=user_data[1], role=user_data[3])
            login_user(user)
            flash("Logged in successfully!", 'success')
            return redirect(url_for('dashboard'))

        flash("Invalid credentials", 'danger')
    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", 'success')
    return redirect(url_for('login'))

# Dashboard Route (Accessible after login)
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('student_dashboard'))

# Admin Dashboard Route
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("You do not have access to this page.", 'danger')
        return redirect(url_for('dashboard'))
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")  # Assuming you have a 'students' table
    students = cursor.fetchall()
    connection.close()

    return render_template('admin_dashboard.html', students=students)

# Student Dashboard Route
@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash("You do not have access to this page.", 'danger')
        return redirect(url_for('dashboard'))
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE user_id = %s", (current_user.id,))
    student_info = cursor.fetchone()
    connection.close()

    return render_template('student_dashboard.html', student=student_info)

# Add Student (Admin only)
@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        flash("You do not have access to this page.", 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        grade = request.form['grade']
        user_id = current_user.id

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, email, grade, user_id) VALUES (%s, %s, %s, %s)",
                       (name, email, grade, user_id))
        connection.commit()
        connection.close()

        flash("Student added successfully!", 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_student.html')

# Edit Student (Admin only)
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if current_user.role != 'admin':
        flash("You do not have access to this page.", 'danger')
        return redirect(url_for('dashboard'))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        grade = request.form['grade']

        cursor.execute("UPDATE students SET name = %s, email = %s, grade = %s WHERE id = %s",
                       (name, email, grade, id))
        connection.commit()
        connection.close()

        flash("Student information updated successfully!", 'success')
        return redirect(url_for('admin_dashboard'))

    connection.close()
    return render_template('edit_student.html', student=student)

# Delete Student (Admin only)
@app.route('/delete_student/<int:id>', methods=['GET'])
@login_required
def delete_student(id):
    if current_user.role != 'admin':
        flash("You do not have access to this page.", 'danger')
        return redirect(url_for('dashboard'))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    connection.commit()
    connection.close()

    flash("Student deleted successfully!", 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
