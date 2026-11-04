"""
Auth Routes - Thin Controller cho Xác thực và Quản lý Tài khoản (Single Identity).
"""

from flask import Blueprint, request, jsonify, g
from services.api_auth import require_token
from services.auth_service import register_customer, authenticate_user, update_customer_profile

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    email = data.get('email', '')
    password = data.get('password', '')
    full_name = data.get('customer_name') or data.get('full_name') or ''
    phone = data.get('phone')
    ok, res, msg = register_customer(email, password, full_name, phone)
    return jsonify({'success': ok, 'message': msg, **res}), 200 if ok else 400


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    login_input = data.get('username') or data.get('email') or ''
    password = data.get('password', '')
    ok, payload, msg = authenticate_user(login_input, password)
    if not ok:
        return jsonify({'success': False, 'message': msg}), 401
    return jsonify({'success': True, **payload})


@auth_bp.route('/api/profile/update', methods=['PUT'])
def api_update_profile():
    err = require_token()
    if err: return err
    if g.api_account_type != 'customer':
        return jsonify({'success': False, 'message': 'Chỉ tài khoản khách hàng mới được cập nhật hồ sơ'}), 403

    data = request.get_json() or {}
    name = data.get('customer_name') or data.get('full_name') or ''
    old_pwd = data.get('old_password', '')
    new_pwd = data.get('new_password', '')
    ok, msg = update_customer_profile(g.api_user_id, name, old_pwd, new_pwd)
    return jsonify({'success': ok, 'message': msg, 'customer_name': name if ok else ''}), 200 if ok else 400
