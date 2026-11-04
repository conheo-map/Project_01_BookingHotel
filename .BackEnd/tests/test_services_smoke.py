"""
Smoke Test for Service Layer - Saigon - Condao Booking Platform.
Kiểm thử độc lập các Service:
- Test 1: Khóa phòng 10 phút và thử khóa lần 2 (bắt lỗi RoomAlreadyLockedError).
- Test 2: Đặt phòng Online thành công -> Kiểm tra dữ liệu được ghi đúng vào 5 bảng mới.
- Test 3: Đặt phòng Walk-in tại quầy với customer_id = NULL thành công (không tạo tài khoản rác).
- Test 4: Check-out thành công -> Hóa đơn được tạo và phòng chuyển sang 'Dirty'.
"""

import sys
import os
import unittest
from datetime import datetime, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Đảm bảo đường dẫn import tới .BackEnd
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from database import get_db_connection
from services.exceptions import (
    RoomAlreadyLockedError,
    RoomNotAvailableError,
    PromotionInvalidError,
    BookingNotFoundError,
    InvalidBookingStateError
)
from services.room_lock_service import (
    lock_room_for_nights,
    release_lock,
    is_room_available_for_nights,
    cleanup_expired_locks
)
from services.pricing_service import (
    calculate_nightly_rates,
    evaluate_occupancy_policy,
    calculate_total_quote
)
from services.promotion_service import (
    validate_and_apply_promo,
    apply_promo_atomic
)
from services.booking_service import (
    create_online_booking,
    create_walkin_booking,
    cancel_booking,
    add_extra_service
)
from services.checkout_service import (
    get_checkout_statement,
    process_checkout
)


class TestServicesSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Thiết lập môi trường kiểm thử: tìm phòng và khách hàng mẫu."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. Tìm 1 phòng mẫu
            cursor.execute("""
                SELECT physical_room_id, room_type_id, room_name
                FROM Physical_Room
                WHERE is_active = 1
                LIMIT 1
            """)
            cls.test_room = cursor.fetchone()
            assert cls.test_room is not None, "Cần ít nhất 1 phòng vật lý trong CSDL"

            # 2. Tìm 1 khách hàng mẫu
            cursor.execute("""
                SELECT account_id, email FROM Accounts
                WHERE account_type = 'customer' AND is_active = 1
                LIMIT 1
            """)
            cls.test_customer = cursor.fetchone()
            assert cls.test_customer is not None, "Cần ít nhất 1 khách hàng trong CSDL"

            cls.created_booking_ids = []
        finally:
            conn.close()

    @classmethod
    def tearDownClass(cls):
        """Dọn dẹp các đơn đặt phòng thử nghiệm sau khi hoàn tất kiểm thử."""
        if not cls.created_booking_ids:
            return
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            for b_id in cls.created_booking_ids:
                cursor.execute("DELETE FROM Invoices WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Booking_Attributions WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Cancellation_Records WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Payments WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Extra_Services WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Booking_Nights WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Booking_Master WHERE booking_id = ?", (b_id,))
            conn.commit()
        finally:
            conn.close()

    def test_01_room_lock_and_conflict(self):
        """Test 1: Khóa phòng 10 phút và thử khóa lần 2 (bắt lỗi RoomAlreadyLockedError)."""
        room_id = self.test_room['physical_room_id']
        test_nights = ['2029-01-10', '2029-01-11']
        session_a = 'smoke_session_user_A'
        session_b = 'smoke_session_user_B'

        # Giải phóng lock cũ nếu có
        release_lock(session_a, room_id)
        release_lock(session_b, room_id)

        # Lần 1: User A khóa phòng 10 phút -> Thành công
        lock_res = lock_room_for_nights(
            physical_room_id=room_id,
            nights_list=test_nights,
            session_id=session_a,
            ttl_minutes=10,
            raise_on_error=True
        )
        self.assertTrue(lock_res['success'])
        self.assertEqual(lock_res['session_id'], session_a)

        # Lần 2: User B cố gắng khóa cùng phòng và ngày đó -> Phải ném RoomAlreadyLockedError
        with self.assertRaises(RoomAlreadyLockedError) as ctx:
            lock_room_for_nights(
                physical_room_id=room_id,
                nights_list=test_nights,
                session_id=session_b,
                ttl_minutes=10,
                raise_on_error=True
            )
        self.assertIn("giữ chỗ tạm thời", str(ctx.exception).lower())

        # Dọn dẹp lock của User A
        released = release_lock(session_a, room_id)
        self.assertGreater(released, 0)
        print("\n[PASS] Test 1: Khóa phòng 10 phút & bắt lỗi RoomAlreadyLockedError chuẩn xác.")

    def test_02_create_online_booking_integrity(self):
        """Test 2: Đặt phòng Online thành công -> Kiểm tra dữ liệu được ghi đúng vào 5 bảng mới."""
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']
        customer_id = self.test_customer['account_id']
        session_id = 'smoke_online_booking_session'
        nights = ['2029-02-15', '2029-02-16']

        # 1. Khách khóa giữ chỗ
        release_lock(session_id, room_id)
        lock_res = lock_room_for_nights(room_id, nights, session_id, ttl_minutes=10)
        self.assertTrue(lock_res['success'])

        # 2. Thực hiện đặt phòng Online
        booking_payload = {
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'booking_type': 'continuous',
            'checkin_date': '2029-02-15',
            'checkout_date': '2029-02-17',
            'adults': 2,
            'children': 0,
            'session_id': session_id,
            'payment_type': 'deposit',
            'payment_method': 'credit_card',
            'source_channel': 'google_ads',
            'utm_campaign': 'summer_campaign',
            'utm_medium': 'cpc'
        }

        success, result, msg = create_online_booking(booking_payload, customer_id, raise_on_error=True)
        self.assertTrue(success, f"Đặt phòng online thất bại: {msg}")
        booking_id = result['booking_id']
        self.created_booking_ids.append(booking_id)

        # 3. Kiểm chứng dữ liệu trên 5 bảng chuẩn 3NF
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            # Bảng 1: Booking_Master
            cursor.execute("SELECT * FROM Booking_Master WHERE booking_id = ?", (booking_id,))
            bm = cursor.fetchone()
            self.assertIsNotNone(bm)
            self.assertEqual(bm['customer_id'], customer_id)
            self.assertEqual(bm['booking_status'], 'Confirmed')
            self.assertEqual(bm['nights'], 2)
            self.assertIsInstance(bm['total_amount'], int)
            self.assertIsInstance(bm['deposit_paid'], int)

            # Bảng 2: Booking_Nights
            cursor.execute("SELECT * FROM Booking_Nights WHERE booking_id = ? ORDER BY night_date", (booking_id,))
            b_nights = cursor.fetchall()
            self.assertEqual(len(b_nights), 2)
            self.assertEqual(b_nights[0]['night_date'], '2029-02-15')
            self.assertEqual(b_nights[1]['night_date'], '2029-02-16')

            # Bảng 3: Invoices
            cursor.execute("SELECT * FROM Invoices WHERE booking_id = ?", (booking_id,))
            inv = cursor.fetchone()
            self.assertIsNotNone(inv)
            self.assertTrue(inv['invoice_number'].startswith('INV-'))
            self.assertEqual(inv['total_amount'], bm['total_amount'])

            # Bảng 4: Booking_Attributions
            cursor.execute("SELECT * FROM Booking_Attributions WHERE booking_id = ?", (booking_id,))
            attr = cursor.fetchone()
            self.assertIsNotNone(attr)
            self.assertEqual(attr['source_channel'], 'google_ads')
            self.assertEqual(attr['utm_campaign'], 'summer_campaign')

            # Bảng 5: Payments
            cursor.execute("SELECT * FROM Payments WHERE booking_id = ?", (booking_id,))
            pay = cursor.fetchone()
            self.assertIsNotNone(pay)
            self.assertEqual(pay['user_id'], customer_id)
            self.assertEqual(pay['amount'], bm['deposit_paid'])
            self.assertEqual(pay['payment_status'], 'Completed')

            # Kiểm tra Room_Lock đã được dọn sạch
            cursor.execute("SELECT 1 FROM Room_Lock WHERE session_id = ?", (session_id,))
            self.assertIsNone(cursor.fetchone(), "Room_Lock phải được xóa sau khi đặt phòng thành công.")

        finally:
            conn.close()

        print("[PASS] Test 2: Đặt phòng Online thành công, đồng bộ dữ liệu toàn vẹn trên cả 5 bảng 3NF.")

    def test_03_create_walkin_booking_without_fake_account(self):
        """Test 3: Đặt phòng Walk-in tại quầy với customer_id = NULL (chấm dứt tạo tài khoản ảo {phone}@walkin.local)."""
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']
        test_phone = '0988112233'
        fake_email = f"{test_phone}@walkin.local"

        walkin_payload = {
            'customer_name': 'Nguyen Walkin VIP',
            'customer_phone': test_phone,
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'checkin_date': '2029-03-20',
            'checkout_date': '2029-03-22',
            'adults': 1,
            'children': 0,
            'deposit_paid': 1500000,
            'payment_method': 'cash'
        }

        success, result, msg = create_walkin_booking(walkin_payload, staff_account_id=1, raise_on_error=True)
        self.assertTrue(success, f"Tạo đơn Walk-in thất bại: {msg}")
        booking_id = result['booking_id']
        self.created_booking_ids.append(booking_id)

        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            # 1. Kiểm tra Booking_Master có customer_id IS NULL và lưu thông tin trực tiếp
            cursor.execute("SELECT * FROM Booking_Master WHERE booking_id = ?", (booking_id,))
            bm = cursor.fetchone()
            self.assertIsNotNone(bm)
            self.assertIsNone(bm['customer_id'], "customer_id của đơn Walk-in phải là NULL")
            self.assertEqual(bm['guest_name'], 'Nguyen Walkin VIP')
            self.assertEqual(bm['guest_phone'], test_phone)

            # 2. Tuyệt đối KHÔNG sinh tài khoản ảo trong bảng Accounts
            cursor.execute("SELECT 1 FROM Accounts WHERE email = ?", (fake_email,))
            self.assertIsNone(cursor.fetchone(), f"Không được phép sinh tài khoản rác {fake_email} vào bảng Accounts!")

            # 3. Kiểm tra Payments cho đơn Walk-in có user_id IS NULL
            cursor.execute("SELECT * FROM Payments WHERE booking_id = ?", (booking_id,))
            pay = cursor.fetchone()
            self.assertIsNotNone(pay)
            self.assertIsNone(pay['user_id'], "user_id trong Payments của khách walk-in phải là NULL")
            self.assertEqual(pay['amount'], 1500000)

        finally:
            conn.close()

        print("[PASS] Test 3: Đặt phòng Walk-in tại quầy thành công với customer_id = NULL, không sinh tài khoản rác.")

    def test_04_checkout_and_dirty_room_transition(self):
        """Test 4: Check-out thành công -> Hóa đơn được tạo và phòng chuyển sang 'Dirty'."""
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']

        # 1. Tạo 1 đơn đặt phòng mẫu để test checkout
        walkin_payload = {
            'customer_name': 'Khach Checkout Test',
            'customer_phone': '0909998877',
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'checkin_date': '2029-04-10',
            'checkout_date': '2029-04-11',
            'adults': 1,
            'deposit_paid': 500000,
            'payment_method': 'cash'
        }
        success, res, _ = create_walkin_booking(walkin_payload, staff_account_id=1, raise_on_error=True)
        self.assertTrue(success)
        booking_id = res['booking_id']
        self.created_booking_ids.append(booking_id)

        # Đổi phòng sang Clean hoặc Occupied trước khi checkout
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Physical_Room SET housekeeping_status = 'Occupied' WHERE physical_room_id = ?", (room_id,))
            conn.commit()
        finally:
            conn.close()

        # 2. Thêm dịch vụ minibar phát sinh
        ok_srv, srv_res, _ = add_extra_service(booking_id, 'Nước suối Dasani', 2, 25000, added_by=1)
        self.assertTrue(ok_srv)
        self.assertEqual(srv_res['total_price'], 50000)

        # 3. Lấy bảng kê quyết toán (Statement)
        statement = get_checkout_statement(booking_id, raise_on_error=True)
        self.assertEqual(statement['booking_id'], booking_id)
        self.assertEqual(statement['extra_services_total'], 50000)

        # 4. Thực hiện quyết toán trả phòng
        ok_co, co_res, msg_co = process_checkout(booking_id, staff_user_id=1, payment_method='cash', raise_on_error=True)
        self.assertTrue(ok_co, f"Check-out thất bại: {msg_co}")
        self.assertEqual(co_res['housekeeping_status'], 'Dirty')

        # 5. Kiểm tra CSDL sau check-out
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            # Trạng thái booking chuyển sang Checked-Out
            cursor.execute("SELECT booking_status FROM Booking_Master WHERE booking_id = ?", (booking_id,))
            status = cursor.fetchone()['booking_status']
            self.assertEqual(status, 'Checked-Out')

            # Trạng thái phòng vật lý tự động chuyển sang 'Dirty'
            cursor.execute("SELECT housekeeping_status FROM Physical_Room WHERE physical_room_id = ?", (room_id,))
            hk_status = cursor.fetchone()['housekeeping_status']
            self.assertEqual(hk_status, 'Dirty', "Phòng vật lý phải tự động đổi trạng thái sang Dirty cho buồng phòng.")

            # Hóa đơn Invoices được cập nhật
            cursor.execute("SELECT * FROM Invoices WHERE booking_id = ?", (booking_id,))
            inv = cursor.fetchone()
            self.assertIsNotNone(inv)
            self.assertEqual(inv['total_amount'], statement['total_payable'])

        finally:
            conn.close()

        print("[PASS] Test 4: Check-out quyết toán thành công, xuất hóa đơn và phòng tự động chuyển sang 'Dirty'.")

    def test_05_pricing_service_quotes(self):
        """Test 5: Tính báo giá phòng và phụ thu qua pricing_service."""
        room_type_id = self.test_room['room_type_id']
        nights = ['2029-05-01', '2029-05-02']

        # 1. Tính báo giá tiêu chuẩn
        quote = calculate_total_quote(room_type_id, None, nights, adults=2, children=1)
        self.assertTrue(quote['allowed'])
        self.assertEqual(quote['number_of_nights'], 2)
        self.assertGreater(quote['total_amount'], 0)
        self.assertEqual(len(quote['nights_breakdown']), 2)

        # 2. Kiểm tra chính sách quá sức chứa
        over_occ = evaluate_occupancy_policy(room_type_id, adults=10, children=5)
        self.assertFalse(over_occ['allowed'])
        self.assertIn("vượt quá", over_occ['reason'].lower())
        print("[PASS] Test 5: Tính báo giá và kiểm tra chính sách sức chứa phòng thành công.")

    def test_06_promotion_atomic_and_errors(self):
        """Test 6: Kiểm tra voucher khuyến mãi nguyên tử và xử lý PromotionInvalidError."""
        # 1. Thử áp dụng mã voucher không tồn tại -> bắt lỗi PromotionInvalidError
        with self.assertRaises(PromotionInvalidError):
            apply_promo_atomic("MA_KHONG_TON_TAI_999", customer_tier="Newbie", current_total_amount=2000000)

        # 2. Tạo 1 voucher thử nghiệm để test atomic update
        conn = get_db_connection()
        test_promo_code = "TESTSMOKE20"
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Promotions WHERE code = ?", (test_promo_code,))
            cursor.execute("""
                INSERT INTO Promotions (code, discount_percent, discount_type, active, max_uses, current_uses, membership_tier_required)
                VALUES (?, 20.0, 'percent', 1, 5, 0, 'Newbie')
            """, (test_promo_code,))
            conn.commit()

            # Áp voucher nguyên tử
            disc, final_amt = apply_promo_atomic(test_promo_code, customer_tier="Newbie", current_total_amount=1000000)
            self.assertEqual(disc, 200000)
            self.assertEqual(final_amt, 800000)

            # Kiểm tra current_uses đã được cộng 1 nguyên tử
            cursor.execute("SELECT current_uses FROM Promotions WHERE code = ?", (test_promo_code,))
            uses = cursor.fetchone()['current_uses']
            self.assertEqual(uses, 1)

            # Dọn dẹp voucher test
            cursor.execute("DELETE FROM Promotions WHERE code = ?", (test_promo_code,))
            conn.commit()
        finally:
            conn.close()

        print("[PASS] Test 6: Áp voucher nguyên tử (Atomic Update) và bắt lỗi PromotionInvalidError thành công.")

    def test_07_cancellation_and_state_errors(self):
        """Test 7: Hủy phòng theo chính sách Refund_Policy và bắt BookingNotFoundError / InvalidBookingStateError."""
        # 1. Hủy booking không tồn tại -> ném BookingNotFoundError
        with self.assertRaises(BookingNotFoundError):
            cancel_booking(99999999, reason="Test error", raise_on_error=True)

        # 2. Tạo 1 booking và thực hiện hủy hợp lệ
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']
        walkin_payload = {
            'customer_name': 'Khach Test Cancel',
            'customer_phone': '0912345678',
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'checkin_date': '2029-06-10',
            'checkout_date': '2029-06-12',
            'adults': 1,
            'deposit_paid': 1000000,
            'payment_method': 'cash'
        }
        ok, res, _ = create_walkin_booking(walkin_payload, staff_account_id=1, raise_on_error=True)
        self.assertTrue(ok)
        booking_id = res['booking_id']
        self.created_booking_ids.append(booking_id)

        # Hủy phòng
        ok_cancel, cancel_res, _ = cancel_booking(booking_id, reason="Khách bận việc đột xuất", raise_on_error=True)
        self.assertTrue(ok_cancel)
        self.assertEqual(cancel_res['status'], 'Canceled')

        # 3. Thử hủy lại đơn đã bị hủy -> ném InvalidBookingStateError
        with self.assertRaises(InvalidBookingStateError):
            cancel_booking(booking_id, reason="Huy lan 2", raise_on_error=True)

        print("[PASS] Test 7: Hủy phòng tính hoàn tiền và bắt lỗi BookingNotFoundError, InvalidBookingStateError chuẩn xác.")


if __name__ == '__main__':
    unittest.main()
