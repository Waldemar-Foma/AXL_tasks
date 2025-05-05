from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @app.context_processor
    def inject_common_vars():
        return {
            'now': datetime.utcnow(),
            'theme': request.cookies.get('theme', 'light') + '_theme.css'
        }
    
    from app.auth.routes import auth_bp
    from app.projects.routes import projects_bp
    from app.tasks.routes import tasks_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    with app.app_context():
        db.create_all()
    
    return app