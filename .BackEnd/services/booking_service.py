"""
Booking Service - Tầng nghiệp vụ cốt lõi quản lý Đặt phòng (Online & Walk-in),
Check-in, Hủy phòng, Đổi phòng, Dịch vụ phát sinh và Sơ đồ phòng.
Tuân thủ kiến trúc Clean Architecture, chuẩn 3NF và tiền tệ số nguyên VND.
"""

from datetime import datetime, timedelta, date
from typing import Dict, Any, Tuple, List, Optional
import sqlite3

from database import get_db_connection
from config import DEFAULT_TAX_RATE
from services.exceptions import (
    RoomAlreadyLockedError,
    RoomNotAvailableError,
    PromotionInvalidError,
    BookingNotFoundError,
    InvalidBookingStateError
)
from services.pricing_service import calculate_booking_price, evaluate_room_occupancy, get_effective_daily_price
from services.promotion_service import validate_and_apply_promo
from services.room_lock_service import (
    release_expired_locks, release_locks_by_session, is_room_available_for_nights,
    get_available_inventory_by_room_type, convert_room_hold_lock
)
from services.checkout_service import recalculate_folio_invoice


def cleanup_expired_locks(conn=None):
    """Tiện ích dọn dẹp các khóa phòng hết hạn (gọi định kỳ bởi background cron job)."""
    return release_expired_locks(conn)


def get_user_role_from_db(account_id: int, account_type: str = 'staff', cursor=None) -> Optional[str]:
    """Tra cứu vai trò (role) của tài khoản từ Accounts/Staff_Profiles."""
    if not account_id:
        return None

    owns_conn = False
    conn = None
    if cursor is None:
        conn = get_db_connection()
        cursor = conn.cursor()
        owns_conn = True

    try:
        if account_type == 'customer':
            cursor.execute("SELECT account_id FROM Accounts WHERE account_id = ? AND account_type = 'customer'", (account_id,))
            return 'Guest' if cursor.fetchone() else None

        cursor.execute("""
            SELECT r.role_name
            FROM Staff_Profiles sp
            JOIN Roles r ON sp.role_id = r.role_id
            WHERE sp.account_id = ?
        """, (account_id,))
        row = cursor.fetchone()
        return row['role_name'] if row else None
    finally:
        if owns_conn and conn:
            conn.close()


def calculate_loyalty_tier(total_points: int) -> str:
    """Xác định hạng thành viên theo điểm thưởng."""
    if total_points >= 210:
        return 'Gold'
    elif total_points >= 50:
        return 'Silver'
    return 'Newbie'


def get_room_availability(cursor, room_type_id: int, checkin_date_obj: date, checkout_date_obj: date):
    """
    Phân loại phòng vật lý còn trống thành 2 nhóm:
    - continuous_available_rooms: Trống toàn bộ các đêm liên tục
    - fragmented_available_rooms: Trống một số đêm ngắt quãng
    """
    cursor.execute("""
        SELECT physical_room_id, room_name, housekeeping_status
        FROM Physical_Room
        WHERE room_type_id = ? AND is_active = 1
        ORDER BY room_name
    """, (room_type_id,))
    all_rooms = cursor.fetchall()
    if not all_rooms:
        return [], []

    list_of_nights = []
    curr = checkin_date_obj
    while curr < checkout_date_obj:
        list_of_nights.append(curr.strftime('%Y-%m-%d'))
        curr += timedelta(days=1)

    start_str = checkin_date_obj.strftime('%Y-%m-%d')
    end_str = checkout_date_obj.strftime('%Y-%m-%d')

    # Lấy các đêm đã đặt từ Booking_Nights
    cursor.execute("""
        SELECT bn.physical_room_id, bn.night_date
        FROM Booking_Nights bn
        JOIN Booking_Master bm ON bn.booking_id = bm.booking_id
        WHERE bm.booking_status NOT IN ('Canceled', 'No-Show')
          AND bn.physical_room_id IN (SELECT physical_room_id FROM Physical_Room WHERE room_type_id = ?)
          AND bn.night_date >= ? AND bn.night_date < ?
    """, (room_type_id, start_str, end_str))
    booked_nights = cursor.fetchall()

    # Lấy các đêm đang bị khóa giữ chỗ (Room_Lock)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        SELECT physical_room_id, lock_date
        FROM Room_Lock
        WHERE physical_room_id IN (SELECT physical_room_id FROM Physical_Room WHERE room_type_id = ?)
          AND locked_until > ? AND lock_date >= ? AND lock_date < ?
    """, (room_type_id, now_str, start_str, end_str))
    locked_nights = cursor.fetchall()

    occ_map = {r['physical_room_id']: set() for r in all_rooms}
    for bn in booked_nights:
        if bn['physical_room_id'] in occ_map:
            occ_map[bn['physical_room_id']].add(bn['night_date'])
    for ln in locked_nights:
        if ln['physical_room_id'] in occ_map:
            occ_map[ln['physical_room_id']].add(ln['lock_date'])

    continuous = []
    fragmented = []

    for r in all_rooms:
        pid = r['physical_room_id']
        occ_set = occ_map.get(pid, set())
        free_nights = [n for n in list_of_nights if n not in occ_set]
        occ_nights = [n for n in list_of_nights if n in occ_set]

        room_data = {
            'physical_room_id': pid,
            'room_name': r['room_name'],
            'housekeeping_status': r['housekeeping_status'],
            'free_nights': free_nights,
            'occupied_nights': occ_nights
        }
        if len(occ_nights) == 0:
            continuous.append(room_data)
        elif len(free_nights) > 0:
            fragmented.append(room_data)

    return continuous, fragmented


def create_online_booking(data: Dict[str, Any], customer_account_id: int, raise_on_error: bool = False) -> Tuple[bool, Dict[str, Any], str]:
    """
    Kịch bản Đặt phòng Online trọn vẹn trong 1 Database Transaction:
    1. Kiểm tra tính hợp lệ dữ liệu & Room_Lock
    2. Tính giá phòng và phụ thu qua pricing_service
    3. Áp voucher qua promotion_service (atomic update)
    4. Tính thuế VAT và số tiền đặt cọc (VND nguyên)
    5. Ghi vào Booking_Master, Invoices, Booking_Attributions, Booking_Nights, Payments
    6. Giải phóng Room_Lock
    """
    hotel_id = data.get('hotel_id')
    room_type_id = data.get('room_type_id')
    physical_room_id = data.get('physical_room_id')
    booking_type = data.get('booking_type', 'continuous')
    checkin_date_str = data.get('checkin_date') or data.get('arrival_date') or ''
    checkout_date_str = data.get('checkout_date') or data.get('departure_date') or ''
    selected_nights = data.get('selected_nights') or []
    adults = int(data.get('adults', 1))
    children = int(data.get('children', 0))
    babies = int(data.get('babies', 0))
    promo_code = (data.get('promo_code') or '').strip().upper()
    payment_type = data.get('payment_type', 'full')
    payment_method = data.get('payment_method', 'credit_card')
    special_requests = data.get('special_requests', '').strip()
    source_channel = (data.get('source_channel') or 'direct').strip()
    utm_campaign = (data.get('utm_campaign') or '').strip()
    utm_medium = (data.get('utm_medium') or '').strip()
    session_id = data.get('session_id', '')

    if not all([customer_account_id, hotel_id, room_type_id]):
        return False, {}, "Thiếu thông tin bắt buộc để tạo đơn đặt phòng."

    hold_id = data.get('hold_id')

    # Xác định danh sách đêm cần đặt
    if booking_type == 'continuous':
        try:
            ci_dt = datetime.strptime(checkin_date_str, '%Y-%m-%d').date()
            co_dt = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
            if ci_dt >= co_dt:
                return False, {}, "Ngày nhận phòng phải trước ngày trả phòng."
        except ValueError:
            return False, {}, "Định dạng ngày nhận/trả phòng không hợp lệ."

        list_of_nights = []
        curr = ci_dt
        while curr < co_dt:
            list_of_nights.append(curr.strftime('%Y-%m-%d'))
            curr += timedelta(days=1)
    else:
        if isinstance(selected_nights, str):
            list_of_nights = [n.strip() for n in selected_nights.split(',') if n.strip()]
        else:
            list_of_nights = list(selected_nights)
        list_of_nights.sort()
        if not list_of_nights:
            return False, {}, "Danh sách đêm ngắt quãng không được để trống."
        checkin_date_str = list_of_nights[0]
        checkout_date_str = (datetime.strptime(list_of_nights[-1], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Kiểm tra khóa giữ chỗ & Tồn kho khả dụng (Chuẩn B2C: Khóa theo RoomType)
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not physical_room_id:
            # Luồng B2C Chuẩn UML 2.x & 3NF: Không gán trước phòng vật lý
            if hold_id:
                cursor.execute("""
                    SELECT 1 FROM RoomHoldLocks
                    WHERE hold_id = ? AND room_type_id = ? AND status = 'active' AND expires_at > ?
                """, (hold_id, room_type_id, now_str))
                if not cursor.fetchone():
                    msg = "Phiên giữ phòng (RoomHoldLock) đã hết hạn hoặc không hợp lệ. Vui lòng thử lại."
                    if raise_on_error:
                        raise RoomAlreadyLockedError(msg)
                    return False, {}, msg
            else:
                # Kiểm tra tồn kho khả dụng thời gian thực
                avail_qty = get_available_inventory_by_room_type(
                    cursor, room_type_id, checkin_date_str, checkout_date_str, exclude_session_id=session_id
                )
                if avail_qty < 1:
                    msg = "Loại phòng này hiện đã hết phòng trống trong khoảng thời gian đã chọn."
                    if raise_on_error:
                        raise RoomNotAvailableError(msg)
                    return False, {}, msg
        else:
            # Luồng tương thích ngược: Khách hoặc Lễ tân chỉ định phòng vật lý
            if session_id:
                cursor.execute("""
                    SELECT 1 FROM Room_Lock
                    WHERE physical_room_id = ? AND session_id = ? AND locked_until > ?
                """, (physical_room_id, session_id, now_str))
                if not cursor.fetchone():
                    cursor.execute("""
                        SELECT 1 FROM Room_Lock
                        WHERE physical_room_id = ? AND locked_until > ?
                    """, (physical_room_id, now_str))
                    if cursor.fetchone():
                        msg = "Phòng hiện đang được giữ chỗ bởi một phiên đặt phòng khác."
                        if raise_on_error:
                            raise RoomAlreadyLockedError(msg)
                        return False, {}, msg
            else:
                cursor.execute("""
                    SELECT 1 FROM Room_Lock
                    WHERE physical_room_id = ? AND locked_until > ?
                """, (physical_room_id, now_str))
                if cursor.fetchone():
                    msg = "Phòng hiện đang được giữ chỗ tạm thời trong 15 phút bởi khách hàng khác."
                    if raise_on_error:
                        raise RoomAlreadyLockedError(msg)
                    return False, {}, msg

            avail, reason = is_room_available_for_nights(cursor, physical_room_id, list_of_nights, exclude_session_id=session_id)
            if not avail:
                if raise_on_error:
                    raise RoomNotAvailableError(reason or "Phòng đã có đơn đặt phòng thực tế.")
                return False, {}, reason or "Phòng đã có đơn đặt phòng thực tế."

        # 2. Lấy thông tin loại phòng
        cursor.execute("SELECT room_type_code FROM Dim_RoomType WHERE room_type_id = ?", (room_type_id,))
        rt_row = cursor.fetchone()
        if not rt_row:
            return False, {}, "Không tìm thấy loại phòng tương ứng."
        room_type_code = rt_row['room_type_code']

        # 3. Lấy hạng thành viên của khách hàng
        cursor.execute("SELECT tier FROM Customer_Profiles WHERE account_id = ?", (customer_account_id,))
        profile_row = cursor.fetchone()
        membership_tier = profile_row['tier'] if profile_row and profile_row['tier'] else 'Newbie'

        # 4. Tính toán giá phòng qua Pricing Service
        price_res = calculate_booking_price(cursor, room_type_id, room_type_code, list_of_nights, adults, children)
        if not price_res.get('allowed'):
            return False, {}, price_res.get('message', 'Chính sách phòng không phù hợp số khách.')

        standard_base_total = price_res['base_room_total']
        locked_unit_price = data.get('locked_unit_price') or data.get('unit_price')

        if locked_unit_price and float(locked_unit_price) > 0:
            base_room_total = int(round(float(locked_unit_price))) * len(list_of_nights)
            discount_amount = max(0, standard_base_total - base_room_total)
            total_after_promo = base_room_total
        else:
            base_room_total = standard_base_total
            # Kiểm tra khuyến mãi tự động hoặc hạng thành viên nếu không truyền mã ưu đãi cụ thể
            promo_p, promo_c = get_promo_price_for_date(
                cursor, standard_base_total // len(list_of_nights), room_type_code, checkin_date_str, membership_tier, hotel_id
            )
            if membership_tier == 'Gold':
                promo_p = int(round(promo_p * 0.95))

            calculated_promo_total = promo_p * len(list_of_nights)
            if calculated_promo_total < standard_base_total and not promo_code:
                base_room_total = calculated_promo_total
                total_after_promo = calculated_promo_total
                discount_amount = standard_base_total - calculated_promo_total
            else:
                # 5. Áp dụng mã khuyến mãi qua Promotion Service
                is_promo_valid, discount_amount, total_after_promo, promo_msg = validate_and_apply_promo(
                    cursor, promo_code, membership_tier, base_room_total, checkin_date_str, atomic_increment=True
                )
                if not is_promo_valid:
                    conn.rollback()
                    if raise_on_error:
                        raise PromotionInvalidError(promo_msg)
                    return False, {}, promo_msg

        # 6. Tính thuế GTGT (VAT 10%) và tiền đặt cọc (VND nguyên)
        tax_amount = int(round(total_after_promo * DEFAULT_TAX_RATE))
        final_total = total_after_promo + tax_amount

        if payment_type == 'deposit':
            deposit_paid = int(round(final_total * 0.5))
        else:
            deposit_paid = final_total

        # 7. Insert Booking_Master
        cursor.execute("""
            INSERT INTO Booking_Master (
                customer_id, hotel_id, room_type_id, physical_room_id,
                arrival_date, departure_date, nights, guests, adults, children, babies,
                total_amount, deposit_paid, tax_amount, discount_amount,
                booking_status, booking_type, special_requests, promo_code, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed', ?, ?, ?, datetime('now'))
        """, (customer_account_id, hotel_id, room_type_id, physical_room_id,
              checkin_date_str, checkout_date_str, len(list_of_nights),
              adults + children, adults, children, babies,
              final_total, deposit_paid, tax_amount, discount_amount,
              booking_type, special_requests, promo_code))
        new_booking_id = cursor.lastrowid

        # 8. Sinh và lưu Invoices
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{new_booking_id:06d}"
        cursor.execute("""
            INSERT INTO Invoices (booking_id, invoice_number, issued_at, total_amount, payment_method)
            VALUES (?, ?, datetime('now'), ?, ?)
        """, (new_booking_id, invoice_number, final_total, payment_method))
        new_invoice_id = cursor.lastrowid

        # 9. Lưu Marketing Attributions
        cursor.execute("""
            INSERT INTO Booking_Attributions (booking_id, source_channel, utm_campaign, utm_medium, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (new_booking_id, source_channel, utm_campaign, utm_medium))

        # 10. Lưu Booking_Nights cho từng đêm
        for night in list_of_nights:
            cursor.execute("""
                INSERT INTO Booking_Nights (booking_id, physical_room_id, night_date, created_at)
                VALUES (?, ?, ?, datetime('now'))
            """, (new_booking_id, physical_room_id, night))

        # 11. Lưu Giao dịch thanh toán (Payments) liên kết CHUẨN XÁC với invoice_id
        cursor.execute("""
            INSERT INTO Payments (booking_id, invoice_id, user_id, amount, payment_method, payment_status, payment_date)
            VALUES (?, ?, ?, ?, ?, 'Completed', datetime('now'))
        """, (new_booking_id, new_invoice_id, customer_account_id, deposit_paid, payment_method))

        # 12. Cộng điểm tích lũy Loyalty Points cho khách hàng
        if customer_account_id:
            earned_points = len(list_of_nights) * 10
            cursor.execute("SELECT loyalty_points FROM Customer_Profiles WHERE account_id = ?", (customer_account_id,))
            prof = cursor.fetchone()
            if prof:
                curr_pts = prof['loyalty_points'] or 0
                new_pts = curr_pts + earned_points
                new_tier = calculate_loyalty_tier(new_pts)
                cursor.execute("""
                    UPDATE Customer_Profiles
                    SET loyalty_points = ?, tier = ?
                    WHERE account_id = ?
                """, (new_pts, new_tier, customer_account_id))

        # 13. Giải phóng / Chuyển đổi Khóa giữ chỗ (RoomHoldLocks & Room_Lock)
        if hold_id:
            cursor.execute("UPDATE RoomHoldLocks SET status = 'converted' WHERE hold_id = ?", (hold_id,))
        if session_id:
            cursor.execute("UPDATE RoomHoldLocks SET status = 'converted' WHERE session_id = ? AND status = 'active'", (session_id,))
            cursor.execute("DELETE FROM Room_Lock WHERE session_id = ?", (session_id,))
        if physical_room_id:
            cursor.execute("DELETE FROM Room_Lock WHERE physical_room_id = ?", (physical_room_id,))

        conn.commit()

        result = {
            'booking_id': new_booking_id,
            'invoice_number': invoice_number,
            'total_amount': final_total,
            'deposit_paid': deposit_paid,
            'tax_amount': tax_amount,
            'discount_amount': discount_amount,
            'nights': len(list_of_nights),
            'status': 'Confirmed'
        }
        return True, result, "Đặt phòng trực tuyến thành công!"
    except (RoomAlreadyLockedError, RoomNotAvailableError, PromotionInvalidError):
        conn.rollback()
        if raise_on_error:
            raise
        raise
    except Exception as e:
        conn.rollback()
        if raise_on_error:
            raise
        return False, {}, f"Lỗi tạo đơn đặt phòng: {str(e)}"
    finally:
        conn.close()


def create_walkin_booking(data: Dict[str, Any], staff_account_id: Optional[int] = None, raise_on_error: bool = False) -> Tuple[bool, Dict[str, Any], str]:
    """
    Tạo đơn đặt phòng tại quầy cho Lễ tân (Walk-in) mà KHÔNG cần tạo tài khoản Customer:
    - customer_id được gán NULL
    - Lưu guest_name, guest_phone trực tiếp vào Booking_Master
    - Không sinh email rác {phone}@walkin.local
    - Tạo đầy đủ Booking_Master, Booking_Nights, Invoices, Payments
    """
    guest_name = (data.get('customer_name') or data.get('guest_name') or '').strip()
    guest_phone = (data.get('customer_phone') or data.get('guest_phone') or '').strip()
    guest_email = (data.get('guest_email') or '').strip()
    hotel_id = data.get('hotel_id') or 1
    room_type_id = data.get('room_type_id')
    physical_room_id = data.get('physical_room_id')
    checkin_date_str = data.get('checkin_date') or data.get('arrival_date') or ''
    checkout_date_str = data.get('checkout_date') or data.get('departure_date') or ''
    adults = int(data.get('adults', 1))
    children = int(data.get('children', 0))
    deposit_paid = int(round(float(data.get('deposit_paid', 0))))
    payment_method = data.get('payment_method', 'cash')
    special_requests = data.get('special_requests', '').strip()

    if not guest_name or not guest_phone or not physical_room_id:
        return False, {}, "Vui lòng nhập họ tên, số điện thoại khách hàng và chọn phòng vật lý."

    try:
        ci_dt = datetime.strptime(checkin_date_str, '%Y-%m-%d').date()
        co_dt = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
        if ci_dt >= co_dt:
            return False, {}, "Ngày nhận phòng phải trước ngày trả phòng."
    except ValueError:
        return False, {}, "Định dạng ngày nhận/trả phòng không hợp lệ."

    list_of_nights = []
    curr = ci_dt
    while curr < co_dt:
        list_of_nights.append(curr.strftime('%Y-%m-%d'))
        curr += timedelta(days=1)

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Kiểm tra phòng trống cho các đêm
        available, reason = is_room_available_for_nights(cursor, physical_room_id, list_of_nights)
        if not available:
            if raise_on_error:
                raise RoomNotAvailableError(reason or "Phòng đã có đơn đặt phòng thực tế.")
            return False, {}, reason

        # 2. Lấy room_type nếu chưa có
        if not room_type_id:
            cursor.execute("SELECT room_type_id FROM Physical_Room WHERE physical_room_id = ?", (physical_room_id,))
            pr_row = cursor.fetchone()
            if not pr_row:
                return False, {}, "Không tìm thấy phòng vật lý."
            room_type_id = pr_row['room_type_id']

        cursor.execute("SELECT room_type_code FROM Dim_RoomType WHERE room_type_id = ?", (room_type_id,))
        rt_row = cursor.fetchone()
        room_type_code = rt_row['room_type_code'] if rt_row else ''

        # 3. Tính tiền
        price_res = calculate_booking_price(cursor, room_type_id, room_type_code, list_of_nights, adults, children)
        if not price_res.get('allowed'):
            return False, {}, price_res.get('message', 'Chính sách phòng không phù hợp số khách.')

        base_total = price_res['base_room_total']
        tax_amount = int(round(base_total * DEFAULT_TAX_RATE))
        final_total = base_total + tax_amount

        # Mặc định nếu lễ tân không nhập deposit thì coi như thanh toán toàn bộ
        if deposit_paid <= 0:
            deposit_paid = final_total

        # 4. Insert Booking_Master (customer_id = NULL)
        cursor.execute("""
            INSERT INTO Booking_Master (
                customer_id, guest_name, guest_phone, guest_email,
                hotel_id, room_type_id, physical_room_id,
                arrival_date, departure_date, nights, guests, adults, children, babies,
                total_amount, deposit_paid, tax_amount, discount_amount,
                booking_status, booking_type, special_requests, created_at
            ) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, 0, 'Confirmed', 'continuous', ?, datetime('now'))
        """, (guest_name, guest_phone, guest_email,
              hotel_id, room_type_id, physical_room_id,
              checkin_date_str, checkout_date_str, len(list_of_nights),
              adults + children, adults, children,
              final_total, deposit_paid, tax_amount, special_requests))
        new_booking_id = cursor.lastrowid

        # 5. Insert Booking_Nights
        for night in list_of_nights:
            cursor.execute("""
                INSERT INTO Booking_Nights (booking_id, physical_room_id, night_date, created_at)
                VALUES (?, ?, ?, datetime('now'))
            """, (new_booking_id, physical_room_id, night))

        # 6. Sinh Invoice trước để lấy invoice_id
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{new_booking_id:06d}"
        cursor.execute("""
            INSERT INTO Invoices (booking_id, invoice_number, issued_at, total_amount, payment_method)
            VALUES (?, ?, datetime('now'), ?, ?)
        """, (new_booking_id, invoice_number, final_total, payment_method))
        new_invoice_id = cursor.lastrowid

        # 7. Insert Payments liên kết CHUẨN XÁC với invoice_id
        cursor.execute("""
            INSERT INTO Payments (booking_id, invoice_id, user_id, amount, payment_method, payment_status, payment_date)
            VALUES (?, ?, NULL, ?, ?, 'Completed', datetime('now'))
        """, (new_booking_id, new_invoice_id, deposit_paid, payment_method))

        # 8. Insert Booking_Attributions (nguồn walk-in)
        cursor.execute("""
            INSERT INTO Booking_Attributions (booking_id, source_channel, utm_campaign, utm_medium, created_at)
            VALUES (?, 'walkin', 'front_desk', '', datetime('now'))
        """, (new_booking_id,))

        conn.commit()

        result = {
            'booking_id': new_booking_id,
            'invoice_number': invoice_number,
            'guest_name': guest_name,
            'guest_phone': guest_phone,
            'total_amount': final_total,
            'deposit_paid': deposit_paid,
            'nights': len(list_of_nights),
            'status': 'Confirmed'
        }
        return True, result, "Tạo đơn đặt phòng Walk-in thành công."
    except Exception as e:
        conn.rollback()
        if raise_on_error:
            raise
        return False, {}, f"Lỗi tạo đơn walk-in: {str(e)}"
    finally:
        conn.close()


def cancel_booking(
    booking_id: int,
    reason: str = "",
    canceled_by_user_id: Optional[int] = None,
    canceled_by: Optional[int] = None,
    raise_on_error: bool = False
) -> Tuple[bool, Dict[str, Any], str]:
    """
    Hủy đơn đặt phòng theo chính sách hoàn tiền Refund_Policy:
    - Tính thời gian còn lại trước 14:00 ngày check-in để xác định % hoàn tiền
    - Cập nhật Booking_Master thành 'Canceled'
    - Lưu Cancellation_Records
    - Ghi nhận hoàn tiền trong Payments (số tiền âm)
    - Xóa các đêm trong Booking_Nights để giải phóng phòng
    """
    actor_id = canceled_by_user_id if canceled_by_user_id is not None else canceled_by
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT booking_id, customer_id, arrival_date, total_amount, deposit_paid, booking_status
            FROM Booking_Master WHERE booking_id = ?
        """, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            msg = f"Không tìm thấy đơn đặt phòng #{booking_id}."
            if raise_on_error:
                raise BookingNotFoundError(msg)
            return False, {}, msg

        current_status = (booking['booking_status'] or '').lower().replace(' ', '')
        if current_status in ('canceled', 'checked-out', 'checkedout'):
            msg = f"Đơn đặt phòng #{booking_id} ở trạng thái '{booking['booking_status']}' không thể hủy."
            if raise_on_error:
                raise InvalidBookingStateError(msg)
            return False, {}, msg

        # Tính chính sách hoàn tiền
        checkin_dt = datetime.strptime(f"{booking['arrival_date']} 14:00:00", '%Y-%m-%d %H:%M:%S')
        hours_remaining = (checkin_dt - datetime.now()).total_seconds() / 3600.0

        cursor.execute("""
            SELECT refund_percent FROM Refund_Policy
            WHERE hours_before_checkin <= ?
            ORDER BY hours_before_checkin DESC
            LIMIT 1
        """, (hours_remaining,))
        pol = cursor.fetchone()
        refund_percent = float(pol['refund_percent']) if pol else 0.0

        deposit_paid = booking['deposit_paid'] or 0
        refund_amount = int(round(deposit_paid * (refund_percent / 100.0)))

        # 1. Cập nhật Booking_Master
        cursor.execute("""
            UPDATE Booking_Master
            SET booking_status = 'Canceled'
            WHERE booking_id = ?
        """, (booking_id,))

        # 2. Ghi Cancellation_Records
        cursor.execute("""
            INSERT INTO Cancellation_Records (booking_id, cancel_reason, canceled_by, refund_amount, refund_percent, canceled_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(booking_id) DO UPDATE SET
                cancel_reason = excluded.cancel_reason,
                canceled_by = excluded.canceled_by,
                refund_amount = excluded.refund_amount,
                refund_percent = excluded.refund_percent,
                canceled_at = datetime('now')
        """, (booking_id, reason or 'Khách hàng hủy phòng', actor_id, refund_amount, refund_percent))

        # 3. Ghi nhận giao dịch hoàn tiền nếu có
        if refund_amount > 0:
            cursor.execute("""
                INSERT INTO Payments (booking_id, user_id, amount, payment_method, payment_status, payment_date)
                VALUES (?, ?, ?, 'refund', 'Refunded', datetime('now'))
            """, (booking_id, booking['customer_id'], -refund_amount))

        # 4. Xóa Booking_Nights để mở lại phòng trống
        cursor.execute("DELETE FROM Booking_Nights WHERE booking_id = ?", (booking_id,))

        conn.commit()

        result = {
            'booking_id': booking_id,
            'refund_percent': refund_percent,
            'refund_amount': refund_amount,
            'status': 'Canceled'
        }
        return True, result, "Hủy đặt phòng thành công."
    except (BookingNotFoundError, InvalidBookingStateError):
        conn.rollback()
        if raise_on_error:
            raise
        raise
    except Exception as e:
        conn.rollback()
        if raise_on_error:
            raise
        return False, {}, f"Lỗi khi hủy phòng: {str(e)}"
    finally:
        conn.close()


def checkin_booking(booking_id: int, staff_account_id: Optional[int] = None) -> Tuple[bool, str]:
    """
    Lễ tân thực hiện Check-in:
    - Kiểm tra ngày nhận phòng
    - Kiểm tra phòng vật lý phải ở trạng thái Clean
    - Đổi trạng thái Booking_Master thành Checked-in
    - Đổi trạng thái Physical_Room thành Occupied
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.physical_room_id, bm.arrival_date, bm.booking_status,
                   pr.housekeeping_status
            FROM Booking_Master bm
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            WHERE bm.booking_id = ?
        """, (booking_id,))
        b = cursor.fetchone()

        if not b:
            return False, "Không tìm thấy đơn đặt phòng."

        if b['booking_status'] == 'Checked-in':
            return False, "Đơn đặt phòng này đã hoàn tất check-in."

        if b['booking_status'] in ('Canceled', 'No-Show'):
            return False, f"Không thể check-in đơn ở trạng thái {b['booking_status']}."

        today_str = date.today().strftime('%Y-%m-%d')
        if today_str < b['arrival_date']:
            return False, f"Chưa tới ngày nhận phòng ({b['arrival_date']})."

        if b['physical_room_id'] and b['housekeeping_status'] != 'Clean':
            return False, f"Không thể giao khóa! Phòng chưa ở trạng thái Sạch (Hiện tại: {b['housekeeping_status']})."

        cursor.execute("UPDATE Booking_Master SET booking_status = 'Checked-in' WHERE booking_id = ?", (booking_id,))
        if b['physical_room_id']:
            cursor.execute("UPDATE Physical_Room SET housekeeping_status = 'Occupied' WHERE physical_room_id = ?", (b['physical_room_id'],))

        conn.commit()
        return True, "Check-in thành công."
    except Exception as e:
        conn.rollback()
        return False, f"Lỗi trong quá trình check-in: {str(e)}"
    finally:
        conn.close()


def move_booking_room(booking_id: int, new_physical_room_id: int) -> Tuple[bool, str]:
    """
    Đổi phòng cho đơn đặt phòng:
    - Kiểm tra phòng mới có sẵn sàng cho tất cả các đêm của đơn không
    - Cập nhật Booking_Master.physical_room_id và Booking_Nights.physical_room_id
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.room_type_id, bm.physical_room_id, bm.booking_status
            FROM Booking_Master bm WHERE bm.booking_id = ?
        """, (booking_id,))
        b = cursor.fetchone()
        if not b:
            return False, "Không tìm thấy đơn đặt phòng."

        cursor.execute("SELECT physical_room_id, room_type_id FROM Physical_Room WHERE physical_room_id = ?", (new_physical_room_id,))
        new_room = cursor.fetchone()
        if not new_room:
            return False, "Phòng vật lý mới không tồn tại."

        if b['room_type_id'] != new_room['room_type_id']:
            return False, "Chỉ có thể đổi sang phòng cùng hạng loại phòng."

        cursor.execute("SELECT night_date FROM Booking_Nights WHERE booking_id = ?", (booking_id,))
        nights = [r['night_date'] for r in cursor.fetchall()]
        if not nights:
            return False, "Đơn đặt phòng không có đêm nào để chuyển phòng."

        # Kiểm tra tính khả dụng phòng mới
        available, reason = is_room_available_for_nights(cursor, new_physical_room_id, nights)
        if not available:
            return False, f"Không thể chuyển sang phòng mới: {reason}"

        old_room_id = b['physical_room_id']
        cursor.execute("UPDATE Booking_Master SET physical_room_id = ? WHERE booking_id = ?", (new_physical_room_id, booking_id))
        cursor.execute("UPDATE Booking_Nights SET physical_room_id = ? WHERE booking_id = ?", (new_physical_room_id, booking_id))

        if old_room_id:
            cursor.execute("UPDATE Physical_Room SET housekeeping_status = 'Dirty' WHERE physical_room_id = ?", (old_room_id,))
        cursor.execute("UPDATE Physical_Room SET housekeeping_status = 'Occupied' WHERE physical_room_id = ?", (new_physical_room_id,))

        conn.commit()
        return True, "Chuyển phòng thành công."
    except Exception as e:
        conn.rollback()
        return False, f"Lỗi chuyển phòng: {str(e)}"
    finally:
        conn.close()


def add_extra_service(booking_id: int, service_name: str, quantity: int, unit_price: int, added_by: Optional[int] = None) -> Tuple[bool, Dict[str, Any], str]:
    """Thêm dịch vụ phát sinh cho đơn đặt phòng (VND nguyên)."""
    if quantity <= 0 or unit_price < 0:
        return False, {}, "Số lượng hoặc đơn giá không hợp lệ."

    total_price = quantity * unit_price
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Extra_Services (booking_id, service_name, quantity, unit_price, total_price, added_by, added_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (booking_id, service_name, quantity, unit_price, total_price, added_by))
        new_id = cursor.lastrowid

        # TỰ ĐỘNG ĐỒNG BỘ HÓA ĐƠN INVOICES (Single Source of Truth)
        folio_res = recalculate_folio_invoice(cursor, booking_id)

        conn.commit()
        return True, {
            'service_id': new_id,
            'total_price': total_price,
            'updated_invoice_total': folio_res.get('total_final'),
            'remaining_balance': folio_res.get('remaining_balance')
        }, "Thêm dịch vụ phát sinh và đồng bộ hóa đơn thành công."
    except Exception as e:
        conn.rollback()
        return False, {}, f"Lỗi thêm dịch vụ: {str(e)}"
    finally:
        conn.close()


# ─── REPOSITORIES / QUERY HELPERS ─────────────────────────────────────────────

def get_bookings_list(user_id: int, role: str, status_filter: str = '', page: int = 1, per_page: int = 20, return_total: bool = False):
    """Truy vấn danh sách đơn đặt phòng kèm phân trang và lọc trạng thái thời gian thực."""
    offset = (page - 1) * per_page
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        if role in ('Admin', 'Manager', 'Receptionist'):
            where_sql = "WHERE 1=1"
            params = []
        else:
            where_sql = "WHERE bm.customer_id = ?"
            params = [user_id]

        today_str = datetime.now().strftime('%Y-%m-%d')
        if status_filter in ('canceled', 'Canceled'):
            where_sql += " AND bm.booking_status = 'Canceled'"
        elif status_filter == 'active':
            where_sql += " AND bm.booking_status NOT IN ('Canceled', 'Checked-out', 'No-Show')"
        elif status_filter == 'today_arrivals':
            where_sql += f" AND bm.arrival_date = '{today_str}' AND bm.booking_status = 'Confirmed'"
        elif status_filter == 'today_departures':
            where_sql += f" AND bm.departure_date = '{today_str}' AND bm.booking_status = 'Checked-In'"
        elif status_filter == 'overdue':
            where_sql += f" AND bm.departure_date < '{today_str}' AND bm.booking_status = 'Confirmed'"
        elif status_filter in ('Checked-In', 'inhouse'):
            where_sql += " AND bm.booking_status = 'Checked-In'"
        elif status_filter:
            where_sql += " AND bm.booking_status = ?"
            params.append(status_filter)

        # Đếm tổng số bản ghi phục vụ phân trang
        cursor.execute(f"SELECT COUNT(*) AS total FROM Booking_Master bm {where_sql}", params)
        total_count = cursor.fetchone()['total']

        cursor.execute(f"""
            SELECT bm.booking_id, bm.customer_id AS user_id,
                   COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_full_name,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_name,
                   COALESCE(bm.guest_phone, cp.phone, '') AS customer_phone,
                   bm.hotel_id, dh.hotel AS hotel_name,
                   bm.room_type_id, drt.room_type_code,
                   bm.physical_room_id, pr.room_name AS physical_room_name, pr.housekeeping_status,
                   bm.arrival_date, bm.arrival_date AS checkin_date,
                   bm.departure_date, bm.departure_date AS checkout_date,
                   bm.nights,
                   bm.adults, bm.children, bm.babies,
                   bm.total_amount AS total_price, bm.deposit_paid, bm.tax_amount,
                   CASE WHEN bm.booking_status = 'Canceled' THEN 1 ELSE 0 END AS is_canceled,
                   bm.booking_status AS status, bm.booking_status AS status_detail,
                   bm.booking_type, '' AS selected_nights,
                   bm.promo_code, bm.discount_amount, bm.created_at
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Dim_Hotel dh ON bm.hotel_id = dh.hotel_id
            LEFT JOIN Dim_RoomType drt ON bm.room_type_id = drt.room_type_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            {where_sql}
            ORDER BY bm.arrival_date DESC, bm.created_at DESC
            LIMIT ? OFFSET ?
        """, params + [per_page, offset])
        bookings = [dict(r) for r in cursor.fetchall()]
        if return_total:
            return bookings, total_count
        return bookings
    finally:
        conn.close()


def search_bookings(keyword: str) -> List[Dict[str, Any]]:
    """Tìm kiếm đơn đặt phòng theo mã booking, email, tên hoặc SĐT khách."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.customer_id AS user_id,
                   COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_full_name,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_name,
                   COALESCE(bm.guest_phone, cp.phone, '') AS customer_phone,
                   bm.hotel_id, dh.hotel AS hotel_name,
                   bm.room_type_id, drt.room_type_code,
                   bm.physical_room_id, pr.room_name AS physical_room_name, pr.housekeeping_status,
                   bm.arrival_date, bm.arrival_date AS checkin_date,
                   bm.departure_date, bm.departure_date AS checkout_date,
                   bm.nights,
                   bm.total_amount AS total_price, bm.deposit_paid, bm.booking_status AS status_detail,
                   bm.booking_type, '' AS selected_nights,
                   CASE WHEN bm.booking_status = 'Canceled' THEN 1 ELSE 0 END AS is_canceled,
                   bm.special_requests
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Dim_Hotel dh ON bm.hotel_id = dh.hotel_id
            LEFT JOIN Dim_RoomType drt ON bm.room_type_id = drt.room_type_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            WHERE a.email LIKE ? OR cp.full_name LIKE ? OR sp.full_name LIKE ? OR bm.guest_name LIKE ?
               OR bm.guest_phone LIKE ? OR CAST(bm.booking_id AS TEXT) = ?
            ORDER BY bm.arrival_date DESC
            LIMIT 30
        """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', keyword))
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()


def get_active_bookings() -> List[Dict[str, Any]]:
    """Lấy danh sách các booking đang và sắp lưu trú cho Lễ tân."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.customer_id AS user_id,
                   COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_full_name,
                   bm.hotel_id, dh.hotel AS hotel_name,
                   bm.room_type_id, drt.room_type_code,
                   bm.physical_room_id, pr.room_name AS physical_room_name,
                   bm.arrival_date, bm.departure_date, bm.nights,
                   bm.total_amount AS total_price, bm.deposit_paid, bm.booking_status AS status_detail,
                   bm.booking_type, '' AS selected_nights,
                   CASE WHEN bm.booking_status = 'Canceled' THEN 1 ELSE 0 END AS is_canceled,
                   bm.special_requests
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Dim_Hotel dh ON bm.hotel_id = dh.hotel_id
            LEFT JOIN Dim_RoomType drt ON bm.room_type_id = drt.room_type_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            WHERE bm.booking_status NOT IN ('Canceled', 'Checked-out', 'No-Show')
            ORDER BY bm.arrival_date ASC
        """)
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()


def get_invoice_details(booking_id: int) -> Tuple[bool, Dict[str, Any], str]:
    """Lấy chi tiết hóa đơn, dịch vụ và thanh toán của đơn đặt phòng."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.customer_id AS user_id,
                   COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   COALESCE(cp.phone, bm.guest_phone, '') AS customer_phone,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_full_name,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_name,
                   bm.hotel_id, dh.hotel AS hotel_name,
                   bm.room_type_id, drt.room_type_code,
                   bm.physical_room_id, pr.room_name AS physical_room_name, pr.room_name,
                   bm.arrival_date, bm.departure_date,
                   bm.arrival_date AS checkin_date, bm.departure_date AS checkout_date,
                   bm.nights,
                   bm.total_amount AS total_price, bm.deposit_paid, bm.tax_amount, bm.discount_amount,
                   bm.booking_status AS status_detail, bm.booking_status AS status,
                   inv.invoice_number, inv.issued_at AS invoice_issued_at
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Dim_Hotel dh ON bm.hotel_id = dh.hotel_id
            LEFT JOIN Dim_RoomType drt ON bm.room_type_id = drt.room_type_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            LEFT JOIN Invoices inv ON bm.booking_id = inv.booking_id
            WHERE bm.booking_id = ?
        """, (booking_id,))
        b = cursor.fetchone()
        if not b:
            return False, {}, "Không tìm thấy đơn đặt phòng."

        cursor.execute("SELECT * FROM Extra_Services WHERE booking_id = ?", (booking_id,))
        extra_services = [dict(r) for r in cursor.fetchall()]

        cursor.execute("SELECT * FROM Payments WHERE booking_id = ?", (booking_id,))
        payments = [dict(r) for r in cursor.fetchall()]

        extra_grand_total = sum(s['total_price'] for s in extra_services)
        return True, {
            'booking': dict(b),
            'extra_services': extra_services,
            'payments': payments,
            'extra_grand_total': extra_grand_total
        }, ""
    finally:
        conn.close()


def get_cancel_preview(booking_id: int) -> Tuple[bool, Dict[str, Any], str]:
    """Xem trước phí hủy phòng."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.customer_id, bm.arrival_date, bm.total_amount, bm.deposit_paid,
                   bm.booking_status, COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách hàng') AS customer_name
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            WHERE bm.booking_id = ?
        """, (booking_id,))
        b = cursor.fetchone()
        if not b:
            return False, {}, "Không tìm thấy đơn đặt phòng."

        if b['booking_status'] in ('Canceled', 'No-Show', 'Checked-out'):
            return False, {}, f"Đơn đặt phòng đang ở trạng thái {b['booking_status']}, không thể hủy."

        checkin_dt = datetime.strptime(f"{b['arrival_date']} 14:00:00", '%Y-%m-%d %H:%M:%S')
        hours_remaining = (checkin_dt - datetime.now()).total_seconds() / 3600.0

        cursor.execute("""
            SELECT refund_percent FROM Refund_Policy
            WHERE hours_before_checkin <= ?
            ORDER BY hours_before_checkin DESC LIMIT 1
        """, (hours_remaining,))
        pol = cursor.fetchone()
        refund_percent = float(pol['refund_percent']) if pol else 0.0

        deposit_paid = b['deposit_paid'] or 0
        refund_amount = int(round(deposit_paid * (refund_percent / 100.0)))
        penalty_amount = max(0, deposit_paid - refund_amount)

        data = {
            'booking_id': booking_id,
            'arrival_date': b['arrival_date'],
            'total_price': b['total_amount'],
            'deposit_paid': deposit_paid,
            'refund_percent': refund_percent,
            'refund_amount': refund_amount,
            'penalty_amount': penalty_amount,
            'customer_name': b['customer_name']
        }
        return True, data, ""
    finally:
        conn.close()


def mark_noshow(booking_id: int) -> Tuple[bool, str]:
    """Đánh dấu No-Show cho đơn đặt phòng."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Booking_Master
            SET booking_status = 'No-Show'
            WHERE booking_id = ? AND booking_status = 'Confirmed'
        """, (booking_id,))
        if cursor.rowcount == 0:
            return False, "Đơn đặt phòng không ở trạng thái Confirmed để đánh dấu No-Show."

        cursor.execute("""
            INSERT INTO Cancellation_Records (booking_id, cancel_reason, canceled_at)
            VALUES (?, 'Khách không đến (No-Show)', datetime('now'))
            ON CONFLICT(booking_id) DO UPDATE SET cancel_reason = excluded.cancel_reason
        """, (booking_id,))

        cursor.execute("DELETE FROM Booking_Nights WHERE booking_id = ?", (booking_id,))
        conn.commit()
        return True, "Đã đánh dấu No-Show thành công."
    except Exception as e:
        conn.rollback()
        return False, f"Lỗi đánh dấu No-Show: {str(e)}"
    finally:
        conn.close()


def get_noshow_candidates() -> List[Dict[str, Any]]:
    """Lấy danh sách các đơn Confirmed có ngày nhận phòng <= hôm nay để lễ tân rà soát."""
    today_str = date.today().strftime('%Y-%m-%d')
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.arrival_date,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách hàng') AS customer_name,
                   COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   bm.hotel_id, dh.hotel AS hotel_name,
                   drt.room_type_code, pr.room_name AS physical_room_name
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Dim_Hotel dh ON bm.hotel_id = dh.hotel_id
            LEFT JOIN Dim_RoomType drt ON bm.room_type_id = drt.room_type_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            WHERE bm.booking_status = 'Confirmed' AND bm.arrival_date <= ?
            ORDER BY bm.arrival_date ASC
        """, (today_str,))
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()


def get_booking_by_id(booking_id: int) -> Optional[Dict[str, Any]]:
    """Lấy chi tiết đơn đặt phòng chuẩn 3NF kèm danh sách đêm Booking_Nights."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.*, COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách hàng') AS customer_name,
                   pr.room_name, rt.room_type_code, dh.hotel AS hotel_name,
                   inv.invoice_number
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            LEFT JOIN Dim_RoomType rt ON bm.room_type_id = rt.room_type_id
            LEFT JOIN Dim_Hotel dh ON bm.hotel_id = dh.hotel_id
            LEFT JOIN Invoices inv ON bm.booking_id = inv.booking_id
            WHERE bm.booking_id = ?
        """, (booking_id,))
        b = cursor.fetchone()
        if not b:
            return None
        res = dict(b)
        cursor.execute("""
            SELECT b_night_id, night_date, physical_room_id, night_price
            FROM Booking_Nights WHERE booking_id = ? ORDER BY night_date
        """, (booking_id,))
        res['nights_details'] = [dict(r) for r in cursor.fetchall()]
        return res
    finally:
        conn.close()


def get_room_plan_matrix(start_date_str: Optional[str] = None, number_of_days: int = 7) -> Dict[str, Any]:
    """Tạo ma trận sơ đồ phòng Gantt cho Lễ tân theo dõi tình trạng buồng phòng."""
    start_dt = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else date.today()
    list_of_dates = [(start_dt + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(number_of_days)]

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pr.physical_room_id, pr.room_name, pr.housekeeping_status,
                   drt.room_type_id, drt.room_type_code, drt.hotel_id, drt.base_price, dh.hotel AS hotel_name
            FROM Physical_Room pr
            JOIN Dim_RoomType drt ON pr.room_type_id = drt.room_type_id
            LEFT JOIN Dim_Hotel dh ON drt.hotel_id = dh.hotel_id
            WHERE pr.is_active = 1
            ORDER BY dh.hotel_id, drt.room_type_code, pr.room_name
        """)
        all_rooms = cursor.fetchall()

        # Lấy thông tin các booking đêm tương ứng từ Booking_Nights
        end_date_str = list_of_dates[-1]
        cursor.execute("""
            SELECT bn.physical_room_id, bn.night_date, bn.booking_id,
                   bm.booking_status, COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách hàng') AS customer_name
            FROM Booking_Nights bn
            JOIN Booking_Master bm ON bn.booking_id = bm.booking_id
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            WHERE bm.booking_status NOT IN ('Canceled', 'No-Show')
              AND bn.night_date >= ? AND bn.night_date <= ?
        """, (list_of_dates[0], end_date_str))
        night_rows = cursor.fetchall()

        # Tạo map tra cứu nhanh (physical_room_id, night_date) -> booking
        lookup = {(nr['physical_room_id'], nr['night_date']): nr for nr in night_rows}

        room_plan_data = []
        for r in all_rooms:
            pid = r['physical_room_id']
            cells = {}
            for d_str in list_of_dates:
                b_info = lookup.get((pid, d_str))
                if b_info:
                    cell_status = b_info['booking_status']
                    booking_meta = {
                        'booking_id': b_info['booking_id'],
                        'customer_name': b_info['customer_name']
                    }
                else:
                    cell_status = r['housekeeping_status'] if r['housekeeping_status'] in ('Dirty', 'Maintenance') else 'empty'
                    booking_meta = None

                cells[d_str] = {'status': cell_status, 'booking': booking_meta}

            room_plan_data.append({
                'physical_room_id': pid,
                'room_name': r['room_name'],
                'room_type_id': r['room_type_id'],
                'room_type_code': r['room_type_code'],
                'base_price': r['base_price'],
                'hotel_name': r['hotel_name'],
                'housekeeping_status': r['housekeeping_status'],
                'cells': cells
            })

        return {'dates': list_of_dates, 'room_plan': room_plan_data}
    finally:
        conn.close()

# ─── BACKWARD COMPATIBILITY ALIASES ───────────────────────────────────────────
from services.pricing_service import evaluate_room_occupancy as evaluate_occupancy_policy

def get_effective_price_for_date(cursor, room_type_id, room_type_code, target_date_str):
    return get_effective_daily_price(cursor, room_type_id, room_type_code, target_date_str)

def get_promo_price_for_date(cursor, effective_price, room_type_code, target_date_str, membership_tier='Newbie', hotel_id=1):
    ok, disc, final_p, _ = validate_and_apply_promo(cursor, '', membership_tier, effective_price, target_date_str, atomic_increment=False)
    # Tìm khuyến mãi scope
    cursor.execute("""
        SELECT discount_percent, discount_type, code FROM Promotions
        WHERE active = 1 AND (start_date IS NULL OR start_date <= ?) AND (end_date IS NULL OR end_date >= ?)
          AND (apply_scope = 'all' OR (apply_scope = 'room_type' AND scope_value = ?))
        ORDER BY discount_percent DESC LIMIT 1
    """, (target_date_str, target_date_str, room_type_code))
    row = cursor.fetchone()
    if not row:
        return effective_price, None
    if row['discount_type'] == 'fixed':
        promo_p = max(0, effective_price - int(round(row['discount_percent'])))
    else:
        promo_p = int(round(effective_price * (1 - row['discount_percent'] / 100.0)))
    return promo_p, row['code']

def is_night_occupied(cursor, physical_room_id, night_date_str):
    from services.room_lock_service import is_room_available_for_nights
    avail, _ = is_room_available_for_nights(cursor, physical_room_id, [night_date_str])
    return not avail

def calculate_booking_total_for_nights(cursor, room_type_id, room_type_code, list_of_nights, membership_tier='Newbie', hotel_id=1, adults=1, children=0):
    res = calculate_booking_price(cursor, room_type_id, room_type_code, list_of_nights, adults, children)
    if not res.get('allowed'):
        return None, None
    return res['base_room_total'], res['base_room_total']

def get_refund_amount_by_hours(conn, arrival_date_str, total_paid):
    cursor = conn.cursor()
    checkin_dt = datetime.strptime(f"{arrival_date_str} 14:00:00", '%Y-%m-%d %H:%M:%S')
    hours = (checkin_dt - datetime.now()).total_seconds() / 3600.0
    cursor.execute("SELECT refund_percent FROM Refund_Policy WHERE hours_before_checkin <= ? ORDER BY hours_before_checkin DESC LIMIT 1", (hours,))
    row = cursor.fetchone()
    pct = float(row['refund_percent']) if row else 0.0
    ref_amt = int(round(total_paid * (pct / 100.0)))
    return pct, ref_amt
