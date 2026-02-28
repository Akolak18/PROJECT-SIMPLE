"""ReplyFast AI — application factory."""
import os
from flask import Flask
from extensions import db, login_manager
from config import config


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from blueprints.main import bp as main_bp
    from blueprints.auth import bp as auth_bp
    from blueprints.dashboard import bp as dashboard_bp
    from blueprints.billing import bp as billing_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(billing_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
