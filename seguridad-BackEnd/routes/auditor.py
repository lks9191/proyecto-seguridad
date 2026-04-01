from flask import Blueprint, jsonify
from models.audit_log import AuditLog, Session
from utils.decorators import role_required
from flask_jwt_extended import jwt_required
from routes.admin import check_and_close_expired_sessions

auditor_bp = Blueprint('auditor', __name__)

@auditor_bp.route('/sessions', methods=['GET'])
@jwt_required()
@role_required(['AUDITOR', 'ADMIN'])
def get_active_sessions():
    check_and_close_expired_sessions()
    active_sessions = Session.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': s.id,
        'username': s.user.carnet,
        'full_name': f"{s.user.names} {s.user.paternal_surname} {s.user.maternal_surname or ''}".strip(),
        'ip_address': s.ip_address,
        'login_at': s.login_at,
        'expires_at': s.expires_at
    } for s in active_sessions]), 200

@auditor_bp.route('/sessions/history', methods=['GET'])
@jwt_required()
@role_required(['AUDITOR', 'ADMIN'])
def get_session_history():
    check_and_close_expired_sessions()
    sessions = Session.query.order_by(Session.login_at.desc()).all()
    return jsonify([{
        'id': s.id,
        'username': s.user.carnet,
        'full_name': f"{s.user.names} {s.user.paternal_surname} {s.user.maternal_surname or ''}".strip(),
        'login_at': s.login_at,
        'login_obs': s.login_obs,
        'logout_at': s.logout_at,
        'logout_obs': s.logout_obs,
        'ip_address': s.ip_address,
        'is_active': s.is_active
    } for s in sessions]), 200

@auditor_bp.route('/logs', methods=['GET'])
@jwt_required()
@role_required(['AUDITOR', 'ADMIN'])
def get_logs():
    check_and_close_expired_sessions()
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return jsonify([{
        'id': log.id,
        'user_id': log.user_id,
        'username': log.user.carnet if log.user else 'SISTEMA',
        'action': log.action,
        'ip_address': log.ip_address,
        'timestamp': log.timestamp,
        'details': log.details
    } for log in logs]), 200
