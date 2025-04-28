from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, current_app
from app.models.user import UserFactory
from app.db.database import DatabaseConnection
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'favicon.ico')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = DatabaseConnection()
        with db.get_cursor() as cursor:
            cursor.execute('SELECT password, role FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
                session['username'] = username
                session['role'] = user[1]
                if user[1] == 'admin':
                    return redirect(url_for('reservation.admin_dashboard'))
                return redirect(url_for('reservation.reservation_form'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        
        try:
            UserFactory.create_user(role, username, email, password)
            return redirect(url_for('auth.login'))
        except:
            return render_template('register.html', error='Username already exists')
    
    return render_template('register.html')