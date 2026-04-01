from flask import Blueprint, jsonify, request
from extensions import db
from models.user import User
from models.role import Role
from models.audit_log import Session, AuditLog
from utils.decorators import role_required
from utils.validators import validate_password
from flask_jwt_extended import jwt_required

import datetime
admin_bp = Blueprint('admin', __name__)

def check_and_close_expired_sessions():
    now = datetime.datetime.utcnow()
    expired = Session.query.filter(Session.is_active == True, Session.expires_at < now).all()
    for s in expired:
        s.is_active = False
        s.logout_at = s.expires_at
        s.logout_obs = "Expiración de sesión / Inactividad / Cierre inesperado"
    if expired:
        db.session.commit()

@admin_bp.route('/sessions', methods=['GET'])
@jwt_required()
@role_required(['ADMIN'])
def get_active_sessions():
    check_and_close_expired_sessions()
    active_sessions = Session.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': s.id,
        'username': s.user.username,
        'ip_address': s.ip_address,
        'login_at': s.login_at,
        'login_obs': s.login_obs,
        'expires_at': s.expires_at
    } for s in active_sessions]), 200

@admin_bp.route('/sessions/history', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'AUDITOR'])
def get_session_history():
    check_and_close_expired_sessions()
    sessions = Session.query.order_by(Session.login_at.desc()).all()
    return jsonify([{
        'id': s.id,
        'username': s.user.username,
        'login_at': s.login_at,
        'login_obs': s.login_obs,
        'logout_at': s.logout_at,
        'logout_obs': s.logout_obs,
        'ip_address': s.ip_address,
        'is_active': s.is_active
    } for s in sessions]), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['ADMIN'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'roles': [role.name for role in user.roles]
    } for user in users]), 200

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    roles_list = data.get('roles', ['USER']) # Default to USER role

    if not username or not email or not password:
        return jsonify(msg="Missing required fields"), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify(msg="User or email already exists"), 400

    is_strong, msg = validate_password(password)
    if not is_strong:
        return jsonify(msg=msg), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    for role_name in roles_list:
        role = Role.query.filter_by(name=role_name).first()
        if role:
            new_user.roles.append(role)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(msg=f"User {username} created successfully"), 201

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="User not found"), 404
        
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    roles_list = data.get('roles')
    
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        is_strong, msg = validate_password(password)
        if not is_strong:
            return jsonify(msg=msg), 400
        user.set_password(password)
    
    if roles_list is not None:
        user.roles = []
        for role_name in roles_list:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user.roles.append(role)
                
    db.session.commit()
    return jsonify(msg=f"User {user.username} updated successfully"), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="User not found"), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify(msg=f"User {user.username} deleted"), 200

@admin_bp.route('/roles', methods=['GET'])
@jwt_required()
@role_required(['ADMIN'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in roles]), 200

@admin_bp.route('/roles', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_role():
    data = request.get_json()
    role_name = data.get('name')
    if not role_name:
        return jsonify(msg="Role name is required"), 400
    
    if Role.query.filter_by(name=role_name).first():
        return jsonify(msg="Role already exists"), 400
    
    new_role = Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()
    return jsonify(msg=f"Role {role_name} created"), 201

@admin_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN'])
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify(msg="Role not found"), 404
        
    data = request.get_json()
    new_name = data.get('name')
    if not new_name:
        return jsonify(msg="Role name is required"), 400
        
    if Role.query.filter(Role.name == new_name, Role.id != role_id).first():
        return jsonify(msg="Role name already exists"), 400
        
    role.name = new_name
    db.session.commit()
    return jsonify(msg=f"Role updated to {new_name}"), 200

@admin_bp.route('/assign-role', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def assign_role():
    data = request.get_json()
    user_id = data.get('user_id')
    role_name = data.get('role')
    
    user = User.query.get(user_id)
    role = Role.query.filter_by(name=role_name).first()
    
    if not user or not role:
        return jsonify(msg="User or Role not found"), 404
    
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
    
    return jsonify(msg=f"Role {role_name} assigned to user {user.username}"), 200

@admin_bp.route('/remove-role', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def remove_role():
    data = request.get_json()
    user_id = data.get('user_id')
    role_name = data.get('role')
    
    user = User.query.get(user_id)
    role = Role.query.filter_by(name=role_name).first()
    
    if not user or not role:
        return jsonify(msg="User or Role not found"), 404
    
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
    
    return jsonify(msg=f"Role {role_name} removed from user {user.username}"), 200
