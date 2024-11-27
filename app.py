from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database connection using mysql-connector
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NewSecurePassword",  
        database="studentidentitymanagement"  
    )

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    db.close()
    if user_data:
        return User(id=user_data[0], username=user_data[1], role=user_data[2])
    return None

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        flash("Username already exists.", 'danger')
        return redirect(url_for('register'))
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", 
                (username, hashed_password, role))
    db.commit()
    db.close()
    flash("Registration successful! Please log in.", 'success')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        try:
            cursor = db.cursor()
            
            cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = %s", (username,))
            user_data = cursor.fetchone()
        finally:
            db.close()

        if user_data and check_password_hash(user_data[2], password):
            # Create a User object and log the user in
            user = User(id=user_data[0], username=user_data[1], role=user_data[3])
            login_user(user)
            flash("Logged in successfully!", 'success')
            return redirect(url_for('dashboard'))
        
        # Flash a message if login fails
        flash("Invalid username or password.", 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('student_dashboard'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied.", 'danger')
        return redirect(url_for('dashboard'))
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    db.close()
    return render_template('admin_dashboard.html', students=students)

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash("Access denied.", 'danger')
        return redirect(url_for('dashboard'))
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE user_id = %s", (current_user.id,))
    student = cursor.fetchone()
    db.close()
    return render_template('student_dashboard.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
