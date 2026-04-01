from flask import Flask
from extensions import db, migrate, jwt
from flask_cors import CORS
from config import Config
from models.user import User
from models.role import Role
from models.audit_log import AuditLog, Session

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.admin import admin_bp
    from routes.auditor import auditor_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auditor_bp, url_prefix='/api/auditor')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
