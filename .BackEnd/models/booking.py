"""
Booking Domain Models: Booking, BookingNight.
Tuân thủ 100% Trang-13 trong Tong_Hop_Bieu_Do.drawio.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from .room import RoomType, PhysicalRoom
from .account import CustomerProfile


class BookingNight:
    """«Entity» BookingNight - Chi tiết từng đêm lưu trú trong đơn đặt phòng"""
    def __init__(
        self,
        night_id: int,
        stay_date: str,
        night_price: float,
        status: str = 'RESERVED',
        assigned_room: Optional[PhysicalRoom] = None
    ):
        self.night_id = night_id
        self.stay_date = stay_date
        self.night_price = float(night_price)
        self.status = status.upper()
        self.assigned_room = assigned_room

    def gan_phong(self, room: PhysicalRoom) -> None:
        """Gán phòng vật lý cho đêm lưu trú (Check-in allocation)."""
        if not room.kiem_tra_san_sang_check_in():
            raise ValueError(f"Phòng {room.room_number} không đủ điều kiện check-in (Hiện tại: {room.housekeeping_status}/{room.occupancy_status}).")
        self.assigned_room = room
        self.status = 'ALLOCATED'

    def cap_nhat_gia_dem(self, price: float) -> None:
        """Cập nhật giá theo chính sách giá linh động ngày lễ/cuối tuần."""
        self.night_price = float(price)

    def cap_nhat_trang_thai(self, st: str) -> None:
        """Cập nhật trạng thái đêm nghỉ (RESERVED, ALLOCATED, COMPLETED, CANCELED)."""
        self.status = st.upper()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'night_id': self.night_id,
            'stay_date': self.stay_date,
            'night_price': self.night_price,
            'status': self.status,
            'assigned_room_id': self.assigned_room.physical_room_id if self.assigned_room else None,
            'assigned_room_number': self.assigned_room.room_number if self.assigned_room else None
        }


class Booking:
    """«Entity» Booking - Đơn đặt phòng (B2C Online hoặc Lễ tân Walk-in)"""
    def __init__(
        self,
        booking_id: int,
        pnr_code: str,
        guest_name: str,
        guest_phone: str,
        arrival_date: str,
        departure_date: str,
        room_type: RoomType,
        total_nights: int = 1,
        total_room_amount: float = 0.0,
        deposit_amount: float = 0.0,
        booking_status: str = 'PENDING',
        customer: Optional[CustomerProfile] = None
    ):
        self.booking_id = booking_id
        self.pnr_code = pnr_code
        self.guest_name = guest_name
        self.guest_phone = guest_phone
        self.arrival_date = arrival_date
        self.departure_date = departure_date
        self.room_type = room_type
        self.total_nights = total_nights
        self.total_room_amount = float(total_room_amount)
        self.deposit_amount = float(deposit_amount)
        self.booking_status = booking_status.upper()
        self.customer = customer  # Nullable for Walk-in without account
        self.nights: List[BookingNight] = []

    def tao_don_dat_phong(self, pnr: str) -> None:
        """Sinh mã PNR duy nhất và kích hoạt đơn đặt phòng ở trạng thái CONFIRMED."""
        self.pnr_code = pnr
        self.booking_status = 'CONFIRMED'

    def tinh_tong_tien_phong(self) -> float:
        """Tính tổng tiền phòng từ các đêm lưu trú chi tiết (Derived attribute)."""
        if self.nights:
            self.total_room_amount = sum(n.night_price for n in self.nights)
        elif self.room_type:
            self.total_room_amount = self.room_type.tinh_gia_phong(self.total_nights)
        return self.total_room_amount

    def xac_nhan_check_in(self) -> None:
        """Chuyển trạng thái đơn phòng sang CHECKED_IN khi khách nhận phòng."""
        if self.booking_status not in ('CONFIRMED', 'PENDING'):
            raise ValueError(f"Đơn phòng ở trạng thái {self.booking_status} không thể check-in.")
        self.booking_status = 'CHECKED_IN'

    def hoan_tat_check_out(self) -> None:
        """Chuyển trạng thái đơn phòng sang CHECKED_OUT sau khi thanh toán tất toán."""
        self.booking_status = 'CHECKED_OUT'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'booking_id': self.booking_id,
            'pnr_code': self.pnr_code,
            'guest_name': self.guest_name,
            'guest_phone': self.guest_phone,
            'arrival_date': self.arrival_date,
            'departure_date': self.departure_date,
            'room_type_id': self.room_type.room_type_id if self.room_type else None,
            'total_nights': self.total_nights,
            'total_room_amount': self.total_room_amount,
            'deposit_amount': self.deposit_amount,
            'booking_status': self.booking_status,
            'customer_id': self.customer.account.account_id if self.customer else None,
            'nights': [n.to_dict() for n in self.nights]
        }
