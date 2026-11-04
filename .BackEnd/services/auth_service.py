"""
Auth Service - Quản lý Danh tính duy nhất (Single Identity Model) cho Khách hàng và Nhân viên.
Bảng nguồn: Accounts, Customer_Profiles, Staff_Profiles, Roles.
"""

from typing import Tuple, Dict, Any, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from services.auth_tokens import create_api_token


def register_customer(email: str, password: str, full_name: str, phone: Optional[str] = None) -> Tuple[bool, Dict[str, Any], str]:
    """Đăng ký tài khoản khách hàng mới vào Accounts và Customer_Profiles."""
    email_clean = (email or '').strip().lower()
    pass_clean = (password or '').strip()
    name_clean = (full_name or '').strip()

    if not email_clean or not pass_clean:
        return False, {}, "Vui lòng nhập đầy đủ email và mật khẩu."

    pwd_hash = generate_password_hash(pass_clean)
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Accounts (email, password_hash, account_type, full_name, phone, is_active, created_at)
            VALUES (?, ?, 'customer', ?, ?, 1, datetime('now'))
        """, (email_clean, pwd_hash, name_clean, phone))
        new_account_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Customer_Profiles (account_id, loyalty_points, tier)
            VALUES (?, 0, 'Newbie')
        """, (new_account_id,))

        conn.commit()
        return True, {'user_id': new_account_id, 'email': email_clean, 'full_name': name_clean}, "Đăng ký tài khoản thành công."
    except Exception as e:
        conn.rollback()
        if "UNIQUE" in str(e).upper():
            return False, {}, "Email này đã được sử dụng trên hệ thống."
        return False, {}, f"Lỗi đăng ký tài khoản: {str(e)}"
    finally:
        conn.close()


def authenticate_user(login_input: str, password: str) -> Tuple[bool, Dict[str, Any], str]:
    """
    Xác thực đăng nhập cho cả Khách hàng và Nhân viên:
    1. Kiểm tra tài khoản Khách hàng (Accounts.account_type = 'customer' qua email)
    2. Kiểm tra tài khoản Nhân viên (Staff_Profiles.username hoặc Accounts.email qua staff)
    """
    inp = (login_input or '').strip()
    pwd = (password or '').strip()
    if not inp or not pwd:
        return False, {}, "Vui lòng nhập tên đăng nhập/email và mật khẩu."

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Thử tài khoản Khách hàng
        cursor.execute("""
            SELECT a.account_id, a.email, a.password_hash, a.full_name, a.is_active,
                   cp.loyalty_points, cp.tier
            FROM Accounts a
            JOIN Customer_Profiles cp ON a.account_id = cp.account_id
            WHERE a.email = ? AND a.account_type = 'customer'
        """, (inp.lower(),))
        cust = cursor.fetchone()

        if cust and check_password_hash(cust['password_hash'], pwd):
            if not cust['is_active']:
                return False, {}, "Tài khoản của bạn đang bị tạm khóa."
            uid = cust['account_id']
            token = create_api_token(uid, 'customer')
            payload = {
                'user_id': uid,
                'email': cust['email'],
                'username': cust['email'],
                'full_name': cust['full_name'] or '',
                'role': 'Guest',
                'account_type': 'customer',
                'token': token
            }
            return True, payload, "Đăng nhập thành công."

        # 2. Thử tài khoản Nhân viên (Staff)
        cursor.execute("""
            SELECT a.account_id, a.email, a.password_hash, a.full_name, a.is_active,
                   sp.username, r.role_name
            FROM Accounts a
            JOIN Staff_Profiles sp ON a.account_id = sp.account_id
            JOIN Roles r ON sp.role_id = r.role_id
            WHERE (sp.username = ? OR a.email = ?) AND a.account_type = 'staff'
        """, (inp, inp.lower()))
        staff = cursor.fetchone()

        if staff and check_password_hash(staff['password_hash'], pwd):
            if not staff['is_active']:
                return False, {}, "Tài khoản nhân viên này đang bị vô hiệu hóa."
            sid = staff['account_id']
            token = create_api_token(sid, 'staff')
            payload = {
                'user_id': sid,
                'username': staff['username'],
                'email': staff['email'],
                'full_name': staff['full_name'] or '',
                'role': staff['role_name'],
                'account_type': 'staff',
                'token': token
            }
            return True, payload, "Đăng nhập thành công."

        return False, {}, "Sai thông tin đăng nhập hoặc mật khẩu không chính xác."
    finally:
        conn.close()


def update_customer_profile(account_id: int, full_name: str, old_password: str = '', new_password: str = '') -> Tuple[bool, str]:
    """Cập nhật thông tin họ tên và đổi mật khẩu cho khách hàng."""
    name_clean = (full_name or '').strip()
    if not name_clean:
        return False, "Tên hiển thị không được để trống."

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM Accounts WHERE account_id = ? AND account_type = 'customer'", (account_id,))
        acc = cursor.fetchone()
        if not acc:
            return False, "Không tìm thấy thông tin tài khoản khách hàng."

        if new_password:
            if not old_password:
                return False, "Vui lòng nhập mật khẩu hiện tại để xác nhận đổi mật khẩu."
            if not check_password_hash(acc['password_hash'], old_password):
                return False, "Mật khẩu hiện tại không chính xác."
            new_hash = generate_password_hash(new_password)
            cursor.execute("UPDATE Accounts SET full_name = ?, password_hash = ? WHERE account_id = ?", (name_clean, new_hash, account_id))
        else:
            cursor.execute("UPDATE Accounts SET full_name = ? WHERE account_id = ?", (name_clean, account_id))

        conn.commit()
        return True, "Cập nhật hồ sơ thành công."
    except Exception as e:
        conn.rollback()
        return False, f"Lỗi cập nhật hồ sơ: {str(e)}"
    finally:
        conn.close()
