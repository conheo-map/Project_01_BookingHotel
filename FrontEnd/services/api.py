"""
HTTP Client Service cho Frontend (Flask SSR - Port 5001).
Đóng vai trò cầu nối giao tiếp với Backend REST API (Port 5000):
- Chuẩn hóa tiền tệ số nguyên VND, loại bỏ hoàn toàn các trường _cents.
- Xử lý mã trạng thái HTTP chuẩn RESTful (200, 201, 400, 404, 409).
- Cung cấp các hàm Domain API tiện ích cho Đặt phòng, Quyết toán, Walk-in.
"""

import os
import requests
from flask import session

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')
_TIMEOUT = 15


def _headers(token=None):
    t = token or session.get('token', '')
    h = {'Content-Type': 'application/json'}
    if t:
        h['Authorization'] = f'Bearer {t}'
    return h


def _normalize_money_fields(obj):
    """
    Chuẩn hóa cấu trúc trường tiền tệ giữa Frontend và Backend:
    - Ánh xạ tương hỗ total_amount <-> total_price (VND nguyên)
    - Loại bỏ triệt để các trường _cents cũ
    """
    if isinstance(obj, dict):
        if 'total_amount' in obj and 'total_price' not in obj:
            obj['total_price'] = obj['total_amount']
        elif 'total_price' in obj and 'total_amount' not in obj:
            obj['total_amount'] = obj['total_price']
        for k, v in list(obj.items()):
            if k.endswith('_cents'):
                del obj[k]
            elif isinstance(v, (dict, list)):
                _normalize_money_fields(v)
    elif isinstance(obj, list):
        for item in obj:
            _normalize_money_fields(item)
    return obj


def api_get(path, params=None, token=None):
    try:
        r = requests.get(
            f'{BACKEND_URL}{path}',
            params=params,
            headers=_headers(token),
            timeout=_TIMEOUT,
        )
        try:
            data = r.json()
            data = _normalize_money_fields(data)
            data['status_code'] = r.status_code
            if not r.ok:
                data['success'] = False
            return data
        except Exception:
            return {'success': False, 'status_code': r.status_code, 'message': f'Lỗi phản hồi Backend (HTTP {r.status_code})'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def api_post(path, data=None, token=None):
    try:
        payload = _normalize_money_fields(data.copy() if isinstance(data, dict) else (data or {}))
        r = requests.post(
            f'{BACKEND_URL}{path}',
            json=payload,
            headers=_headers(token),
            timeout=_TIMEOUT,
        )
        try:
            res_data = r.json()
            res_data = _normalize_money_fields(res_data)
            res_data['status_code'] = r.status_code
            if not r.ok:
                res_data['success'] = False
                if r.status_code == 409 and not res_data.get('message'):
                    res_data['message'] = 'Phòng đã được người khác giữ chỗ trong 10 phút. Vui lòng chọn phòng khác!'
            return res_data
        except Exception:
            if r.status_code == 409:
                return {'success': False, 'status_code': 409, 'message': 'Phòng đã được người khác giữ chỗ trong 10 phút. Vui lòng chọn phòng khác!'}
            return {'success': False, 'status_code': r.status_code, 'message': f'Backend trả về lỗi (HTTP {r.status_code}): {r.text[:200]}'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def api_put(path, data=None, token=None):
    try:
        payload = _normalize_money_fields(data.copy() if isinstance(data, dict) else (data or {}))
        r = requests.put(
            f'{BACKEND_URL}{path}',
            json=payload,
            headers=_headers(token),
            timeout=_TIMEOUT,
        )
        try:
            res_data = r.json()
            res_data = _normalize_money_fields(res_data)
            res_data['status_code'] = r.status_code
            if not r.ok:
                res_data['success'] = False
            return res_data
        except Exception:
            return {'success': False, 'status_code': r.status_code, 'message': f'Backend trả về lỗi (HTTP {r.status_code}): {r.text[:200]}'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def api_delete(path, token=None):
    try:
        r = requests.delete(
            f'{BACKEND_URL}{path}',
            headers=_headers(token),
            timeout=_TIMEOUT,
        )
        try:
            data = r.json()
            return _normalize_money_fields(data)
        except Exception:
            return {'success': False, 'status_code': r.status_code, 'message': f'Backend trả về lỗi (HTTP {r.status_code})'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def api_get_qs(path_with_qs, token=None):
    """GET với query string đã được build sẵn (hỗ trợ multi-value array params)."""
    try:
        r = requests.get(
            f'{BACKEND_URL}{path_with_qs}',
            headers=_headers(token),
            timeout=_TIMEOUT,
        )
        try:
            return _normalize_money_fields(r.json())
        except Exception:
            return {'success': False, 'status_code': r.status_code, 'message': f'Backend trả về lỗi (HTTP {r.status_code})'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def api_upload(path, files, token=None):
    """Upload file qua multipart/form-data."""
    try:
        t = token or session.get('token', '')
        h = {}
        if t:
            h['Authorization'] = f'Bearer {t}'
        r = requests.post(
            f'{BACKEND_URL}{path}',
            files=files,
            headers=h,
            timeout=30,
        )
        try:
            return _normalize_money_fields(r.json())
        except Exception:
            return {'success': False, 'message': f'Backend trả về lỗi (HTTP {r.status_code}): {r.text[:200]}'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ── DOMAIN API WRAPPERS (CLEAN SERVICE BRIDGES) ──────────────────────────────

def create_booking(payload, token=None):
    """
    Tạo đơn đặt phòng Online qua Backend REST API:
    - Bắt lỗi 409 Conflict -> Thông báo phòng đang bị người khác giữ chỗ trong 10 phút.
    - Bắt lỗi 400 Bad Request -> Thông báo lỗi chi tiết từ server.
    - Đón nhận booking_id và invoice_number khi thành công (201 Created).
    """
    res = api_post('/api/bookings', payload, token=token)
    if res.get('status_code') == 409 or ('message' in res and 'giữ chỗ' in str(res['message']).lower()):
        return {
            'success': False,
            'status_code': 409,
            'message': 'Phòng đã được người khác giữ chỗ trong 10 phút. Vui lòng chọn phòng khác!'
        }
    return res


def create_walkin_booking(payload, token=None):
    """Lễ tân tạo đơn đặt phòng trực tiếp tại quầy (customer_id = NULL)."""
    return api_post('/api/bookings/walkin', payload, token=token)


def get_checkout_statement(booking_id, token=None):
    """Lấy bảng kê quyết toán trả phòng chi tiết từ Backend."""
    return api_get(f'/api/bookings/{booking_id}/checkout-statement', token=token)


def process_checkout(booking_id, payment_method='cash', token=None):
    """Thực hiện quyết toán trả phòng và chuyển phòng sang Dirty."""
    return api_put(f'/api/bookings/{booking_id}/checkout', {'payment_method': payment_method}, token=token)
