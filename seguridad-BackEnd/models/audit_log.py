from extensions import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False) # e.g., 'LOGIN_SUCCESS', 'LOGIN_FAILED', 'ACCESS_DENIED'
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('audit_logs', cascade="all, delete-orphan", lazy=True))

    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id} at {self.timestamp}>'

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45))
    login_at = db.Column(db.DateTime, default=datetime.utcnow)
    login_obs = db.Column(db.String(255))
    logout_at = db.Column(db.DateTime)
    logout_obs = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref=db.backref('sessions', cascade="all, delete-orphan", lazy=True))

    def __repr__(self):
        return f'<Session {self.id} for user {self.user_id}>'
