from flask import Blueprint, jsonify, request
from extensions import db
from models.user import User
from models.audit_log import Session, AuditLog
import random
import datetime
from utils.mailer import send_otp_email
from utils.validators import validate_password
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if not user:
        return jsonify(msg="User not found"), 404
        
    return jsonify(
        username=user.username,
        email=user.email,
        roles=[role.name for role in user.roles],
        is_2fa_enabled=user.is_2fa_enabled,
        created_at=user.created_at
    ), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    data = request.get_json()
    
    if not user:
        return jsonify(msg="User not found"), 404
        
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        is_strong, msg = validate_password(password)
        if not is_strong:
            return jsonify(msg=msg), 400
        user.set_password(password)
        
    db.session.commit()
    
    log = AuditLog(user_id=user.id, action='PROFILE_UPDATE', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()
    
    return jsonify(msg="Profile updated successfully"), 200

@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    # Mask session as inactive
    active_session = Session.query.filter_by(user_id=int(user_id), is_active=True).first()
    if active_session:
        active_session.is_active = False
        db.session.commit()
    
    log = AuditLog(user_id=int(user_id), action='LOGOUT', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()
    
    return jsonify(msg="Logged out successfully"), 200

@user_bp.route('/request-2fa', methods=['POST'])
@jwt_required()
def request_2fa():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    user.otp_code = otp
    user.otp_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    db.session.commit()
    
    if send_otp_email(user.email, otp):
        return jsonify(msg="Código enviado a tu correo"), 200
    return jsonify(msg="Error al enviar el correo"), 500

@user_bp.route('/confirm-2fa', methods=['POST'])
@jwt_required()
def confirm_2fa():
    user_id = get_jwt_identity()
    data = request.get_json()
    token = data.get('token')
    
    user = User.query.get(int(user_id))
    
    if user.otp_code == token and user.otp_expiry > datetime.datetime.utcnow():
        user.is_2fa_enabled = True
        user.otp_code = None
        user.otp_expiry = None
        db.session.commit()
        
        log = AuditLog(user_id=user.id, action='2FA_ENABLED', ip_address=request.remote_addr)
        db.session.add(log)
        db.session.commit()
        
        return jsonify(msg="2FA activado con éxito"), 200
    
    return jsonify(msg="Código inválido o expirado"), 400

@user_bp.route('/disable-2fa', methods=['POST'])
@jwt_required()
def disable_2fa():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    user.is_2fa_enabled = False
    db.session.commit()
    
    log = AuditLog(user_id=user.id, action='2FA_DISABLED', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()
    
    return jsonify(msg="2FA desactivado"), 200
