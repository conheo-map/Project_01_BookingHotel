"""
End-to-End (E2E) Full Lifecycle Test Suite
Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo

Bao quát trọn vẹn 4 luồng nghiệp vụ thực tế từ Database -> Service Layer -> REST API Controllers:
- Luồng 1: B2C Booking & Room Lock (Khóa 10 phút, chống trùng 409 Conflict, thanh toán sinh Booking + Invoice, giải phóng Lock).
- Luồng 2: Walk-in tại quầy cho khách vãng lai (customer_id = NULL, Booking_Attributions.source_channel = 'walkin', không sinh tài khoản rác trong Accounts).
- Luồng 3: Trọn vẹn vòng đời lưu trú (Check-in -> Thêm minibar Extra_Services -> Check-out quyết toán -> Phòng chuyển Dirty -> Housekeeper dọn dẹp chuyển Clean).
- Luồng 4: Giá linh hoạt & Promo nguyên tử (Manager đổi giá ngày lễ 2.500.000đ -> Khách tìm thấy đúng giá -> Áp voucher 10% trừ đúng 250.000đ -> current_uses tăng nguyên tử).
"""

import sys
import os
import unittest
import json
from datetime import datetime, date, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, '.BackEnd')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import create_app
from database import get_db_connection
from services.auth_tokens import create_api_token
from services.room_lock_service import release_lock


class TestE2EFullLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Khởi tạo môi trường kiểm thử E2E và dữ liệu chuẩn."""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            # 1. Lấy thông tin phòng mẫu hợp lệ và đang kích hoạt
            cursor.execute("""
                SELECT pr.physical_room_id, pr.room_name, pr.room_type_id, drt.room_type_code, drt.hotel_id, drt.base_price
                FROM Physical_Room pr
                JOIN Dim_RoomType drt ON pr.room_type_id = drt.room_type_id
                WHERE pr.is_active = 1 AND drt.is_active = 1 AND drt.room_type_code != ''
                LIMIT 1
            """)
            cls.test_room = cursor.fetchone()
            assert cls.test_room is not None, "Không tìm thấy phòng vật lý đang kích hoạt trong CSDL"

            # Đảm bảo phòng ban đầu ở trạng thái Clean
            cursor.execute("UPDATE Physical_Room SET housekeeping_status = 'Clean' WHERE physical_room_id = ?",
                           (cls.test_room['physical_room_id'],))
            conn.commit()

            # 2. Lấy 2 khách hàng mẫu
            cursor.execute("SELECT account_id, email FROM Accounts WHERE account_type = 'customer' ORDER BY account_id LIMIT 2")
            customers = cursor.fetchall()
            cls.customer1 = customers[0]
            cls.customer2 = customers[1]

            # 3. Lấy nhân viên các bộ phận: Receptionist, Housekeeper, Manager
            cursor.execute("""
                SELECT sp.account_id, sp.full_name, r.role_name
                FROM Staff_Profiles sp
                JOIN Roles r ON sp.role_id = r.role_id
                WHERE r.role_name = 'Receptionist'
                LIMIT 1
            """)
            cls.receptionist = cursor.fetchone()

            cursor.execute("""
                SELECT sp.account_id, sp.full_name, r.role_name
                FROM Staff_Profiles sp
                JOIN Roles r ON sp.role_id = r.role_id
                WHERE r.role_name = 'Housekeeper'
                LIMIT 1
            """)
            cls.housekeeper = cursor.fetchone()

            cursor.execute("""
                SELECT sp.account_id, sp.full_name, r.role_name
                FROM Staff_Profiles sp
                JOIN Roles r ON sp.role_id = r.role_id
                WHERE r.role_name = 'Manager'
                LIMIT 1
            """)
            cls.manager = cursor.fetchone()

            # 4. Tạo Auth Tokens
            cls.token_cust1 = create_api_token(cls.customer1['account_id'], 'customer')
            cls.token_cust2 = create_api_token(cls.customer2['account_id'], 'customer')
            cls.token_receptionist = create_api_token(cls.receptionist['account_id'], 'staff')
            cls.token_housekeeper = create_api_token(cls.housekeeper['account_id'], 'staff')
            cls.token_manager = create_api_token(cls.manager['account_id'], 'staff')

            cls.headers_cust1 = {'Authorization': f'Bearer {cls.token_cust1}', 'Content-Type': 'application/json'}
            cls.headers_cust2 = {'Authorization': f'Bearer {cls.token_cust2}', 'Content-Type': 'application/json'}
            cls.headers_receptionist = {'Authorization': f'Bearer {cls.token_receptionist}', 'Content-Type': 'application/json'}
            cls.headers_housekeeper = {'Authorization': f'Bearer {cls.token_housekeeper}', 'Content-Type': 'application/json'}
            cls.headers_manager = {'Authorization': f'Bearer {cls.token_manager}', 'Content-Type': 'application/json'}

            # 5. Khởi tạo voucher 10% chuẩn cho kiểm thử Luồng 4
            cursor.execute("""
                INSERT OR REPLACE INTO Promotions (
                    promotion_id, code, discount_percent, discount_type, max_uses, current_uses,
                    membership_tier_required, start_date, end_date, active, apply_scope
                ) VALUES (999, 'E2E_PROMO10', 10.0, 'percent', 100, 0, 'Newbie', '2026-01-01', '2026-12-31', 1, 'all')
            """)
            conn.commit()

            cls.created_booking_ids = []
            cls.created_rate_dates = []
        finally:
            conn.close()

    @classmethod
    def tearDownClass(cls):
        """Dọn dẹp triệt để dữ liệu phát sinh sau khi chạy E2E."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            for b_id in cls.created_booking_ids:
                cursor.execute("DELETE FROM Payments WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Extra_Services WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Booking_Nights WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Booking_Attributions WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Cancellation_Records WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Invoices WHERE booking_id = ?", (b_id,))
                cursor.execute("DELETE FROM Booking_Master WHERE booking_id = ?", (b_id,))

            for (rt_code, v_date) in cls.created_rate_dates:
                cursor.execute("DELETE FROM Room_Rates WHERE room_type_code = ? AND valid_date = ?", (rt_code, v_date))

            cursor.execute("DELETE FROM Promotions WHERE promotion_id = 999")
            cursor.execute("DELETE FROM Room_Lock WHERE session_id LIKE 'sess_e2e_%'")
            # Trả phòng về Clean
            cursor.execute("UPDATE Physical_Room SET housekeeping_status = 'Clean' WHERE physical_room_id = ?",
                           (cls.test_room['physical_room_id'],))
            conn.commit()
        finally:
            conn.close()

    # =========================================================================
    # LUỒNG 1: HÀNH TRÌNH ĐẶT PHÒNG B2C TRỰC TUYẾN (B2C BOOKING & LOCK)
    # =========================================================================
    def test_flow_1_b2c_booking_and_lock_lifecycle(self):
        """
        Luồng 1:
        1. Khách tìm phòng ngày 2026-11-10 đến 2026-11-12.
        2. Khách khóa giữ chỗ phòng trong 10 phút -> Bảng Room_Lock có bản ghi.
        3. Khách thứ hai cố tình vào khóa đúng phòng đó -> Hệ thống trả 409 Conflict.
        4. Khách thứ nhất thanh toán và tạo đơn -> Sinh Booking_Master và Invoices.
        5. Kiểm tra bảng Room_Lock: Khóa đã được tự động giải phóng.
        """
        pid = self.test_room['physical_room_id']
        rt_id = self.test_room['room_type_id']
        session_cust1 = "sess_e2e_cust1_flow1"
        session_cust2 = "sess_e2e_cust2_flow1"
        checkin_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        checkout_date = (date.today() + timedelta(days=4)).strftime('%Y-%m-%d')
        nights = [(date.today() + timedelta(days=2)).strftime('%Y-%m-%d'), (date.today() + timedelta(days=3)).strftime('%Y-%m-%d')]

        # 1. Tìm phòng
        search_resp = self.client.get(
            f"/api/rooms/search?checkin_date={checkin_date}&checkout_date={checkout_date}&adults=2&hotel_id={self.test_room['hotel_id']}"
        )
        self.assertEqual(search_resp.status_code, 200, "Tìm phòng phải thành công HTTP 200")
        search_data = search_resp.get_json()
        self.assertTrue(search_data.get('success'), "Kết quả tìm phòng success=True")
        rooms = search_data.get('rooms', [])
        self.assertTrue(len(rooms) > 0, "Phải tìm thấy ít nhất 1 phòng còn trống")

        # 2. Khách 1 khóa giữ phòng trong 10 phút
        lock_resp1 = self.client.post(
            f"/api/rooms/{pid}/lock",
            headers=self.headers_cust1,
            json={'session_id': session_cust1, 'nights': nights}
        )
        self.assertEqual(lock_resp1.status_code, 200, "Khách 1 khóa phòng phải thành công")
        lock_data1 = lock_resp1.get_json()
        self.assertTrue(lock_data1.get('success'))

        # Kiểm tra CSDL: Bảng Room_Lock có bản ghi
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Room_Lock WHERE physical_room_id = ? AND session_id = ?", (pid, session_cust1))
        locked_count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(locked_count, 2, "Room_Lock phải chứa 2 đêm giữ chỗ của khách 1")

        # 3. Khách 2 cố tình khóa đúng phòng đó -> Bị chặn 409 Conflict
        lock_resp2 = self.client.post(
            f"/api/rooms/{pid}/lock",
            headers=self.headers_cust2,
            json={'session_id': session_cust2, 'nights': nights}
        )
        self.assertEqual(lock_resp2.status_code, 409, "Hệ thống phải trả 409 Conflict khi phòng đang bị giữ")
        lock_data2 = lock_resp2.get_json()
        self.assertFalse(lock_data2.get('success'))
        self.assertIn("giữ chỗ", lock_data2.get('message', '').lower())

        # 4. Khách 1 thanh toán và hoàn tất đơn đặt phòng
        booking_payload = {
            "hotel_id": self.test_room['hotel_id'],
            "room_type_id": rt_id,
            "physical_room_id": pid,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "selected_nights": nights,
            "adults": 2,
            "children": 0,
            "session_id": session_cust1,
            "payment_type": "full",
            "payment_method": "credit_card"
        }
        create_resp = self.client.post(
            "/api/bookings",
            headers=self.headers_cust1,
            json=booking_payload
        )
        self.assertEqual(create_resp.status_code, 201, "Tạo đơn phòng online phải trả 201 Created")
        create_data = create_resp.get_json()
        self.assertTrue(create_data.get('success'))
        booking_id = create_data.get('booking_id')
        invoice_number = create_data.get('invoice_number')
        self.assertIsNotNone(booking_id)
        self.assertIsNotNone(invoice_number)
        self.created_booking_ids.append(booking_id)

        # Kiểm tra CSDL: Đơn được ghi vào Booking_Master và Invoices
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT booking_id, customer_id, booking_status, total_amount FROM Booking_Master WHERE booking_id = ?", (booking_id,))
        bm_row = cursor.fetchone()
        self.assertIsNotNone(bm_row)
        self.assertEqual(bm_row['booking_status'], 'Confirmed')
        self.assertEqual(bm_row['customer_id'], self.customer1['account_id'])

        cursor.execute("SELECT invoice_number, total_amount FROM Invoices WHERE booking_id = ?", (booking_id,))
        inv_row = cursor.fetchone()
        self.assertIsNotNone(inv_row)
        self.assertEqual(inv_row['invoice_number'], invoice_number)

        # 5. Kiểm tra bảng Room_Lock: Khóa giữ chỗ tự động giải phóng
        cursor.execute("SELECT COUNT(*) FROM Room_Lock WHERE session_id = ?", (session_cust1,))
        remaining_locks = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(remaining_locks, 0, "Room_Lock phải được giải phóng 100% sau khi tạo đơn thành công")

    # =========================================================================
    # LUỒNG 2: HÀNH TRÌNH ĐẶT PHÒNG TẠI QUẦY CHO KHÁCH VÃNG LAI (WALK-IN)
    # =========================================================================
    def test_flow_2_receptionist_walkin_no_dummy_account(self):
        """
        Luồng 2:
        1. Lễ tân thao tác tạo đơn Walk-in cho khách: "Nguyễn Văn Khách", SĐT "0901234567".
        2. Đơn được lưu thành công với customer_id = NULL.
        3. Kiểm tra bảng Accounts: Xác nhận KHÔNG có tài khoản ảo {phone}@walkin.local hay tài khoản rác.
        4. Kiểm tra bảng Booking_Attributions: source_channel = 'walkin'.
        """
        pid = self.test_room['physical_room_id']
        rt_id = self.test_room['room_type_id']
        walkin_payload = {
            "hotel_id": self.test_room['hotel_id'],
            "room_type_id": rt_id,
            "physical_room_id": pid,
            "checkin_date": "2026-11-20",
            "checkout_date": "2026-11-22",
            "selected_nights": ["2026-11-20", "2026-11-21"],
            "guest_name": "Nguyễn Văn Khách",
            "guest_phone": "0901234567",
            "guest_email": "",
            "adults": 1,
            "children": 0,
            "deposit_amount": 0,
            "payment_method": "cash"
        }

        walkin_resp = self.client.post(
            "/api/bookings/walkin",
            headers=self.headers_receptionist,
            json=walkin_payload
        )
        self.assertEqual(walkin_resp.status_code, 201, "Tạo đơn Walk-in phải trả 201 Created")
        walkin_data = walkin_resp.get_json()
        self.assertTrue(walkin_data.get('success'))
        walkin_booking_id = walkin_data.get('booking_id')
        self.assertIsNotNone(walkin_booking_id)
        self.created_booking_ids.append(walkin_booking_id)

        # 2. Kiểm tra CSDL: customer_id = NULL, thông tin khách lưu trực tiếp tại Booking_Master
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT booking_id, customer_id, guest_name, guest_phone, booking_status
            FROM Booking_Master
            WHERE booking_id = ?
        """, (walkin_booking_id,))
        walkin_row = cursor.fetchone()
        self.assertIsNotNone(walkin_row)
        self.assertIsNone(walkin_row['customer_id'], "Walk-in booking PHẢI có customer_id là NULL")
        self.assertEqual(walkin_row['guest_name'], "Nguyễn Văn Khách")
        self.assertEqual(walkin_row['guest_phone'], "0901234567")

        # Kiểm tra nguồn Walk-in chuẩn 3NF trong Booking_Attributions
        cursor.execute("SELECT source_channel FROM Booking_Attributions WHERE booking_id = ?", (walkin_booking_id,))
        attr_row = cursor.fetchone()
        self.assertIsNotNone(attr_row)
        self.assertEqual(attr_row['source_channel'], 'walkin')

        # 3. Kiểm tra bảng Accounts: Xác nhận KHÔNG có tài khoản rác
        cursor.execute("SELECT COUNT(*) FROM Accounts WHERE email LIKE '%0901234567%' OR email LIKE '%@walkin%'")
        dummy_accounts = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(dummy_accounts, 0, "Bảng Accounts KHÔNG được chứa bất kỳ tài khoản rác walk-in nào")

    # =========================================================================
    # LUỒNG 3: TRỌN VẸN VÒNG ĐỜI LƯU TRÚ (CHECK-IN -> EXTRA -> CHECK-OUT -> CLEAN)
    # =========================================================================
    def test_flow_3_complete_stay_lifecycle_and_housekeeping(self):
        """
        Luồng 3:
        1. Lễ tân Check-in đơn phòng hôm nay -> Booking_Master.booking_status = 'Checked-in'.
        2. Khách dùng minibar: Lễ tân thêm 2 chai nước suối 20.000đ/chai vào Extra_Services.
        3. Khách làm thủ tục Check-out:
           - Lễ tân gọi API bảng kê (checkout-statement), xác nhận dịch vụ thêm 40.000đ.
           - Lễ tân xác nhận quyết toán (process_checkout), in Invoices, trạng thái đổi thành 'Checked-Out'.
        4. Tự động chuyển trạng thái phòng: Physical_Room.housekeeping_status tự động thành 'Dirty'.
        5. Nhân viên buồng phòng (Housekeeper) dọn xong, gọi API chuyển trạng thái phòng về 'Clean'.
        """
        today = date.today()
        checkin_date_str = today.strftime('%Y-%m-%d')
        checkout_date_str = (today + timedelta(days=2)).strftime('%Y-%m-%d')
        night_1 = checkin_date_str
        night_2 = (today + timedelta(days=1)).strftime('%Y-%m-%d')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pr.physical_room_id, pr.room_type_id, drt.hotel_id
            FROM Physical_Room pr
            JOIN Dim_RoomType drt ON pr.room_type_id = drt.room_type_id
            WHERE pr.is_active = 1
              AND pr.physical_room_id NOT IN (
                  SELECT physical_room_id FROM Booking_Nights
                  WHERE night_date IN (?, ?)
              )
            LIMIT 1
        """, (night_1, night_2))
        avail = cursor.fetchone()
        if avail:
            pid = avail['physical_room_id']
            rt_id = avail['room_type_id']
            hotel_id = avail['hotel_id']
        else:
            pid = self.test_room['physical_room_id']
            rt_id = self.test_room['room_type_id']
            hotel_id = self.test_room['hotel_id']

        # Đảm bảo phòng sạch trước khi check-in
        conn.execute("UPDATE Physical_Room SET housekeeping_status = 'Clean' WHERE physical_room_id = ?", (pid,))
        conn.commit()
        conn.close()

        b_payload = {
            "hotel_id": hotel_id,
            "room_type_id": rt_id,
            "physical_room_id": pid,
            "checkin_date": checkin_date_str,
            "checkout_date": checkout_date_str,
            "selected_nights": [night_1, night_2],
            "guest_name": "Trần Thị Du Khách",
            "guest_phone": "0987654321",
            "adults": 2,
            "children": 0,
            "deposit_amount": 0,
            "payment_method": "cash"
        }
        create_resp = self.client.post("/api/bookings/walkin", headers=self.headers_receptionist, json=b_payload)
        self.assertEqual(create_resp.status_code, 201)
        booking_id = create_resp.get_json()['booking_id']
        self.created_booking_ids.append(booking_id)

        # 1. Lễ tân thực hiện Check-in
        checkin_resp = self.client.put(f"/api/bookings/{booking_id}/checkin", headers=self.headers_receptionist)
        self.assertEqual(checkin_resp.status_code, 200, "Check-in phải thành công")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT booking_status FROM Booking_Master WHERE booking_id = ?", (booking_id,))
        self.assertEqual(cursor.fetchone()['booking_status'], 'Checked-in')
        conn.close()

        # 2. Thêm dịch vụ minibar: 2 chai nước suối 20.000đ
        extra_payload = {
            "service_name": "Nước suối khoáng Côn Đảo",
            "quantity": 2,
            "unit_price": 20000
        }
        extra_resp = self.client.post(
            f"/api/bookings/{booking_id}/extra-services",
            headers=self.headers_receptionist,
            json=extra_payload
        )
        self.assertEqual(extra_resp.status_code, 201, "Thêm Extra_Services phải trả 201 Created")

        # Kiểm tra CSDL Extra_Services
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT service_name, quantity, unit_price, total_price FROM Extra_Services WHERE booking_id = ?", (booking_id,))
        extra_row = cursor.fetchone()
        self.assertIsNotNone(extra_row)
        self.assertEqual(extra_row['quantity'], 2)
        self.assertEqual(extra_row['unit_price'], 20000)
        self.assertEqual(extra_row['total_price'], 40000)
        conn.close()

        # 3. Lễ tân lấy bảng kê trả phòng (checkout-statement)
        stmt_resp = self.client.get(f"/api/bookings/{booking_id}/checkout-statement", headers=self.headers_receptionist)
        self.assertEqual(stmt_resp.status_code, 200, "Lấy bảng kê trả phòng phải thành công")
        stmt_data = stmt_resp.get_json().get('statement', {})
        self.assertEqual(stmt_data.get('extra_services_total'), 40000, "Tiền dịch vụ thêm phải là 40.000đ")

        # Lễ tân thực hiện quyết toán Check-out
        checkout_resp = self.client.put(
            f"/api/bookings/{booking_id}/checkout",
            headers=self.headers_receptionist,
            json={"payment_method": "cash"}
        )
        self.assertEqual(checkout_resp.status_code, 200, "Quyết toán check-out phải thành công")
        checkout_data = checkout_resp.get_json()
        self.assertTrue(checkout_data.get('success'))

        # Kiểm tra CSDL sau quyết toán
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT booking_status FROM Booking_Master WHERE booking_id = ?", (booking_id,))
        self.assertEqual(cursor.fetchone()['booking_status'], 'Checked-Out', "Trạng thái đơn phải là Checked-Out")

        # 4. Xác nhận Physical_Room tự động chuyển sang 'Dirty'
        cursor.execute("SELECT housekeeping_status FROM Physical_Room WHERE physical_room_id = ?", (pid,))
        self.assertEqual(cursor.fetchone()['housekeeping_status'], 'Dirty', "Phòng phải tự động chuyển thành 'Dirty'")
        conn.close()

        # 5. Nhân viên buồng phòng dọn dẹp và gọi API chuyển về 'Clean'
        clean_resp = self.client.put(
            f"/api/physical-rooms/{pid}/status",
            headers=self.headers_housekeeper,
            json={"housekeeping_status": "Clean"}
        )
        self.assertEqual(clean_resp.status_code, 200, "Housekeeper cập nhật trạng thái phòng phải thành công")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT housekeeping_status FROM Physical_Room WHERE physical_room_id = ?", (pid,))
        self.assertEqual(cursor.fetchone()['housekeeping_status'], 'Clean', "Phòng đã được buồng phòng dọn dẹp chuyển về 'Clean'")
        conn.close()

    # =========================================================================
    # LUỒNG 4: GIÁ LINH HOẠT VÀ KHUYẾN MÃI NGUYÊN TỬ (DYNAMIC PRICING & PROMO)
    # =========================================================================
    def test_flow_4_dynamic_pricing_and_atomic_promotion(self):
        """
        Luồng 4:
        1. Quản lý (Manager) thiết lập giá ngày lễ 2.500.000đ cho ngày 2026-12-25 trong Room_Rates.
        2. Khách hàng tìm phòng vào ngày 2026-12-25: Xác nhận hệ thống báo đúng giá 2.500.000đ.
        3. Khách áp mã voucher 10%: Xác nhận tổng tiền trừ chính xác 250.000đ (còn 2.250.000đ trước thuế).
        4. Xác nhận current_uses của voucher trong bảng Promotions được tăng nguyên tử lên +1.
        """
        pid = self.test_room['physical_room_id']
        rt_id = self.test_room['room_type_id']
        rt_code = self.test_room['room_type_code']
        holiday_date = "2026-12-25"
        holiday_next_date = "2026-12-26"
        session_promo = "sess_e2e_flow4_promo"

        # 1. Quản lý thiết lập giá ngày lễ 2.500.000đ
        rate_payload = {
            "mode": "type",
            "target_id": rt_code,
            "start_date": holiday_date,
            "end_date": holiday_date,
            "new_price": 2500000,
            "is_holiday": 1
        }
        set_rate_resp = self.client.post(
            "/api/room-rates/comprehensive",
            headers=self.headers_manager,
            json=rate_payload
        )
        self.assertEqual(set_rate_resp.status_code, 200, "Manager cập nhật giá linh hoạt phải thành công")
        self.created_rate_dates.append((rt_code, holiday_date))

        # Kiểm tra CSDL Room_Rates
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT base_price, is_holiday FROM Room_Rates WHERE room_type_code = ? AND valid_date = ?", (rt_code, holiday_date))
        rate_row = cursor.fetchone()
        self.assertIsNotNone(rate_row)
        self.assertEqual(rate_row['base_price'], 2500000, "Giá trong Room_Rates phải là 2.500.000đ")
        self.assertEqual(rate_row['is_holiday'], 1)

        # Lấy số lượt sử dụng voucher trước khi đặt
        cursor.execute("SELECT current_uses FROM Promotions WHERE code = 'E2E_PROMO10'")
        initial_uses = cursor.fetchone()['current_uses']
        conn.close()

        # 2. Khách hàng tìm phòng vào ngày 2026-12-25
        search_resp = self.client.get(
            f"/api/rooms/search?checkin_date={holiday_date}&checkout_date={holiday_next_date}&adults=1&hotel_id={self.test_room['hotel_id']}"
        )
        self.assertEqual(search_resp.status_code, 200)
        search_rooms = search_resp.get_json().get('rooms', [])
        target_room = next((r for r in search_rooms if r.get('room_type_code') == rt_code), None)
        self.assertIsNotNone(target_room, f"Phải tìm thấy phòng hạng {rt_code}")
        self.assertEqual(
            int(round(target_room.get('effective_price_max'))),
            2500000,
            "Hệ thống phải báo đúng giá ngày lễ 2.500.000đ từ Room_Rates"
        )

        # 3. Khách khóa phòng và áp voucher E2E_PROMO10 (10%)
        lock_resp = self.client.post(
            f"/api/rooms/{pid}/lock",
            headers=self.headers_cust1,
            json={'session_id': session_promo, 'nights': [holiday_date]}
        )
        self.assertEqual(lock_resp.status_code, 200)

        booking_promo_payload = {
            "hotel_id": self.test_room['hotel_id'],
            "room_type_id": rt_id,
            "physical_room_id": pid,
            "checkin_date": holiday_date,
            "checkout_date": holiday_next_date,
            "selected_nights": [holiday_date],
            "adults": 1,
            "children": 0,
            "session_id": session_promo,
            "promo_code": "E2E_PROMO10",
            "payment_type": "full",
            "payment_method": "credit_card"
        }
        create_resp = self.client.post("/api/bookings", headers=self.headers_cust1, json=booking_promo_payload)
        self.assertEqual(create_resp.status_code, 201, "Tạo đơn có voucher 10% phải thành công trả 201")
        promo_booking_id = create_resp.get_json()['booking_id']
        self.created_booking_ids.append(promo_booking_id)

        # Kiểm tra CSDL Booking_Master: Số tiền giảm đúng 250.000đ
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT discount_amount, total_amount, tax_amount FROM Booking_Master WHERE booking_id = ?", (promo_booking_id,))
        bm_promo = cursor.fetchone()
        self.assertEqual(bm_promo['discount_amount'], 250000, "Voucher 10% của 2.500.000đ phải giảm đúng 250.000đ")
        # Tiền phòng sau giảm: 2.250.000đ. Thuế 10%: 225.000đ. Tổng: 2.475.000đ
        self.assertEqual(bm_promo['tax_amount'], 225000)
        self.assertEqual(bm_promo['total_amount'], 2475000)

        # 4. Kiểm tra current_uses tăng nguyên tử lên +1
        cursor.execute("SELECT current_uses FROM Promotions WHERE code = 'E2E_PROMO10'")
        new_uses = cursor.fetchone()['current_uses']
        conn.close()
        self.assertEqual(new_uses, initial_uses + 1, "Voucher current_uses phải được tăng nguyên tử đúng +1")


if __name__ == '__main__':
    unittest.main()
