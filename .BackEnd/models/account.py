"""
IAM & RBAC Domain Models: Role, Account, StaffProfile, CustomerProfile.
Tuân thủ 100% Trang-13 trong Tong_Hop_Bieu_Do.drawio.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any


class Role:
    """«Entity» Role - Vai trò quản trị và phân quyền RBAC"""
    def __init__(self, role_id: int, role_name: str, description: Optional[str] = None, created_at: Optional[datetime] = None):
        self.role_id = role_id
        self.role_name = role_name
        self.description = description
        self.created_at = created_at or datetime.now()

    def phan_quyen(self, acc: 'Account') -> None:
        """Gán vai trò cho tài khoản nhân viên."""
        if hasattr(acc, 'staff_profile') and acc.staff_profile:
            acc.staff_profile.role = self

    def kiem_tra_quyen(self, action: str) -> bool:
        """Kiểm tra quyền thao tác nghiệp vụ theo RBAC."""
        permissions = {
            'Admin': ['all'],
            'Manager': ['view_reports', 'manage_rooms', 'manage_staff', 'approve_refunds'],
            'Receptionist': ['checkin', 'checkout', 'create_walkin', 'assign_room', 'record_service'],
            'Housekeeper': ['clean_room', 'inspect_room', 'report_maintenance']
        }
        allowed = permissions.get(self.role_name, [])
        return 'all' in allowed or action in allowed

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Account:
    """«Entity / Supertype» Account - Định danh duy nhất toàn hệ thống"""
    def __init__(
        self,
        account_id: int,
        email: str,
        password_hash: str,
        account_type: str = 'CUSTOMER',
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.account_id = account_id
        self.email = email
        self.password_hash = password_hash
        self.account_type = account_type.upper()
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.staff_profile: Optional['StaffProfile'] = None
        self.customer_profile: Optional['CustomerProfile'] = None

    def xac_thuc_dang_nhap(self, password: str, hasher_func=None) -> bool:
        """Xác thực mật khẩu người dùng."""
        if not self.is_active:
            return False
        if hasher_func:
            return hasher_func(password, self.password_hash)
        return self.password_hash == password

    def doi_mat_khau(self, old_pwd: str, new_pwd_hash: str, verify_func=None) -> bool:
        """Đổi mật khẩu người dùng sau khi xác minh mật khẩu cũ."""
        if verify_func and not verify_func(old_pwd, self.password_hash):
            return False
        self.password_hash = new_pwd_hash
        return True

    def cap_nhat_trang_thai(self, is_active: bool) -> None:
        """Khóa hoặc kích hoạt tài khoản."""
        self.is_active = is_active

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account_id,
            'email': self.email,
            'account_type': self.account_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class StaffProfile:
    """«Entity» StaffProfile - Hồ sơ nhân viên kế thừa 1:1 từ Account"""
    def __init__(
        self,
        account: Account,
        staff_code: str,
        full_name: str,
        phone: str,
        department: str,
        role: Optional[Role] = None
    ):
        self.account = account
        self.staff_code = staff_code
        self.full_name = full_name
        self.phone = phone
        self.department = department
        self.role = role
        account.staff_profile = self

    def tiep_nhan_ca_truc(self) -> None:
        """Ghi nhận bắt đầu ca trực nhân sự."""
        pass

    def tra_cuu_lich_su_ca_truc(self) -> List[Dict[str, Any]]:
        """Tra cứu lịch sử ca trực và tác nghiệp."""
        return []

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account.account_id,
            'staff_code': self.staff_code,
            'full_name': self.full_name,
            'phone': self.phone,
            'department': self.department,
            'role_name': self.role.role_name if self.role else None
        }


class CustomerProfile:
    """«Entity» CustomerProfile - Hồ sơ khách hàng / hội viên kế thừa 1:1 từ Account"""
    def __init__(
        self,
        account: Account,
        full_name: str,
        phone: str,
        id_card_number: Optional[str] = None,
        loyalty_points: int = 0,
        membership_tier: str = 'STANDARD',
        address: Optional[str] = None
    ):
        self.account = account
        self.full_name = full_name
        self.phone = phone
        self.id_card_number = id_card_number
        self.loyalty_points = loyalty_points
        self.membership_tier = membership_tier.upper()
        self.address = address
        account.customer_profile = self

    def tich_luy_diem(self, amount: float) -> None:
        """Tích lũy điểm hội viên: 100.000 VNĐ = 1 điểm."""
        points_earned = int(amount // 100000)
        self.loyalty_points += points_earned
        self.nang_hang_thanh_vien()

    def nang_hang_thanh_vien(self) -> None:
        """Nâng hạng hội viên tự động theo số điểm tích lũy."""
        if self.loyalty_points >= 1000:
            self.membership_tier = 'PLATINUM'
        elif self.loyalty_points >= 500:
            self.membership_tier = 'GOLD'
        elif self.loyalty_points >= 200:
            self.membership_tier = 'SILVER'
        else:
            self.membership_tier = 'STANDARD'

    def cap_nhat_thong_tin(self, info: Dict[str, Any]) -> None:
        """Cập nhật thông tin định danh và liên hệ."""
        if 'full_name' in info:
            self.full_name = info['full_name']
        if 'phone' in info:
            self.phone = info['phone']
        if 'id_card_number' in info:
            self.id_card_number = info['id_card_number']
        if 'address' in info:
            self.address = info['address']

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account.account_id,
            'full_name': self.full_name,
            'phone': self.phone,
            'id_card_number': self.id_card_number,
            'loyalty_points': self.loyalty_points,
            'membership_tier': self.membership_tier,
            'address': self.address
        }
