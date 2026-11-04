"""
Integration Test for REST API Controllers - Saigon - Condao Booking Platform.
Sử dụng Flask test_client() để kiểm thử đầu-cuối các API Thin Controllers:
- Test API 1: POST /api/rooms/lock -> Thành công trả 200; gọi lại lần 2 trả 409 Conflict.
- Test API 2: POST /api/bookings -> Tạo đơn phòng online thành công trả 201 Created.
- Test API 3: POST /api/bookings/walkin -> Tạo đơn Walk-in thành công trả 201 Created.
- Test API 4: GET /api/bookings/<id>/checkout-statement -> Trả về chi tiết bảng kê trả phòng.
- Test API 5: PUT /api/bookings/<id>/checkout -> Trả phòng thành công, hóa đơn sinh đúng định dạng INV-YYYYMMDD-ID.
"""

import sys
import os
import unittest
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import create_app
from database import get_db_connection
from services.auth_tokens import create_api_token
from services.room_lock_service import release_lock


class TestApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Khởi tạo Flask test_client và dữ liệu thử nghiệm."""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # Lấy 1 phòng mẫu
            cursor.execute("SELECT physical_room_id, room_type_id, room_name FROM Physical_Room WHERE is_active = 1 LIMIT 1")
            cls.test_room = cursor.fetchone()
            assert cls.test_room is not None

            # Lấy 1 khách hàng mẫu
            cursor.execute("SELECT account_id, email FROM Accounts WHERE account_type = 'customer' LIMIT 1")
            cls.test_customer = cursor.fetchone()

            # Lấy 1 lễ tân mẫu (Receptionist)
            cursor.execute("""
                SELECT sp.account_id, sp.full_name, r.role_name
                FROM Staff_Profiles sp
                JOIN Roles r ON sp.role_id = r.role_id
                WHERE r.role_name = 'Receptionist'
                LIMIT 1
            """)
            cls.test_staff = cursor.fetchone()
            assert cls.test_staff is not None

            cls.customer_token = create_api_token(cls.test_customer['account_id'], 'customer')
            cls.staff_token = create_api_token(cls.test_staff['account_id'], 'staff')

            cls.customer_headers = {
                'Authorization': f'Bearer {cls.customer_token}',
                'Content-Type': 'application/json'
            }
            cls.staff_headers = {
                'Authorization': f'Bearer {cls.staff_token}',
                'Content-Type': 'application/json'
            }
            cls.created_booking_ids = []
        finally:
            conn.close()

    @classmethod
    def tearDownClass(cls):
        """Dọn dẹp các đơn đặt phòng thử nghiệm sau khi test hoàn tất."""
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

    def test_01_api_lock_room_and_conflict(self):
        """Test API 1: POST /api/rooms/lock -> Thành công trả 200; gọi lại lần 2 trả 409 Conflict."""
        room_id = self.test_room['physical_room_id']
        nights = ['2029-07-01', '2029-07-02']
        session_1 = 'api_test_session_user_1'
        session_2 = 'api_test_session_user_2'

        # Dọn dẹp lock cũ
        release_lock(session_1, room_id)
        release_lock(session_2, room_id)

        # Lần 1: Khóa thành công
        payload1 = {
            'physical_room_id': room_id,
            'nights': nights,
            'session_id': session_1
        }
        resp1 = self.client.post('/api/rooms/lock', json=payload1)
        self.assertEqual(resp1.status_code, 200)
        data1 = resp1.get_json()
        self.assertTrue(data1.get('success'))

        # Lần 2: Cố gắng khóa cùng phòng/ngày từ session khác -> 409 Conflict
        payload2 = {
            'physical_room_id': room_id,
            'nights': nights,
            'session_id': session_2
        }
        resp2 = self.client.post('/api/rooms/lock', json=payload2)
        self.assertEqual(resp2.status_code, 409)
        data2 = resp2.get_json()
        self.assertFalse(data2.get('success'))
        self.assertIn("giữ chỗ trong 10 phút", data2.get('message', ''))

        # Dọn dẹp lock
        release_lock(session_1, room_id)
        print("\n[PASS] Test API 1: POST /api/rooms/lock trả 200 và chặn xung đột với 409 Conflict chuẩn mực.")

    def test_02_api_create_online_booking(self):
        """Test API 2: POST /api/bookings -> Tạo đơn phòng online thành công trả 201 Created."""
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']
        session_id = 'api_online_booking_session'
        nights = ['2029-08-10', '2029-08-11']

        # Khóa phòng trước
        release_lock(session_id, room_id)
        self.client.post('/api/rooms/lock', json={
            'physical_room_id': room_id,
            'nights': nights,
            'session_id': session_id
        })

        booking_payload = {
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'booking_type': 'continuous',
            'checkin_date': '2029-08-10',
            'checkout_date': '2029-08-12',
            'adults': 2,
            'children': 0,
            'session_id': session_id,
            'payment_type': 'deposit',
            'payment_method': 'credit_card',
            'source_channel': 'google',
            'utm_campaign': 'autumn_promo'
        }

        resp = self.client.post('/api/bookings', json=booking_payload, headers=self.customer_headers)
        self.assertEqual(resp.status_code, 201, f"Lỗi: {resp.get_json()}")
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn('booking_id', data)
        self.assertIn('invoice_number', data)

        self.created_booking_ids.append(data['booking_id'])
        print("[PASS] Test API 2: POST /api/bookings tạo đơn online thành công, trả về HTTP 201 Created.")

    def test_03_api_create_walkin_booking(self):
        """Test API 3: POST /api/bookings/walkin -> Tạo đơn Walk-in thành công trả 201 Created."""
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']
        test_phone = '0933445566'

        walkin_payload = {
            'customer_name': 'Le Thi Thu Thao (Walkin API)',
            'customer_phone': test_phone,
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'checkin_date': '2029-09-01',
            'checkout_date': '2029-09-03',
            'adults': 1,
            'children': 0,
            'deposit_paid': 1200000,
            'payment_method': 'cash'
        }

        resp = self.client.post('/api/bookings/walkin', json=walkin_payload, headers=self.staff_headers)
        self.assertEqual(resp.status_code, 201, f"Lỗi: {resp.get_json()}")
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        b_id = data['booking_id']
        self.created_booking_ids.append(b_id)

        # Kiểm chứng trong CSDL: customer_id phải là NULL
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id, guest_name, guest_phone FROM Booking_Master WHERE booking_id = ?", (b_id,))
            row = cursor.fetchone()
            self.assertIsNone(row['customer_id'], "Walk-in phải có customer_id = NULL")
            self.assertEqual(row['guest_name'], 'Le Thi Thu Thao (Walkin API)')

            # Xác nhận không tạo tài khoản ảo trong Accounts
            cursor.execute("SELECT 1 FROM Accounts WHERE email LIKE ?", (f'%{test_phone}%',))
            self.assertIsNone(cursor.fetchone(), "Không được sinh tài khoản rác trong Accounts")
        finally:
            conn.close()

        print("[PASS] Test API 3: POST /api/bookings/walkin thành công, trả 201 Created, customer_id = NULL.")

    def test_04_api_checkout_statement(self):
        """Test API 4: GET /api/bookings/<id>/checkout-statement -> Trả về chi tiết bảng kê trả phòng."""
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']

        # Tạo đơn để test checkout
        walkin_payload = {
            'customer_name': 'Khach Test Statement',
            'customer_phone': '0966554433',
            'hotel_id': 1,
            'room_type_id': room_type_id,
            'physical_room_id': room_id,
            'checkin_date': '2029-10-15',
            'checkout_date': '2029-10-17',
            'adults': 1,
            'deposit_paid': 800000,
            'payment_method': 'cash'
        }
        res_create = self.client.post('/api/bookings/walkin', json=walkin_payload, headers=self.staff_headers)
        self.assertEqual(res_create.status_code, 201)
        b_id = res_create.get_json()['booking_id']
        self.created_booking_ids.append(b_id)

        # Thêm 1 dịch vụ phát sinh
        self.client.post(f'/api/bookings/{b_id}/extra-services', json={
            'service_name': 'Bia Tiger Lon',
            'quantity': 3,
            'unit_price': 35000
        }, headers=self.staff_headers)

        # Gọi API lấy bảng kê quyết toán
        resp = self.client.get(f'/api/bookings/{b_id}/checkout-statement')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        statement = data.get('statement')
        self.assertEqual(statement['booking_id'], b_id)
        self.assertEqual(statement['extra_services_total'], 105000)
        self.assertGreater(statement['total_payable'], 0)

        # Lưu b_id để dùng tiếp cho test 5
        self.checkout_test_booking_id = b_id
        print("[PASS] Test API 4: GET /api/bookings/<id>/checkout-statement trả bảng kê tài chính chi tiết chuẩn xác.")

    def test_05_api_checkout_process(self):
        """Test API 5: PUT /api/bookings/<id>/checkout -> Trả phòng thành công, hóa đơn INV-YYYYMMDD-ID và phòng Dirty."""
        # Lấy lại booking_id từ test 4 (hoặc tạo mới nếu chạy riêng lẻ)
        b_id = getattr(self, 'checkout_test_booking_id', None)
        room_id = self.test_room['physical_room_id']
        room_type_id = self.test_room['room_type_id']

        if not b_id:
            walkin_payload = {
                'customer_name': 'Khach Test Checkout Process',
                'customer_phone': '0977889900',
                'hotel_id': 1,
                'room_type_id': room_type_id,
                'physical_room_id': room_id,
                'checkin_date': '2029-11-01',
                'checkout_date': '2029-11-02',
                'adults': 1,
                'deposit_paid': 500000,
                'payment_method': 'cash'
            }
            res_c = self.client.post('/api/bookings/walkin', json=walkin_payload, headers=self.staff_headers)
            b_id = res_c.get_json()['booking_id']
            self.created_booking_ids.append(b_id)

        # Gọi PUT checkout
        resp = self.client.put(f'/api/bookings/{b_id}/checkout', json={'payment_method': 'cash'}, headers=self.staff_headers)
        self.assertEqual(resp.status_code, 200, f"Lỗi: {resp.get_json()}")
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertTrue(data['invoice_number'].startswith('INV-'))
        self.assertEqual(data['housekeeping_status'], 'Dirty')

        # Kiểm chứng phòng vật lý trong CSDL tự động chuyển sang 'Dirty'
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT housekeeping_status FROM Physical_Room WHERE physical_room_id = ?", (room_id,))
            hk_status = cursor.fetchone()['housekeeping_status']
            self.assertEqual(hk_status, 'Dirty', "Phòng vật lý phải tự động cập nhật sang 'Dirty' cho buồng phòng.")
        finally:
            conn.close()

        print("[PASS] Test API 5: PUT /api/bookings/<id>/checkout thành công, sinh hóa đơn và chuyển phòng sang 'Dirty'.")


if __name__ == '__main__':
    unittest.main()
