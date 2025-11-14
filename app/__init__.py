import os
import sys
from flask import Flask

def create_app():
    """Create and configure Flask application"""
    
    # Get absolute paths
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    # Create Flask app with correct paths
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-2025')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Server error'}, 500
    
    return app
