from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Use a secure key in production
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
