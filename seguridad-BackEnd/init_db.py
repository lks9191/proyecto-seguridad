from app import create_app
from extensions import db
from models.role import Role
from models.user import User

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default roles
        roles = ['USER', 'ADMIN', 'AUDITOR']
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
