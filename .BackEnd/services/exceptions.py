"""
Custom Domain Exceptions for Saigon - Condao Booking Platform.
Kiến trúc: Clean Layered Architecture - Service Layer Exceptions.
"""

class BookingDomainError(Exception):
    """Lớp ngoại lệ cơ sở cho toàn bộ nghiệp vụ đặt phòng."""
    def __init__(self, message: str = "Lỗi nghiệp vụ đặt phòng", code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class RoomAlreadyLockedError(BookingDomainError):
    """Phòng đã bị người khác giữ chỗ tạm thời trong phiên 10 phút."""
    def __init__(self, message: str = "Phòng hiện đang được giữ chỗ tạm thời bởi khách hàng khác. Vui lòng thử lại sau 10 phút hoặc chọn phòng khác."):
        super().__init__(message=message, code="ROOM_ALREADY_LOCKED")


class RoomNotAvailableError(BookingDomainError):
    """Phòng đã có người đặt thực tế hoặc không thể đáp ứng cho khoảng thời gian yêu cầu."""
    def __init__(self, message: str = "Phòng đã có đơn đặt phòng thực tế trong khoảng thời gian đã chọn."):
        super().__init__(message=message, code="ROOM_NOT_AVAILABLE")


class PromotionInvalidError(BookingDomainError):
    """Mã voucher khuyến mãi không hợp lệ, hết hạn, hết lượt dùng, hoặc không đủ hạng thẻ."""
    def __init__(self, message: str = "Mã khuyến mãi không hợp lệ hoặc không đủ điều kiện áp dụng."):
        super().__init__(message=message, code="PROMOTION_INVALID")


class BookingNotFoundError(BookingDomainError):
    """Không tìm thấy đơn đặt phòng tương ứng trong cơ sở dữ liệu."""
    def __init__(self, message: str = "Không tìm thấy thông tin đơn đặt phòng."):
        super().__init__(message=message, code="BOOKING_NOT_FOUND")


class InvalidBookingStateError(BookingDomainError):
    """Vi phạm vòng đời trạng thái đơn đặt phòng (State Transition Violation)."""
    def __init__(self, message: str = "Thao tác không hợp lệ đối với trạng thái hiện tại của đơn đặt phòng."):
        super().__init__(message=message, code="INVALID_BOOKING_STATE")
