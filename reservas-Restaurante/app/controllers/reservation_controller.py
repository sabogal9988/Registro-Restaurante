from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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
                flash('Reservation made successfully!', 'success')  # Add success message
                return redirect(url_for('reservation.reservation_form'))
            
            return render_template('reservation.html', restaurants=restaurants, error='No available tables')
    
    return render_template('reservation.html', restaurants=restaurants)
