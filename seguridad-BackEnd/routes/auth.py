from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.role import Role
from models.audit_log import AuditLog
from utils.validators import validate_password
from utils.totp import generate_totp_secret, verify_totp, get_totp_uri
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
import random
from utils.mailer import send_otp_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify(msg="Missing required fields"), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify(msg="User or email already exists"), 400

    is_strong, msg = validate_password(password)
    if not is_strong:
        return jsonify(msg=msg), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    # Assign default role
    user_role = Role.query.filter_by(name='USER').first()
    if not user_role:
        user_role = Role(name='USER')
        db.session.add(user_role)
    
    new_user.roles.append(user_role)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(msg="User registered successfully"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    requested_role = data.get('role')

    user = User.query.filter_by(username=username).first()
    
    ip_address = request.remote_addr

    if not user or not user.check_password(password):
        log = AuditLog(user_id=user.id if user else None, action='LOGIN_FAILED', ip_address=ip_address, details=f"Fallido para: {username}")
        db.session.add(log)
        db.session.commit()
        return jsonify(msg="Credenciales incorrectas"), 401

    # Check if user has the requested role
    user_roles = [role.name for role in user.roles]
    if not user_roles:
        return jsonify(msg="El usuario no tiene ningún rol asignado"), 403
        
    if requested_role and requested_role not in user_roles:
        return jsonify(msg=f"Acceso denegado: El usuario no cuenta con el rol de {requested_role}"), 403

    if user.is_2fa_enabled:
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        user.otp_code = otp
        user.otp_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        db.session.commit()
        
        send_otp_email(user.email, otp)
        
        # Return a temporary token to proceed to 2FA verification
        temp_token = create_access_token(
            identity=str(user.id), 
            expires_delta=datetime.timedelta(minutes=10), 
            additional_claims={"is_2fa_pending": True, "selected_role": requested_role}
        )
        return jsonify(msg="2FA REQUIRED", temp_token=temp_token, is_2fa_enabled=True), 200
    
    # Successful login without 2FA
    primary_role = requested_role if requested_role else user_roles[0]
    access_token = create_access_token(identity=str(user.id), additional_claims={"roles": user_roles, "active_role": primary_role})
    
    # Create a session
    from models.audit_log import Session
    from flask import current_app
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['SESSION_TIMEOUT_MINUTES'])
    new_session = Session(
        user_id=user.id, 
        ip_address=ip_address, 
        expires_at=expires_at,
        login_obs="Inicio de sesión estándar"
    )
    db.session.add(new_session)
    
    log = AuditLog(user_id=user.id, action='LOGIN_SUCCESS', ip_address=ip_address, details=f"Iniciado como {primary_role}")
    db.session.add(log)
    db.session.commit()
    
    return jsonify(access_token=access_token, roles=user_roles, active_role=primary_role), 200

@auth_bp.route('/verify-2fa', methods=['POST'])
@jwt_required()
def verify_2fa():
    claims = get_jwt_identity() # This will be the user id
    if not claims:
        return jsonify(msg="Unauthorized"), 401
    
    data = request.get_json()
    token = data.get('token')
    
    user = User.query.get(int(claims))
    if not user:
        return jsonify(msg="User not found"), 404
    
    # Check OTP from database instead of TOTP
    if user.otp_code == token and user.otp_expiry > datetime.datetime.utcnow():
        # Clear used OTP
        user.otp_code = None
        user.otp_expiry = None
        db.session.commit()
        # Extract selected role from incoming token claims if possible
        import jwt
        from flask import current_app
        raw_token = request.headers.get('Authorization').split()[1]
        decoded = jwt.decode(raw_token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        requested_role = decoded.get('selected_role')

        user_roles = [role.name for role in user.roles]
        primary_role = requested_role if requested_role and requested_role in user_roles else user_roles[0]

        access_token = create_access_token(identity=str(user.id), additional_claims={"roles": user_roles, "active_role": primary_role})
        
        # Create a session
        from models.audit_log import Session
        from flask import current_app
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['SESSION_TIMEOUT_MINUTES'])
        new_session = Session(
            user_id=user.id, 
            ip_address=request.remote_addr,
            expires_at=expires_at,
            login_obs="Inicio de sesión con 2FA"
        )
        db.session.add(new_session)
        
        log = AuditLog(user_id=user.id, action='LOGIN_SUCCESS_2FA', ip_address=request.remote_addr, details=f"Iniciado como {primary_role}")
        db.session.add(log)
        db.session.commit()
        
        return jsonify(access_token=access_token, roles=user_roles, active_role=primary_role), 200
    
    log = AuditLog(user_id=user.id, action='LOGIN_FAILED_2FA', ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()
    
    return jsonify(msg="Invalid 2FA token"), 401

@auth_bp.route('/setup-2fa', methods=['POST'])
@jwt_required()
def setup_2fa():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if user.is_2fa_enabled:
        return jsonify(msg="2FA is already enabled"), 400
    
    secret = generate_totp_secret()
    user.totp_secret = secret
    db.session.commit()
    
    uri = get_totp_uri(user.username, secret)
    return jsonify(secret=secret, qr_uri=uri), 200

@auth_bp.route('/enable-2fa', methods=['POST'])
@jwt_required()
def enable_2fa():
    user_id = get_jwt_identity()
    data = request.get_json()
    token = data.get('token')
    
    user = User.query.get(int(user_id))
    if verify_totp(user.totp_secret, token):
        user.is_2fa_enabled = True
        db.session.commit()
        return jsonify(msg="2FA enabled successfully"), 200
    
    return jsonify(msg="Invalid token, failed to enable 2FA"), 400
