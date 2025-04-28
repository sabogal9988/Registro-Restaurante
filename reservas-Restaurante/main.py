from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.reservation_controller import reservation_bp
from app.db.database import init_db

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your-secret-key'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(reservation_bp)

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True)