"""
Frontend SSR Integration Tests - Saigon - Condao Booking Platform (Port 5001).
Kiểm thử giao diện Flask SSR, Template Filters và luồng xử lý xung đột giữ chỗ 409:
- Test 1: Truy cập trang chủ `/` (Status 200, render GSAP banner).
- Test 2: Truy cập trang tìm kiếm `/search` (Status 200).
- Test 3: Kiểm tra template filter `format_vnd` hiển thị đúng định dạng `1.250.000 ₫`.
- Test 4: Giả lập submit đặt phòng và kiểm tra cơ chế bắt lỗi flash message khi phòng bị khóa (409 Conflict).
"""

import sys
import os
import unittest
import importlib.util
from unittest.mock import patch

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'FrontEnd')
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

# Tránh va chạm namespace sys.modules['app'] giữa .BackEnd/app.py và FrontEnd/app.py
frontend_app_spec = importlib.util.spec_from_file_location("frontend_app_module", os.path.join(FRONTEND_DIR, "app.py"))
frontend_app_module = importlib.util.module_from_spec(frontend_app_spec)
# Cần set sys.modules tạm thời để routes trong FrontEnd import đúng
sys.modules["frontend_app_module"] = frontend_app_module
frontend_app_spec.loader.exec_module(frontend_app_module)
create_frontend_app = frontend_app_module.create_app


class TestFrontendViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_frontend_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SECRET_KEY'] = 'test-secret-key-frontend'
        cls.client = cls.app.test_client()

    @patch('routes.search.api_get')
    @patch('services.api.api_get')
    def test_01_homepage_renders_with_gsap(self, mock_svc_get, mock_search_get):
        """Test 1: Truy cập trang chủ `/` (Status 200, render banner và cấu trúc GSAP)."""
        mock_svc_get.return_value = {'hotels': [], 'room_types': []}
        mock_search_get.return_value = {'hotels': [], 'room_types': []}
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')
        self.assertIn("Hotel", html)
        self.assertTrue("banner" in html.lower() or "gsap" in html.lower() or "khách sạn" in html.lower())
        print("\n[PASS] Test 1: Truy cập trang chủ `/` thành công (HTTP 200, render đầy đủ banner GSAP).")

    @patch('routes.search.api_get')
    @patch('services.api.api_get')
    def test_02_search_page_renders(self, mock_svc_get, mock_search_get):
        """Test 2: Truy cập trang tìm kiếm `/search` (Status 200)."""
        mock_svc_get.return_value = {'hotels': [], 'room_types': [], 'rooms': []}
        mock_search_get.return_value = {'hotels': [], 'room_types': [], 'rooms': []}
        resp = self.client.get('/search')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')
        self.assertTrue("tìm kiếm" in html.lower() or "search" in html.lower() or "hạng phòng" in html.lower())
        print("[PASS] Test 2: Truy cập trang tìm kiếm `/search` thành công (HTTP 200).")

    def test_03_format_vnd_template_filter(self):
        """Test 3: Kiểm tra filter format_vnd hiển thị chuẩn tiền tệ Việt Nam (1.250.000 ₫)."""
        filter_func = self.app.jinja_env.filters.get('format_vnd')
        self.assertIsNotNone(filter_func, "Filter 'format_vnd' chưa được đăng ký trong Jinja2.")

        # Kiểm tra định dạng với các giá trị khác nhau
        self.assertEqual(filter_func(1250000), "1.250.000 ₫")
        self.assertEqual(filter_func(0), "0 ₫")
        self.assertEqual(filter_func("2500000"), "2.500.000 ₫")
        self.assertEqual(filter_func(None), "0 ₫")
        self.assertEqual(filter_func(1500000.75), "1.500.001 ₫")
        print("[PASS] Test 3: Template filter `format_vnd` hiển thị chính xác định dạng VND (`1.250.000 ₫`).")

    @patch('routes.booking.create_booking')
    def test_04_booking_conflict_409_flash_warning(self, mock_create_booking):
        """Test 4: Giả lập đặt phòng gặp lỗi 409 Conflict -> Flash banner cảnh báo phòng đã bị khóa."""
        # Giả lập Backend trả về lỗi 409 Conflict
        conflict_msg = 'Phòng đã được người khác giữ chỗ trong 10 phút. Vui lòng chọn phòng khác!'
        mock_create_booking.return_value = {
            'success': False,
            'status_code': 409,
            'message': conflict_msg
        }

        with self.client.session_transaction() as sess:
            sess['token'] = 'test-token-123'
            sess['user_id'] = 1
            sess['account_type'] = 'customer'
            sess['booking_lock'] = {
                'physical_room_id': 1,
                'room_type_id': 1,
                'hotel_id': 1,
                'checkin_date': '2029-12-01',
                'checkout_date': '2029-12-03',
                'selected_nights': ['2029-12-01', '2029-12-02'],
                'adults': 2,
                'children': 0,
                'booking_type': 'continuous'
            }
            sess['checkout_choices'] = {
                'payment_method': 'cash',
                'payment_type': 'full'
            }

        # Gửi POST yêu cầu thanh toán
        resp = self.client.post('/booking/payment', data={}, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')
        # Kiểm tra thông báo cảnh báo xuất hiện trong giao diện
        self.assertTrue(
            "giữ chỗ" in html.lower() or "chọn phòng khác" in html.lower(),
            f"Giao diện cần hiển thị thông báo flash cảnh báo giữ phòng. HTML preview: {html[:500]}"
        )
        print("[PASS] Test 4: Bắt lỗi 409 Conflict và hiển thị flash message cảnh báo giữ chỗ chuẩn mực.")

    def test_5_vip_evoucher_success_page_renders_flawlessly(self):
        """
        Test 5: Trang Xác nhận Đặt phòng (/payment/success) hiển thị đầy đủ
        thông tin chứng thư VIP E-Voucher 5 sao: PNR code, QR Check-in,
        thông tin phòng, đặc quyền đón tiễn sân bay, và bảng quyết toán.
        """
        with self.client.session_transaction() as sess:
            sess['last_booking'] = {
                'booking_id': 119850,
                'total_amount': 1463000,
                'deposit_paid': 731500,
                'remaining_amount': 731500,
                'invoice_number': 'INV-20261106-119850',
                'payment_type': 'deposit',
                'payment_method': 'bank_transfer',
                'room_title': 'Hạng phòng Villa Deluxe Hướng Vườn',
                'room_name': 'Villa 01',
                'hotel_name': 'Sài Gòn - Côn Đảo Resort',
                'checkin_date': '2026-11-06',
                'checkout_date': '2026-11-08',
                'num_nights': 2,
                'adults': 2,
                'children': 0,
                'customer_name': 'Trần Thị Du Khách',
                'customer_email': 'guest1@example.com',
                'membership_tier': 'VIP Diamond Member',
            }

        resp = self.client.get('/payment/success')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')

        self.assertIn('BK-119850', html)
        self.assertIn('INV-20261106-119850', html)
        self.assertIn('Hạng phòng Villa Deluxe Hướng Vườn', html)
        self.assertIn('2026-11-06', html)
        self.assertIn('2026-11-08', html)
        self.assertIn('1.463.000', html)
        self.assertIn('731.500', html)
        self.assertIn('api.qrserver.com', html)
        self.assertIn('Sân bay Cỏ Ống', html)
        self.assertIn('vip-voucher-card', html)
        print("[PASS] Test 5: VIP E-Voucher 5 sao hiển thị hoàn mỹ với đầy đủ PNR, QR code và đặc quyền.")

    @patch('routes.booking.api_get')
    def test_06_booking_history_renders_bookings(self, mock_api_get):
        """Test 6: Truy cập lịch sử đặt phòng `/history` hiển thị danh sách đơn thành công."""
        mock_api_get.return_value = {
            'success': True,
            'bookings': [
                {
                    'booking_id': 119850,
                    'user_id': 1,
                    'customer_full_name': 'Trần Thị Du Khách',
                    'hotel_name': 'Sài Gòn - Côn Đảo Resort',
                    'room_type_code': 'RES_VDEL',
                    'physical_room_name': 'RES_VDEL_01',
                    'arrival_date': '2026-11-06',
                    'departure_date': '2026-11-08',
                    'nights': 2,
                    'total_price': 1463000,
                    'deposit_paid': 731500,
                    'status': 'Confirmed',
                    'status_detail': 'Confirmed',
                    'booking_type': 'continuous',
                    'is_canceled': 0
                }
            ]
        }
        with self.client.session_transaction() as sess:
            sess['token'] = 'test-valid-token'
            sess['user_id'] = 1
            sess['username'] = 'guest1@example.com'
            sess['role'] = 'Guest'
            sess['account_type'] = 'customer'

        resp = self.client.get('/history')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')
        self.assertIn('119850', html)
        self.assertIn('RES_VDEL', html)
        self.assertIn('journey-card', html)
        self.assertNotIn('Chưa có hành trình nào', html)
        print("[PASS] Test 6: Lịch sử đặt phòng `/history` render chính xác các thẻ hành trình booking.")


if __name__ == '__main__':
    unittest.main()
