from flask import Blueprint, jsonify
from models.audit_log import AuditLog
from utils.decorators import role_required
from flask_jwt_extended import jwt_required

auditor_bp = Blueprint('auditor', __name__)

@auditor_bp.route('/logs', methods=['GET'])
@jwt_required()
@role_required(['AUDITOR', 'ADMIN'])
def get_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return jsonify([{
        'id': log.id,
        'user_id': log.user_id,
        'action': log.action,
        'ip_address': log.ip_address,
        'timestamp': log.timestamp,
        'details': log.details
    } for log in logs]), 200
