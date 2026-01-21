from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
import os

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.locations import locations_bp
    from routes.bookings import bookings_bp
    from routes.reviews import reviews_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        from models import User
        admin = User.query.filter_by(email='admin@vcloak.com').first()
        if not admin:
            admin = User(
                email='admin@vcloak.com',
                name='Admin',
                role='admin',
                verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Default admin user created: admin@vcloak.com / admin123')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to vcloak API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'locations': '/api/locations',
                'bookings': '/api/bookings',
                'reviews': '/api/reviews',
                'admin': '/api/admin'
            }
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
