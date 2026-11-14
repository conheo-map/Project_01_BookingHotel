"""
Finance & Billing Domain Models: ServiceItem, ServiceConsumption, FolioInvoice, PaymentTransaction.
Tuân thủ 100% Trang-13 trong Tong_Hop_Bieu_Do.drawio.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from .booking import Booking
from .account import StaffProfile


class ServiceItem:
    """«Entity» ServiceItem - Danh mục dịch vụ gia tăng (Minibar, Nhà hàng, Spa, Giặt ủi)"""
    def __init__(
        self,
        item_id: int,
        item_code: str,
        item_name: str,
        category: str,
        unit_price: float,
        vat_rate: float = 0.1,
        is_active: bool = True
    ):
        self.item_id = item_id
        self.item_code = item_code
        self.item_name = item_name
        self.category = category.upper()
        self.unit_price = float(unit_price)
        self.vat_rate = float(vat_rate)
        self.is_active = is_active

    def kiem_tra_kha_dung(self) -> bool:
        """Kiểm tra dịch vụ có đang mở bán hay không."""
        return self.is_active

    def lay_gia_ban_kem_thue(self) -> float:
        """Giá bán đã bao gồm thuế GTGT."""
        return round(self.unit_price * (1 + self.vat_rate), 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'item_id': self.item_id,
            'item_code': self.item_code,
            'item_name': self.item_name,
            'category': self.category,
            'unit_price': self.unit_price,
            'vat_rate': self.vat_rate,
            'is_active': self.is_active
        }


class ServiceConsumption:
    """«Entity» ServiceConsumption - Bản ghi tiêu dùng dịch vụ phát sinh trong thời gian lưu trú"""
    def __init__(
        self,
        consumption_id: int,
        booking: Booking,
        service_item: ServiceItem,
        quantity: int = 1,
        unit_price: Optional[float] = None,
        consumed_at: Optional[datetime] = None,
        staff: Optional[StaffProfile] = None
    ):
        self.consumption_id = consumption_id
        self.booking = booking
        self.service_item = service_item
        self.quantity = max(1, quantity)
        self.unit_price = float(unit_price if unit_price is not None else service_item.unit_price)
        self.consumed_at = consumed_at or datetime.now()
        self.staff = staff
        self.total_amount: float = self.tinh_thanh_tien()

    def tinh_thanh_tien(self) -> float:
        """Tính thành tiền tiêu dùng: quantity * unitPrice."""
        self.total_amount = round(self.quantity * self.unit_price, 2)
        return self.total_amount

    def ghi_nhan_tieu_dung(self, staff: StaffProfile) -> None:
        """Ghi nhận nhân viên tác nghiệp đã lập phiếu dịch vụ."""
        self.staff = staff

    def to_dict(self) -> Dict[str, Any]:
        return {
            'consumption_id': self.consumption_id,
            'booking_id': self.booking.booking_id if self.booking else None,
            'item_id': self.service_item.item_id if self.service_item else None,
            'item_name': self.service_item.item_name if self.service_item else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_amount': self.total_amount,
            'consumed_at': self.consumed_at.isoformat() if self.consumed_at else None,
            'staff_name': self.staff.full_name if self.staff else None
        }


class FolioInvoice:
    """«Entity» FolioInvoice - Hóa đơn tài chính tổng hợp quyết toán (Check-out)"""
    def __init__(
        self,
        invoice_id: int,
        booking: Booking,
        invoice_number: str,
        room_subtotal: float = 0.0,
        service_subtotal: float = 0.0,
        tax_vat_amount: float = 0.0,
        deposit_deducted: float = 0.0,
        final_amount: float = 0.0,
        status: str = 'DRAFT',
        issued_at: Optional[datetime] = None
    ):
        self.invoice_id = invoice_id
        self.booking = booking
        self.invoice_number = invoice_number
        self.room_subtotal = float(room_subtotal)
        self.service_subtotal = float(service_subtotal)
        self.tax_vat_amount = float(tax_vat_amount)
        self.deposit_deducted = float(deposit_deducted)
        self.final_amount = float(final_amount)
        self.status = status.upper()
        self.issued_at = issued_at or datetime.now()

    def tong_hop_chi_phi(self, consumptions: Optional[List[ServiceConsumption]] = None) -> None:
        """Tổng hợp tiền phòng và toàn bộ dịch vụ phát sinh theo chuẩn công thức 3NF."""
        self.room_subtotal = self.booking.tinh_tong_tien_phong()
        if consumptions:
            self.service_subtotal = sum(c.tinh_thanh_tien() for c in consumptions)
        # Thuế GTGT 10%
        self.tax_vat_amount = round((self.room_subtotal + self.service_subtotal) * 0.1, 2)
        self.deposit_deducted = float(self.booking.deposit_amount)
        self.tinh_tien_con_lai()

    def tinh_tien_con_lai(self) -> float:
        """Tính số tiền còn phải thanh toán: Room + Service + VAT - Deposit."""
        gross_total = self.room_subtotal + self.service_subtotal + self.tax_vat_amount
        self.final_amount = max(0.0, round(gross_total - self.deposit_deducted, 2))
        return self.final_amount

    def chot_quyet_toan(self, staff: StaffProfile) -> None:
        """Chuyển trạng thái sang ISSUED khi lễ tân chốt quyết toán thu tiền."""
        self.status = 'ISSUED'
        self.issued_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'invoice_id': self.invoice_id,
            'booking_id': self.booking.booking_id if self.booking else None,
            'invoice_number': self.invoice_number,
            'room_subtotal': self.room_subtotal,
            'service_subtotal': self.service_subtotal,
            'tax_vat_amount': self.tax_vat_amount,
            'deposit_deducted': self.deposit_deducted,
            'final_amount': self.final_amount,
            'status': self.status,
            'issued_at': self.issued_at.isoformat() if self.issued_at else None
        }


class PaymentTransaction:
    """«Entity» PaymentTransaction - Giao dịch thanh toán tiền cọc hoặc thanh toán quyết toán"""
    def __init__(
        self,
        payment_id: int,
        invoice: Optional[FolioInvoice],
        payment_type: str = 'DEPOSIT',
        payment_method: str = 'VNPAY_QR',
        amount: float = 0.0,
        transaction_code: str = '',
        payment_status: str = 'SUCCESS',
        created_at: Optional[datetime] = None
    ):
        self.payment_id = payment_id
        self.invoice = invoice
        self.payment_type = payment_type.upper()
        self.payment_method = payment_method.upper()
        self.amount = float(amount)
        self.transaction_code = transaction_code
        self.payment_status = payment_status.upper()
        self.created_at = created_at or datetime.now()

    def ghi_nhan_giao_dich(self, code: str, amt: float) -> None:
        """Ghi nhận mã tham chiếu từ ngân hàng/cổng thanh toán."""
        self.transaction_code = code
        self.amount = float(amt)

    def xac_nhan_thanh_cong(self) -> None:
        """Xác nhận giao dịch thanh toán thành công."""
        self.payment_status = 'SUCCESS'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'payment_id': self.payment_id,
            'invoice_id': self.invoice.invoice_id if self.invoice else None,
            'payment_type': self.payment_type,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'transaction_code': self.transaction_code,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
