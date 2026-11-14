from flask import Blueprint, request, jsonify, g
from database import get_db_connection
from services.api_auth import require_token
from services.booking_service import get_user_role_from_db

admin_bp = Blueprint('admin_bp', __name__)


# ─── USER MANAGEMENT ENDPOINTS ───────────────────────────────────────────────

@admin_bp.route('/api/users', methods=['GET'])
def api_get_users():
    auth_err = require_token()
    if auth_err is not None:
        return auth_err
    caller_role = get_user_role_from_db(g.api_user_id, g.api_account_type or 'staff')
    if caller_role != 'Admin':
        return jsonify({'success': False, 'message': 'Khong co quyen'}), 403
    
    user_type = request.args.get('type', 'staff').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if user_type == 'staff':
        cursor.execute("""
            SELECT a.account_id AS user_id, 
                   sp.username, 
                   a.email, 
                   sp.full_name, 
                   a.created_at,
                   a.is_active,
                   COALESCE(r.role_name, 'Staff') AS roles,
                   'staff' AS account_type
            FROM Staff_Profiles sp
            JOIN Accounts a ON sp.account_id = a.account_id
            LEFT JOIN Roles r ON sp.role_id = r.role_id
            ORDER BY sp.role_id ASC, a.account_id ASC
        """)
    elif user_type == 'customer':
        cursor.execute("""
            SELECT a.account_id AS user_id, 
                   COALESCE(NULLIF(cp.phone, ''), a.email) AS username, 
                   a.email, 
                   cp.full_name, 
                   a.created_at,
                   a.is_active,
                   'Guest' AS roles,
                   'customer' AS account_type
            FROM Customer_Profiles cp
            JOIN Accounts a ON cp.account_id = a.account_id
            ORDER BY a.account_id DESC
            LIMIT 100
        """)
    else: # all
        cursor.execute("""
            SELECT a.account_id AS user_id, 
                   COALESCE(sp.username, NULLIF(cp.phone, ''), a.email) AS username, 
                   a.email, 
                   COALESCE(sp.full_name, cp.full_name, 'Khách hàng') AS full_name, 
                   a.created_at,
                   a.is_active,
                   COALESCE(r.role_name, 'Guest') AS roles,
                   a.account_type
            FROM Accounts a
            LEFT JOIN Staff_Profiles sp ON a.account_id = sp.account_id
            LEFT JOIN Customer_Profiles cp ON a.account_id = cp.account_id
            LEFT JOIN Roles r ON sp.role_id = r.role_id
            ORDER BY CASE WHEN a.account_type = 'staff' THEN 0 ELSE 1 END, a.account_id ASC
            LIMIT 100
        """)
    
    users_list = [dict(r) for r in cursor.fetchall()]

    # Thống kê tổng quan nhân sự
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT sp.account_id) AS total_staff,
            SUM(CASE WHEN r.role_name = 'Admin' THEN 1 ELSE 0 END) AS total_admin,
            SUM(CASE WHEN r.role_name = 'Manager' THEN 1 ELSE 0 END) AS total_manager,
            SUM(CASE WHEN r.role_name = 'Receptionist' THEN 1 ELSE 0 END) AS total_receptionist,
            SUM(CASE WHEN r.role_name = 'Housekeeper' THEN 1 ELSE 0 END) AS total_housekeeper
        FROM Staff_Profiles sp
        LEFT JOIN Roles r ON sp.role_id = r.role_id
    """)
    stats_row = cursor.fetchone()
    stats = dict(stats_row) if stats_row else {}

    cursor.execute("SELECT COUNT(*) FROM Accounts WHERE account_type = 'customer'")
    stats['total_customers'] = cursor.fetchone()[0]

    conn.close()
    return jsonify({'success': True, 'users': users_list, 'stats': stats})


@admin_bp.route('/api/users/<int:target_user_id>/role', methods=['PUT'])
def api_update_user_role(target_user_id):
    auth_err = require_token()
    if auth_err is not None:
        return auth_err
    caller_role = get_user_role_from_db(g.api_user_id, g.api_account_type or 'staff')
    if caller_role != 'Admin':
        return jsonify({'success': False, 'message': 'Khong co quyen'}), 403
    data = request.get_json()
    new_role_name = data.get('new_role_name')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role_id FROM Roles WHERE role_name = ?", (new_role_name,))
    role_row = cursor.fetchone()
    if not role_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Vai tro khong ton tai'}), 404
    
    new_role_id = role_row['role_id']
    
    if new_role_name == 'Guest':
        # Hạ cấp xuống customer
        cursor.execute("DELETE FROM Staff_Profiles WHERE account_id = ?", (target_user_id,))
        cursor.execute("UPDATE Accounts SET account_type = 'customer' WHERE account_id = ?", (target_user_id,))
    else:
        # Cập nhật hoặc thêm vào Staff_Profiles
        cursor.execute("SELECT account_id FROM Staff_Profiles WHERE account_id = ?", (target_user_id,))
        if cursor.fetchone():
            cursor.execute("UPDATE Staff_Profiles SET role_id = ? WHERE account_id = ?", (new_role_id, target_user_id))
        else:
            cursor.execute("SELECT email FROM Accounts WHERE account_id = ?", (target_user_id,))
            acc = cursor.fetchone()
            uname = acc['email'].split('@')[0] if acc else f"user_{target_user_id}"
            cursor.execute("""
                INSERT INTO Staff_Profiles (account_id, role_id, full_name, username)
                VALUES (?, ?, ?, ?)
            """, (target_user_id, new_role_id, uname, uname))
        cursor.execute("UPDATE Accounts SET account_type = 'staff' WHERE account_id = ?", (target_user_id,))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Cap nhat vai tro thanh cong'})


@admin_bp.route('/api/users/<int:target_user_id>', methods=['DELETE'])
def api_delete_user(target_user_id):
    auth_err = require_token()
    if auth_err is not None:
        return auth_err
    caller_role = get_user_role_from_db(g.api_user_id, g.api_account_type or 'staff')
    if caller_role != 'Admin':
        return jsonify({'success': False, 'message': 'Khong co quyen'}), 403
    
    if target_user_id == g.api_user_id:
        return jsonify({'success': False, 'message': 'Không thể tự xóa tài khoản Quản trị viên đang đăng nhập'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Staff_Profiles WHERE account_id = ?", (target_user_id,))
    cursor.execute("DELETE FROM Customer_Profiles WHERE account_id = ?", (target_user_id,))
    cursor.execute("DELETE FROM Accounts WHERE account_id = ?", (target_user_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Xoa thanh cong'})


