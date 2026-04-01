from extensions import db
from datetime import datetime
import bcrypt

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    carnet = db.Column(db.String(20), unique=True, nullable=False)
    names = db.Column(db.String(100), nullable=False)
    paternal_surname = db.Column(db.String(100), nullable=False)
    maternal_surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    totp_secret = db.Column(db.String(32))
    otp_code = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)
    is_2fa_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.carnet}>'
