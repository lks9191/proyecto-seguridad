from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

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
