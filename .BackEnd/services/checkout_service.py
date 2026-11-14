"""
Checkout Service - Quyết toán trả phòng, tính tiền dịch vụ phát sinh, xuất hóa đơn và chuyển phòng sang Dirty.
Kiến trúc: Clean Service Layer
"""

from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from database import get_db_connection
from services.exceptions import BookingNotFoundError, InvalidBookingStateError


def calculate_loyalty_tier(total_points: int) -> str:
    """Xác định hạng thành viên dựa trên tổng điểm thưởng tích lũy."""
    if total_points >= 210:
        return 'Gold'
    elif total_points >= 50:
        return 'Silver'
    return 'Newbie'


def recalculate_folio_invoice(cursor, booking_id: int) -> Dict[str, Any]:
    """
    Tự động tính toán lại và đồng bộ hóa đơn Invoices cho đơn đặt phòng:
    Single Source of Truth cho toàn bộ nghiệp vụ kế toán Folio.
    """
    # 1. Lấy thông tin phòng và tiền cọc từ Booking_Master
    cursor.execute("""
        SELECT total_amount, deposit_paid, customer_id
        FROM Booking_Master WHERE booking_id = ?
    """, (booking_id,))
    bm = cursor.fetchone()
    if not bm:
        return {}

    # 2. Lấy tổng tiền dịch vụ phát sinh từ Extra_Services
    cursor.execute("""
        SELECT COALESCE(SUM(total_price), 0) AS extra_total
        FROM Extra_Services WHERE booking_id = ?
    """, (booking_id,))
    extra_total = cursor.fetchone()['extra_total']

    total_final = (bm['total_amount'] or 0) + extra_total
    deposit_paid = bm['deposit_paid'] or 0
    remaining_balance = max(0, total_final - deposit_paid)

    # 3. Đảm bảo bản ghi Invoices luôn tồn tại và cập nhật total_amount
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{booking_id:06d}"
    cursor.execute("""
        INSERT INTO Invoices (booking_id, invoice_number, issued_at, total_amount, payment_method)
        VALUES (?, ?, datetime('now'), ?, 'pending')
        ON CONFLICT(booking_id) DO UPDATE SET
            total_amount = excluded.total_amount
    """, (booking_id, invoice_number, total_final))

    # Lấy invoice_id
    cursor.execute("SELECT invoice_id, invoice_number FROM Invoices WHERE booking_id = ?", (booking_id,))
    inv_row = cursor.fetchone()
    inv_id = inv_row['invoice_id'] if inv_row else None

    return {
        'invoice_id': inv_id,
        'invoice_number': inv_row['invoice_number'] if inv_row else invoice_number,
        'room_total': bm['total_amount'],
        'extra_services_total': extra_total,
        'total_final': total_final,
        'deposit_paid': deposit_paid,
        'remaining_balance': remaining_balance
    }



def get_checkout_statement(booking_id: int, raise_on_error: bool = False) -> Dict[str, Any]:
    """
    Lấy bảng kê quyết toán trả phòng:
    - Tiền phòng gốc & tiền cọc đã thanh toán
    - Tổng hợp danh mục phụ thu từ Extra_Services
    - Số tiền còn thiếu cần quyết toán
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.customer_id,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS guest_name,
                   COALESCE(cp.full_name, sp.full_name, bm.guest_name, 'Khách vãng lai') AS customer_name,
                   COALESCE(cp.phone, bm.guest_phone, '') AS guest_phone,
                   COALESCE(cp.phone, bm.guest_phone, '') AS customer_phone,
                   COALESCE(a.email, bm.guest_email, '') AS customer_email,
                   bm.hotel_id, bm.room_type_id, bm.physical_room_id,
                   bm.arrival_date, bm.departure_date,
                   bm.arrival_date AS checkin_date, bm.departure_date AS checkout_date,
                   bm.nights,
                   bm.total_amount, bm.deposit_paid, bm.tax_amount, bm.discount_amount,
                   bm.booking_status, pr.room_name, rt.room_type_code
            FROM Booking_Master bm
            LEFT JOIN Accounts a ON bm.customer_id = a.account_id
            LEFT JOIN Customer_Profiles cp ON bm.customer_id = cp.account_id
            LEFT JOIN Staff_Profiles sp ON bm.customer_id = sp.account_id
            LEFT JOIN Physical_Room pr ON bm.physical_room_id = pr.physical_room_id
            LEFT JOIN Dim_RoomType rt ON bm.room_type_id = rt.room_type_id
            WHERE bm.booking_id = ?
        """, (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            if raise_on_error:
                raise BookingNotFoundError(f"Không tìm thấy đơn đặt phòng #{booking_id}.")
            return {}

        # Lấy danh sách dịch vụ phát sinh từ Extra_Services
        cursor.execute("""
            SELECT service_id, service_name, quantity, unit_price, total_price, added_at
            FROM Extra_Services
            WHERE booking_id = ?
        """, (booking_id,))
        services = [dict(r) for r in cursor.fetchall()]
        extra_services_total = sum(s['total_price'] for s in services)

        total_payable = booking['total_amount'] + extra_services_total
        remaining_balance = max(0, total_payable - (booking['deposit_paid'] or 0))

        return {
            'booking_id': booking['booking_id'],
            'customer_id': booking['customer_id'],
            'guest_name': booking['guest_name'],
            'customer_name': booking['customer_name'],
            'guest_phone': booking['guest_phone'],
            'customer_phone': booking['customer_phone'],
            'customer_email': booking['customer_email'],
            'room_name': booking['room_name'],
            'physical_room_id': booking['physical_room_id'],
            'room_type_code': booking['room_type_code'],
            'arrival_date': booking['arrival_date'],
            'departure_date': booking['departure_date'],
            'checkin_date': booking['checkin_date'],
            'checkout_date': booking['checkout_date'],
            'nights': booking['nights'],
            'booking_status': booking['booking_status'],
            'room_total_amount': booking['total_amount'],
            'deposit_paid': booking['deposit_paid'],
            'extra_services': services,
            'extra_services_total': extra_services_total,
            'total_payable': total_payable,
            'remaining_balance': remaining_balance
        }
    finally:
        conn.close()


def get_checkout_summary(booking_id: int) -> Tuple[bool, Dict[str, Any], str]:
    """Tương thích ngược: get_checkout_summary trả về Tuple (success, data, msg)."""
    statement = get_checkout_statement(booking_id, raise_on_error=False)
    if not statement:
        return False, {}, f"Không tìm thấy đơn đặt phòng #{booking_id}."
    return True, statement, ""


def process_checkout(
    booking_id: int,
    staff_user_id: Optional[int] = None,
    payment_method: str = 'cash',
    raise_on_error: bool = False
) -> Tuple[bool, Dict[str, Any], str]:
    """
    Thực hiện quyết toán trả phòng trong 1 Database Transaction:
    1. Kiểm tra trạng thái đơn đặt phòng.
    2. Thu tiền phần còn lại (nếu có) và ghi vào Payments.
    3. Đổi trạng thái Booking_Master thành 'Checked-Out'.
    4. Đổi trạng thái Physical_Room thành 'Dirty' (chờ buồng phòng dọn dẹp).
    5. Tạo/Cập nhật Invoice chính thức dạng 'INV-YYYYMMDD-{booking_id:06d}'.
    6. Cộng điểm tích lũy thành viên (Loyalty Points) nếu là khách có tài khoản.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bm.booking_id, bm.customer_id, bm.physical_room_id, bm.nights,
                   bm.total_amount, bm.deposit_paid, bm.booking_status
            FROM Booking_Master bm
            WHERE bm.booking_id = ?
        """, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            msg = f"Không tìm thấy đơn đặt phòng #{booking_id}."
            if raise_on_error:
                raise BookingNotFoundError(msg)
            return False, {}, msg

        current_status = (booking['booking_status'] or '').lower().replace(' ', '')
        if current_status in ('canceled', 'checked-out', 'checkedout'):
            msg = f"Không thể check-out đơn ở trạng thái '{booking['booking_status']}'."
            if raise_on_error:
                raise InvalidBookingStateError(msg)
            return False, {}, msg

        # Tính tổng tiền dịch vụ phát sinh từ Extra_Services
        cursor.execute("""
            SELECT COALESCE(SUM(total_price), 0) AS extra_total
            FROM Extra_Services WHERE booking_id = ?
        """, (booking_id,))
        extra_services_total = cursor.fetchone()['extra_total']

        total_final = booking['total_amount'] + extra_services_total
        remaining_balance = max(0, total_final - (booking['deposit_paid'] or 0))

        # 1. Xuất / Cập nhật Hóa đơn (Invoices) chuẩn INV-YYYYMMDD-{booking_id:06d}
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{booking_id:06d}"
        cursor.execute("""
            INSERT INTO Invoices (booking_id, invoice_number, issued_at, total_amount, payment_method)
            VALUES (?, ?, datetime('now'), ?, ?)
            ON CONFLICT(booking_id) DO UPDATE SET
                total_amount = excluded.total_amount,
                payment_method = excluded.payment_method,
                issued_at = datetime('now')
        """, (booking_id, invoice_number, total_final, payment_method))

        cursor.execute("SELECT invoice_id FROM Invoices WHERE booking_id = ?", (booking_id,))
        inv_row = cursor.fetchone()
        invoice_id = inv_row['invoice_id'] if inv_row else None

        # 2. Ghi nhận thanh toán phần còn lại liên kết CHUẨN XÁC với invoice_id (Khử Transitive Dependency)
        if remaining_balance > 0:
            cursor.execute("""
                INSERT INTO Payments (booking_id, invoice_id, user_id, amount, payment_method, payment_status, payment_date)
                VALUES (?, ?, ?, ?, ?, 'Completed', datetime('now'))
            """, (booking_id, invoice_id, booking['customer_id'], remaining_balance, payment_method))

        # 3. Cập nhật trạng thái Booking_Master thành Checked-Out
        cursor.execute("""
            UPDATE Booking_Master
            SET booking_status = 'Checked-Out'
            WHERE booking_id = ?
        """, (booking_id,))

        # 4. Đổi trạng thái phòng vật lý thành 'Dirty'
        if booking['physical_room_id']:
            cursor.execute("""
                UPDATE Physical_Room
                SET housekeeping_status = 'Dirty'
                WHERE physical_room_id = ?
            """, (booking['physical_room_id'],))

        # 5. Tích điểm thành viên nếu khách có tài khoản
        if booking['customer_id']:
            earned_points = (booking['nights'] or 1) * 10
            cursor.execute("""
                SELECT loyalty_points FROM Customer_Profiles WHERE account_id = ?
            """, (booking['customer_id'],))
            profile = cursor.fetchone()
            if profile:
                new_points = (profile['loyalty_points'] or 0) + earned_points
                new_tier = calculate_loyalty_tier(new_points)
                cursor.execute("""
                    UPDATE Customer_Profiles
                    SET loyalty_points = ?, tier = ?
                    WHERE account_id = ?
                """, (new_points, new_tier, booking['customer_id']))

        conn.commit()

        result = {
            'booking_id': booking_id,
            'invoice_number': invoice_number,
            'total_amount': total_final,
            'deposit_paid': booking['deposit_paid'],
            'extra_services_total': extra_services_total,
            'remaining_paid': remaining_balance,
            'housekeeping_status': 'Dirty',
            'status': 'Checked-Out'
        }
        return True, result, "Quyết toán trả phòng thành công."
    except (BookingNotFoundError, InvalidBookingStateError):
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        if raise_on_error:
            raise
        return False, {}, f"Lỗi trong quá trình quyết toán check-out: {str(e)}"
    finally:
        conn.close()
