from flask import Blueprint, render_template, request, redirect, url_for, session
from app.db.database import DatabaseConnection
from datetime import datetime

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservation', methods=['GET', 'POST'])
def reservation_form():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    db = DatabaseConnection()
    with db.get_cursor() as cursor:
        cursor.execute('SELECT id, name FROM restaurants')
        restaurants = cursor.fetchall()
        
        if request.method == 'POST':
            restaurant_id = request.form['restaurant_id']
            reservation_time = request.form['reservation_time']
            party_size = request.form['party_size']
            
            cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
            user_id = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT id FROM tables 
                WHERE restaurant_id = ? AND capacity >= ? 
                AND id NOT IN (
                    SELECT table_id FROM reservations 
                    WHERE reservation_time = ? AND status != 'cancelled'
                )
                LIMIT 1
            ''', (restaurant_id, party_size, reservation_time))
            table = cursor.fetchone()
            
            if table:
                cursor.execute('''
                    INSERT INTO reservations (user_id, table_id, reservation_time, status)
                    VALUES (?, ?, ?, 'pending')
                ''', (user_id, table[0], reservation_time))
                return redirect(url_for('reservation.reservation_form'))
            
            return render_template('reservation.html', restaurants=restaurants, error='No available tables')
    
    return render_template('reservation.html', restaurants=restaurants)

@reservation_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    db = DatabaseConnection()
    with db.get_cursor() as cursor:
        # Fetch reservations
        cursor.execute('''
            SELECT r.id, u.username, t.table_number, r.reservation_time, r.status
            FROM reservations r
            JOIN users u ON r.user_id = u.id
            JOIN tables t ON r.table_id = t.id
        ''')
        reservations = cursor.fetchall()

        # Fetch restaurants
        cursor.execute('SELECT id, name, address FROM restaurants')
        restaurants = cursor.fetchall()

        # Fetch users
        cursor.execute('SELECT id, username, role, email FROM users')
        users = cursor.fetchall()

        # Fetch tables
        cursor.execute('SELECT id, restaurant_id, capacity, table_number FROM tables')
        tables = cursor.fetchall()
    
    return render_template('admin_dashboard.html', reservations=reservations, restaurants=restaurants, users=users, tables=tables)

@reservation_bp.route('/admin/add_restaurant', methods=['POST'])
def add_restaurant():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    name = request.form['name']
    address = request.form['address']
    
    db = DatabaseConnection()
    with db.get_cursor() as cursor:
        cursor.execute('INSERT INTO restaurants (name, address) VALUES (?, ?)', (name, address))
    
    return redirect(url_for('reservation.admin_dashboard'))

@reservation_bp.route('/admin/add_table', methods=['POST'])
def add_table():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    restaurant_id = request.form['restaurant_id']
    capacity = request.form['capacity']
    table_number = request.form['table_number']
    
    db = DatabaseConnection()
    with db.get_cursor() as cursor:
        cursor.execute('INSERT INTO tables (restaurant_id, capacity, table_number) VALUES (?, ?, ?)', 
                      (restaurant_id, capacity, table_number))
    
    return redirect(url_for('reservation.admin_dashboard'))
