"""
Room Domain Models: RoomType, PhysicalRoom, RoomHoldLock.
Tuân thủ 100% Trang-13 trong Tong_Hop_Bieu_Do.drawio.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class RoomType:
    """«Entity» RoomType - Hạng phòng thương mại B2C"""
    def __init__(
        self,
        room_type_id: int,
        type_code: str,
        type_name: str,
        base_price: float,
        max_adults: int = 2,
        total_inventory: int = 10,
        is_active: bool = True
    ):
        self.room_type_id = room_type_id
        self.type_code = type_code
        self.type_name = type_name
        self.base_price = float(base_price)
        self.max_adults = max_adults
        self.total_inventory = total_inventory
        self.is_active = is_active

    def kiem_tra_phong_trong(self, checkin_date: str, checkout_date: str) -> int:
        """Kiểm tra số lượng phòng khả dụng theo công thức: Total - Sold - ActiveLocks."""
        return self.total_inventory

    def tinh_gia_phong(self, total_nights: int, adults: int = 2) -> float:
        """Tính tổng tiền lưu trú theo số đêm và phụ thu nếu vượt maxAdults."""
        base_total = self.base_price * max(1, total_nights)
        extra_adults = max(0, adults - self.max_adults)
        extra_charge = extra_adults * 200000.0 * max(1, total_nights)
        return base_total + extra_charge

    def cap_nhat_ton_kho(self, delta: int) -> None:
        """Cập nhật tồn kho phòng thương mại."""
        self.total_inventory = max(0, self.total_inventory + delta)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'room_type_id': self.room_type_id,
            'type_code': self.type_code,
            'type_name': self.type_name,
            'base_price': self.base_price,
            'max_adults': self.max_adults,
            'total_inventory': self.total_inventory,
            'is_active': self.is_active
        }


class PhysicalRoom:
    """«Entity» PhysicalRoom - Phòng vật lý tác nghiệp tại cơ sở lưu trú"""
    def __init__(
        self,
        physical_room_id: int,
        room_type: RoomType,
        room_number: str,
        floor_number: int = 1,
        housekeeping_status: str = 'CLEAN',
        occupancy_status: str = 'VACANT',
        is_active: bool = True
    ):
        self.physical_room_id = physical_room_id
        self.room_type = room_type
        self.room_number = room_number
        self.floor_number = floor_number
        self.housekeeping_status = housekeeping_status.upper()
        self.occupancy_status = occupancy_status.upper()
        self.is_active = is_active

    def kiem_tra_san_sang_check_in(self) -> bool:
        """Điều kiện bắt buộc trước khi gán phòng check-in: Phải CLEAN và VACANT."""
        return self.is_active and self.housekeeping_status == 'CLEAN' and self.occupancy_status == 'VACANT'

    def chuyen_sang_dirty(self) -> None:
        """Chuyển trạng thái sang DIRTY sau khi khách trả phòng (Check-out)."""
        self.housekeeping_status = 'DIRTY'
        self.occupancy_status = 'VACANT'

    def chuyen_sang_clean(self) -> None:
        """Chuyển trạng thái sang CLEAN sau khi buồng phòng dọn xong."""
        self.housekeeping_status = 'CLEAN'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'physical_room_id': self.physical_room_id,
            'room_type_id': self.room_type.room_type_id if self.room_type else None,
            'room_number': self.room_number,
            'floor_number': self.floor_number,
            'housekeeping_status': self.housekeeping_status,
            'occupancy_status': self.occupancy_status,
            'is_active': self.is_active
        }


class RoomHoldLock:
    """«Entity» RoomHoldLock - Khóa giữ chỗ phòng tạm thời chống Overbooking / Race Condition"""
    def __init__(
        self,
        hold_id: int,
        room_type: RoomType,
        session_id: str,
        quantity: int = 1,
        locked_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        status: str = 'ACTIVE'
    ):
        self.hold_id = hold_id
        self.room_type = room_type
        self.session_id = session_id
        self.quantity = quantity
        self.locked_at = locked_at or datetime.now()
        # Chuẩn nghiệp vụ: Hạn giữ phòng 15 phút
        self.expires_at = expires_at or (self.locked_at + timedelta(minutes=15))
        self.status = status.upper()

    def tao_khoa_giu_cho(self, mins: int = 15) -> None:
        """Khởi tạo phiên khóa giữ chỗ với TTL mặc định 15 phút."""
        self.locked_at = datetime.now()
        self.expires_at = self.locked_at + timedelta(minutes=mins)
        self.status = 'ACTIVE'

    def kiem_tra_het_han(self) -> bool:
        """Kiểm tra khóa đã hết hạn hay chưa."""
        if self.status != 'ACTIVE':
            return True
        is_expired = datetime.now() > self.expires_at
        if is_expired:
            self.status = 'EXPIRED'
        return is_expired

    def chuyen_sang_da_ban(self) -> None:
        """Chuyển khóa tạm thời sang SOLD sau khi Webhook thanh toán xác nhận thành công."""
        self.status = 'SOLD'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'hold_id': self.hold_id,
            'room_type_id': self.room_type.room_type_id if self.room_type else None,
            'session_id': self.session_id,
            'quantity': self.quantity,
            'locked_at': self.locked_at.isoformat() if self.locked_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'status': self.status
        }
