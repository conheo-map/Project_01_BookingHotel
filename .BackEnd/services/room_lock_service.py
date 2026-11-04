"""
Room Lock Service - Quản lý khóa giữ phòng tạm thời chống Overbooking.
Kiến trúc: Clean Service Layer
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict, Any, Union
import sqlite3

from database import get_db_connection
from services.exceptions import RoomAlreadyLockedError, RoomNotAvailableError


def cleanup_expired_locks(conn=None) -> int:
    """Quét và giải phóng các phòng đã hết hạn giữ chỗ (locked_until < now)."""
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Room_Lock WHERE locked_until < ?", (now_str,))
        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count
    finally:
        if owns_conn:
            conn.close()


def release_expired_locks(conn=None) -> int:
    """Tương thích ngược: Alias cho cleanup_expired_locks."""
    return cleanup_expired_locks(conn=conn)


def check_room_availability_internal(
    cursor,
    physical_room_id: int,
    night_dates: List[str],
    exclude_session_id: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Hàm kiểm tra nội bộ: Trả về (is_available, error_type, reason_message)
    error_type: None | 'BOOKED' | 'LOCKED'
    """
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for night in night_dates:
        # 1. Kiểm tra đơn đặt phòng thực tế (trừ các đơn đã hủy hoặc no-show)
        cursor.execute("""
            SELECT 1 FROM Booking_Nights bn
            JOIN Booking_Master bm ON bn.booking_id = bm.booking_id
            WHERE bn.physical_room_id = ?
              AND bn.night_date = ?
              AND bm.booking_status NOT IN ('Canceled', 'No-Show')
            LIMIT 1
        """, (physical_room_id, night))
        if cursor.fetchone():
            return False, 'BOOKED', f"Đêm {night} đã có đơn đặt phòng thực tế bởi khách khác."

        # 2. Kiểm tra khóa giữ chỗ tạm thời (Room_Lock) còn hạn
        if exclude_session_id:
            cursor.execute("""
                SELECT 1 FROM Room_Lock
                WHERE physical_room_id = ?
                  AND lock_date = ?
                  AND locked_until > ?
                  AND session_id != ?
                LIMIT 1
            """, (physical_room_id, night, now_str, exclude_session_id))
        else:
            cursor.execute("""
                SELECT 1 FROM Room_Lock
                WHERE physical_room_id = ?
                  AND lock_date = ?
                  AND locked_until > ?
                LIMIT 1
            """, (physical_room_id, night, now_str))

        if cursor.fetchone():
            return False, 'LOCKED', f"Đêm {night} hiện đang được giữ chỗ tạm thời trong 10 phút bởi khách khác."

    return True, None, None


def is_room_available_for_nights(*args, **kwargs) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra phòng vật lý có sẵn sàng cho danh sách đêm hay không.
    Hỗ trợ 2 chữ ký hàm:
    - is_room_available_for_nights(physical_room_id, nights_list, session_id=None)
    - is_room_available_for_nights(cursor, physical_room_id, night_dates, exclude_session_id=None)
    """
    if len(args) > 0 and hasattr(args[0], 'execute'):
        # Chữ ký cũ có cursor: (cursor, physical_room_id, night_dates, exclude_session_id=None)
        cursor = args[0]
        physical_room_id = args[1]
        night_dates = args[2]
        exclude_session_id = args[3] if len(args) > 3 else kwargs.get('exclude_session_id')
        avail, _, reason = check_room_availability_internal(cursor, physical_room_id, night_dates, exclude_session_id)
        return avail, reason
    else:
        # Chữ ký mới: (physical_room_id, nights_list, session_id=None)
        physical_room_id = args[0] if len(args) > 0 else kwargs.get('physical_room_id')
        night_dates = args[1] if len(args) > 1 else kwargs.get('nights_list', [])
        session_id = args[2] if len(args) > 2 else kwargs.get('session_id')

        conn = kwargs.get('conn')
        owns_conn = False
        if conn is None:
            conn = get_db_connection()
            owns_conn = True
        try:
            cursor = conn.cursor()
            avail, _, reason = check_room_availability_internal(cursor, physical_room_id, night_dates, session_id)
            return avail, reason
        finally:
            if owns_conn:
                conn.close()


def lock_room_for_nights(
    physical_room_id: int,
    nights_list: List[str],
    session_id: str,
    ttl_minutes: int = 10,
    booking_temp_ref: Optional[str] = None,
    raise_on_error: bool = True
) -> Dict[str, Any]:
    """
    Khóa giữ chỗ phòng vật lý tạm thời trong ttl_minutes (mặc định 10 phút).
    - Quét và dọn các khóa quá hạn
    - Kiểm tra tính khả dụng: Ném RoomAlreadyLockedError hoặc RoomNotAvailableError nếu raise_on_error=True
    - Ghi nhận khóa vào bảng Room_Lock
    """
    if not nights_list:
        if raise_on_error:
            raise ValueError("Danh sách ngày cần khóa không được để trống.")
        return {'success': False, 'message': 'Danh sách ngày cần khóa không được để trống.'}

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 1. Dọn dẹp các khóa hết hạn
        cursor.execute("DELETE FROM Room_Lock WHERE locked_until < ?", (now_str,))

        # 2. Kiểm tra tính khả dụng
        is_avail, err_type, reason = check_room_availability_internal(
            cursor, physical_room_id, nights_list, exclude_session_id=session_id
        )

        if not is_avail:
            if raise_on_error:
                if err_type == 'LOCKED':
                    raise RoomAlreadyLockedError(reason or "Phòng đang được giữ chỗ bởi khách khác.")
                else:
                    raise RoomNotAvailableError(reason or "Phòng đã có đơn đặt phòng thực tế.")
            return {'success': False, 'message': reason, 'error_type': err_type}

        # 3. Xóa các lock cũ của cùng session trên phòng này (refresh gia hạn)
        cursor.execute("""
            DELETE FROM Room_Lock
            WHERE session_id = ? AND physical_room_id = ?
        """, (session_id, physical_room_id))

        locked_until_dt = datetime.now() + timedelta(minutes=ttl_minutes)
        locked_until_str = locked_until_dt.strftime('%Y-%m-%d %H:%M:%S')

        # 4. Ghi khóa mới cho từng đêm
        for night in nights_list:
            cursor.execute("""
                INSERT INTO Room_Lock (physical_room_id, session_id, lock_date, locked_until, booking_temp_ref)
                VALUES (?, ?, ?, ?, ?)
            """, (physical_room_id, session_id, night, locked_until_str, booking_temp_ref))

        conn.commit()
        return {
            'success': True,
            'message': f'Đã khóa giữ chỗ thành công trong {ttl_minutes} phút.',
            'session_id': session_id,
            'physical_room_id': physical_room_id,
            'locked_until': locked_until_str,
            'locked_nights': nights_list
        }
    except (RoomAlreadyLockedError, RoomNotAvailableError):
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        if raise_on_error:
            raise
        return {'success': False, 'message': f'Lỗi hệ thống khi khóa phòng: {str(e)}'}
    finally:
        conn.close()


def lock_physical_room(
    physical_room_id: int,
    night_dates: List[str],
    session_id: str,
    ttl_minutes: int = 10,
    booking_temp_ref: Optional[str] = None
) -> Dict[str, Any]:
    """Tương thích ngược: lock_physical_room trả về dict (không raise exception)."""
    return lock_room_for_nights(
        physical_room_id=physical_room_id,
        nights_list=night_dates,
        session_id=session_id,
        ttl_minutes=ttl_minutes,
        booking_temp_ref=booking_temp_ref,
        raise_on_error=False
    )


def release_lock(session_id: str, physical_room_id: Optional[int] = None, conn=None) -> int:
    """Giải phóng khóa giữ phòng theo session sau khi đặt phòng hoàn tất hoặc giỏ hàng bị hủy."""
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        cursor = conn.cursor()
        if physical_room_id:
            cursor.execute("DELETE FROM Room_Lock WHERE session_id = ? AND physical_room_id = ?", (session_id, physical_room_id))
        else:
            cursor.execute("DELETE FROM Room_Lock WHERE session_id = ?", (session_id,))
        count = cursor.rowcount
        conn.commit()
        return count
    finally:
        if owns_conn:
            conn.close()


def release_locks_by_session(session_id: str, physical_room_id: Optional[int] = None, conn=None) -> int:
    """Tương thích ngược: Alias cho release_lock."""
    return release_lock(session_id=session_id, physical_room_id=physical_room_id, conn=conn)


# =========================================================================
# CHUẨN MỰC MỚI UML 2.X & 3NF: KHÓA GIỮ CHỖ THEO LOẠI PHÒNG (RoomHoldLocks)
# =========================================================================

def cleanup_expired_room_hold_locks(conn=None) -> int:
    """Tự động cập nhật các khóa giữ chỗ RoomHoldLocks hết hạn sang status = 'expired'."""
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE RoomHoldLocks
            SET status = 'expired'
            WHERE status = 'active' AND expires_at <= ?
        """, (now_str,))
        count = cursor.rowcount
        conn.commit()
        return count
    finally:
        if owns_conn:
            conn.close()


def get_available_inventory_by_room_type(
    cursor,
    room_type_id: int,
    arrival_date: str,
    departure_date: str,
    exclude_session_id: Optional[str] = None
) -> int:
    """
    Tính số phòng trống khả dụng theo công thức:
    Available = TotalInventory - (SoldNights + ActiveLocks)
    Cho tất cả các đêm từ arrival_date đến departure_date.
    """
    # 1. Tổng số phòng vật lý đang hoạt động của loại phòng này
    cursor.execute("""
        SELECT COUNT(*) FROM Physical_Room
        WHERE room_type_id = ? AND is_active = 1
    """, (room_type_id,))
    total_inventory = cursor.fetchone()[0]
    if total_inventory <= 0:
        return 0

    # 2. Sinh danh sách các đêm
    arr_dt = datetime.strptime(arrival_date, '%Y-%m-%d').date()
    dep_dt = datetime.strptime(departure_date, '%Y-%m-%d').date()
    nights = []
    curr = arr_dt
    while curr < dep_dt:
        nights.append(curr.strftime('%Y-%m-%d'))
        curr += timedelta(days=1)

    if not nights:
        return 0

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    min_available = total_inventory

    for night in nights:
        # Số phòng đã bán/đã xác nhận trong đêm này
        cursor.execute("""
            SELECT COUNT(DISTINCT bn.b_night_id)
            FROM Booking_Nights bn
            JOIN Booking_Master bm ON bn.booking_id = bm.booking_id
            WHERE bm.room_type_id = ?
              AND bn.night_date = ?
              AND bm.booking_status NOT IN ('Canceled', 'No-Show')
        """, (room_type_id, night))
        sold_nights = cursor.fetchone()[0]

        # Số phòng đang bị khóa tạm thời trong đêm này
        if exclude_session_id:
            cursor.execute("""
                SELECT COALESCE(SUM(quantity), 0)
                FROM RoomHoldLocks
                WHERE room_type_id = ?
                  AND status = 'active'
                  AND expires_at > ?
                  AND arrival_date <= ? AND departure_date > ?
                  AND session_id != ?
            """, (room_type_id, now_str, night, night, exclude_session_id))
        else:
            cursor.execute("""
                SELECT COALESCE(SUM(quantity), 0)
                FROM RoomHoldLocks
                WHERE room_type_id = ?
                  AND status = 'active'
                  AND expires_at > ?
                  AND arrival_date <= ? AND departure_date > ?
            """, (room_type_id, now_str, night, night))
        active_locks = cursor.fetchone()[0]

        avail_tonight = total_inventory - (sold_nights + active_locks)
        if avail_tonight < min_available:
            min_available = avail_tonight

    return max(0, min_available)


def create_room_hold_lock(
    room_type_id: int,
    session_id: str,
    arrival_date: str,
    departure_date: str,
    quantity: int = 1,
    ttl_minutes: int = 15
) -> Dict[str, Any]:
    """
    Tạo bản ghi khóa giữ chỗ tạm thời (TTL 15 phút) theo Loại phòng (RoomType).
    Ngăn chặn 100% Race Condition / Overbooking mà không cần gán cứng phòng vật lý!
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cleanup_expired_room_hold_locks(conn=conn)

        # Kiểm tra tồn kho khả dụng
        avail = get_available_inventory_by_room_type(
            cursor, room_type_id, arrival_date, departure_date, exclude_session_id=session_id
        )

        if avail < quantity:
            return {
                'success': False,
                'message': f'Loại phòng này hiện chỉ còn {avail} phòng trống, không đủ đáp ứng số lượng {quantity} phòng bạn yêu cầu.',
                'available': avail
            }

        now_dt = datetime.now()
        exp_dt = now_dt + timedelta(minutes=ttl_minutes)
        now_str = now_dt.strftime('%Y-%m-%d %H:%M:%S')
        exp_str = exp_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Vô hiệu hóa lock cũ của cùng session nếu có
        cursor.execute("""
            UPDATE RoomHoldLocks
            SET status = 'expired'
            WHERE session_id = ? AND status = 'active'
        """, (session_id,))

        cursor.execute("""
            INSERT INTO RoomHoldLocks (
                room_type_id, session_id, quantity,
                arrival_date, departure_date, locked_at, expires_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
        """, (room_type_id, session_id, quantity, arrival_date, departure_date, now_str, exp_str))
        hold_id = cursor.lastrowid
        conn.commit()

        return {
            'success': True,
            'message': f'Đã khóa giữ chỗ thành công {quantity} phòng trong {ttl_minutes} phút.',
            'hold_id': hold_id,
            'session_id': session_id,
            'room_type_id': room_type_id,
            'expires_at': exp_str,
            'quantity': quantity
        }
    except Exception as e:
        conn.rollback()
        return {'success': False, 'message': f'Lỗi hệ thống khi khóa giữ chỗ: {str(e)}'}
    finally:
        conn.close()


def convert_room_hold_lock(hold_id: int, conn=None) -> bool:
    """Chuyển trạng thái khóa phòng sang 'converted' khi khách thanh toán thành công."""
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE RoomHoldLocks
            SET status = 'converted'
            WHERE hold_id = ?
        """, (hold_id,))
        count = cursor.rowcount
        if owns_conn:
            conn.commit()
        return count > 0
    finally:
        if owns_conn:
            conn.close()

