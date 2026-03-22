from flask import Blueprint, jsonify, request
from extensions import db
from models.user import User
from models.role import Role
from utils.decorators import role_required
from flask_jwt_extended import jwt_required

admin_bp = Blueprint('admin', __name__)

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
