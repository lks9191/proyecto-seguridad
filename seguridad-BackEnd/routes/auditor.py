from flask import Blueprint, jsonify
from models.audit_log import AuditLog, Session
from utils.decorators import role_required
from flask_jwt_extended import jwt_required

auditor_bp = Blueprint('auditor', __name__)

@auditor_bp.route('/sessions', methods=['GET'])
@jwt_required()
@role_required(['AUDITOR', 'ADMIN'])
def get_active_sessions():
    active_sessions = Session.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': s.id,
        'username': s.user.username,
        'ip_address': s.ip_address,
        'created_at': s.created_at
    } for s in active_sessions]), 200

@auditor_bp.route('/sessions/history', methods=['GET'])
@jwt_required()
@role_required(['AUDITOR', 'ADMIN'])
def get_session_history():
    logs = AuditLog.query.filter(AuditLog.action.in_(['LOGIN_SUCCESS', 'LOGIN_SUCCESS_2FA', 'LOGOUT'])).order_by(AuditLog.timestamp.desc()).all()
    return jsonify([{
        'id': log.id,
        'username': log.user.username if log.user else 'Unknown',
        'action': log.action,
        'ip_address': log.ip_address,
        'timestamp': log.timestamp
    } for log in logs]), 200

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
