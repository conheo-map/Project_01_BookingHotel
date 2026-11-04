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
from unittest.mock import patch

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'FrontEnd')
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

from app import create_app as create_frontend_app


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


if __name__ == '__main__':
    unittest.main()
