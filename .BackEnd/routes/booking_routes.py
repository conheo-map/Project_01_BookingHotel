"""
Booking Routes - Thin Controller cho nghiệp vụ Đặt phòng, Quyết toán & Buồng phòng.
Tuân thủ Clean Architecture: Không chứa SQL trực tiếp, dưới 200 dòng, bắt Exception nghiệp vụ.
"""
from flask import Blueprint, request, jsonify, g
from services.api_auth import require_token, can_access_customer_booking
from services.exceptions import (
    RoomAlreadyLockedError, RoomNotAvailableError,
    PromotionInvalidError, BookingNotFoundError, InvalidBookingStateError
)
from services.booking_service import (
    get_user_role_from_db, create_online_booking, create_walkin_booking,
    cancel_booking, checkin_booking, move_booking_room, add_extra_service,
    get_bookings_list, get_booking_by_id, search_bookings, get_active_bookings,
    get_invoice_details, get_cancel_preview, mark_noshow, get_room_plan_matrix
)
from services.checkout_service import get_checkout_statement, process_checkout
from services.room_lock_service import create_room_hold_lock, get_available_inventory_by_room_type
from services.checkin_service import get_assignable_clean_rooms, assign_room_and_checkin

booking_bp = Blueprint('booking_bp', __name__)

def _require_staff():
    role = get_user_role_from_db(g.api_user_id, g.api_account_type or 'staff')
    if role not in ('Receptionist', 'Manager', 'Admin'):
        return jsonify({'success': False, 'message': 'Yêu cầu quyền hạn nhân sự.'}), 403
    return None

@booking_bp.route('/api/bookings', methods=['GET'])
def api_get_bookings():
    err = require_token()
    if err: return err
    role = get_user_role_from_db(g.api_user_id, g.api_account_type or 'customer') or 'Guest'
    bookings = get_bookings_list(
        g.api_user_id, role,
        status_filter=request.args.get('status', ''),
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 20, type=int)
    )
    return jsonify({'success': True, 'bookings': bookings}), 200

@booking_bp.route('/api/bookings/<int:booking_id>', methods=['GET'])
def api_get_booking_by_id(booking_id):
    err = require_token()
    if err: return err
    booking = get_booking_by_id(booking_id)
    if not booking:
        return jsonify({'success': False, 'message': f'Không tìm thấy đơn đặt phòng #{booking_id}.'}), 404
    if not can_access_customer_booking(booking.get('customer_id')):
        return jsonify({'success': False, 'message': 'Không có quyền truy cập.'}), 403
    return jsonify({'success': True, 'booking': booking}), 200

@booking_bp.route('/api/bookings', methods=['POST'])
def api_create_booking():
    data = request.get_json() or {}
    customer_id = getattr(g, 'api_user_id', None) or data.get('customer_id') or 1
    try:
        ok, res, msg = create_online_booking(data, customer_account_id=customer_id, raise_on_error=True)
        return jsonify({'success': True, 'message': msg, **res}), 201
    except RoomAlreadyLockedError as e:
        return jsonify({'success': False, 'message': str(e)}), 409
    except (RoomNotAvailableError, PromotionInvalidError, ValueError) as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'}), 500

@booking_bp.route('/api/bookings/walkin', methods=['POST'])
def api_create_walkin():
    err = require_token() or _require_staff()
    staff_id = getattr(g, 'api_user_id', None) or 1
    data = request.get_json() or {}
    try:
        ok, res, msg = create_walkin_booking(data, staff_account_id=staff_id, raise_on_error=True)
        return jsonify({'success': True, 'message': msg, **res}), 201
    except (RoomNotAvailableError, ValueError) as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi tạo đơn walk-in: {str(e)}'}), 500

@booking_bp.route('/api/bookings/<int:booking_id>/cancel', methods=['PUT'])
def api_cancel_booking(booking_id):
    reason = (request.get_json() or {}).get('cancel_reason', '')
    user_id = getattr(g, 'api_user_id', None)
    try:
        ok, res, msg = cancel_booking(booking_id, reason=reason, canceled_by_user_id=user_id, raise_on_error=True)
        return jsonify({'success': True, 'message': msg, **res}), 200
    except BookingNotFoundError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except InvalidBookingStateError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi hủy phòng: {str(e)}'}), 500

@booking_bp.route('/api/bookings/<int:booking_id>/checkout-statement', methods=['GET'])
def api_checkout_statement(booking_id):
    try:
        statement = get_checkout_statement(booking_id, raise_on_error=True)
        return jsonify({'success': True, 'statement': statement}), 200
    except BookingNotFoundError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi lấy bảng kê: {str(e)}'}), 500

@booking_bp.route('/api/bookings/<int:booking_id>/checkout', methods=['PUT'])
def api_checkout_process(booking_id):
    pm = (request.get_json() or {}).get('payment_method', 'cash')
    staff_id = getattr(g, 'api_user_id', None)
    try:
        ok, res, msg = process_checkout(booking_id, staff_user_id=staff_id, payment_method=pm, raise_on_error=True)
        return jsonify({'success': True, 'message': msg, **res}), 200
    except BookingNotFoundError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except InvalidBookingStateError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi quyết toán: {str(e)}'}), 500

@booking_bp.route('/api/bookings/<int:booking_id>/extra-services', methods=['GET', 'POST'])
@booking_bp.route('/api/bookings/<int:booking_id>/extra-service', methods=['POST'])
def api_extra_services(booking_id):
    if request.method == 'GET':
        ok, data, msg = get_invoice_details(booking_id)
        return jsonify({'success': ok, 'services': data.get('extra_services', []) if ok else [], 'message': msg if not ok else ''}), 200 if ok else 404
    d = request.get_json() or {}
    ok, res, msg = add_extra_service(
        booking_id, service_name=d.get('service_name', 'Dịch vụ thêm'),
        quantity=int(d.get('quantity', 1)), unit_price=int(round(float(d.get('unit_price', 0)))),
        added_by=getattr(g, 'api_user_id', None)
    )
    return jsonify({'success': ok, 'message': msg, **res}), 201 if ok else 400

@booking_bp.route('/api/room-plan', methods=['GET'])
def api_room_plan():
    return jsonify({'success': True, **get_room_plan_matrix(request.args.get('start_date'), request.args.get('days', 7, type=int))}), 200

@booking_bp.route('/api/room-plan/move', methods=['POST'])
@booking_bp.route('/api/bookings/<int:booking_id>/move-room', methods=['PUT'])
def api_move_room(booking_id=None):
    d = request.get_json() or {}
    b_id = booking_id or d.get('booking_id')
    new_room = d.get('new_physical_room_id')
    if not b_id or not new_room:
        return jsonify({'success': False, 'message': 'Thiếu booking_id hoặc new_physical_room_id'}), 400
    ok, msg = move_booking_room(int(b_id), int(new_room))
    return jsonify({'success': ok, 'message': msg}), 200 if ok else 400

# ─── FRONTEND COMPATIBILITY HELPERS ──────────────────────────────────────────
@booking_bp.route('/api/bookings/search', methods=['GET'])
def api_search():
    q = request.args.get('q', '').strip()
    return jsonify({'success': bool(q), 'bookings': search_bookings(q) if q else []}), 200

@booking_bp.route('/api/bookings/active', methods=['GET'])
def api_active():
    return jsonify({'success': True, 'active_bookings': get_active_bookings()}), 200

@booking_bp.route('/api/bookings/invoice/<int:booking_id>', methods=['GET'])
def api_invoice(booking_id):
    ok, data, msg = get_invoice_details(booking_id)
    return jsonify({'success': ok, 'message': msg, **(data if ok else {})}), 200 if ok else 404

@booking_bp.route('/api/bookings/cancel-preview/<int:booking_id>', methods=['GET'])
def api_cancel_prev(booking_id):
    ok, data, msg = get_cancel_preview(booking_id)
    return jsonify({'success': ok, 'message': msg, **(data if ok else {})}), 200 if ok else 400

@booking_bp.route('/api/bookings/<int:booking_id>/checkin', methods=['PUT'])
def api_checkin_booking(booking_id):
    ok, msg = checkin_booking(booking_id, staff_account_id=getattr(g, 'api_user_id', None))
    return jsonify({'success': ok, 'message': msg}), 200 if ok else 400

@booking_bp.route('/api/bookings/<int:booking_id>/noshow', methods=['PUT'])
def api_noshow(booking_id):
    ok, msg = mark_noshow(booking_id)
    return jsonify({'success': ok, 'message': msg}), 200 if ok else 400


# ─── B2C HOLD LOCK (TTL 15M) & FRONT-DESK DYNAMIC ASSIGNMENT ─────────────────
@booking_bp.route('/api/rooms/hold', methods=['POST'])
def api_hold_room():
    """Khách đặt online tạo phiên khóa giữ chỗ 15 phút theo loại phòng (chống overbooking)."""
    d = request.get_json() or {}
    rt_id = d.get('room_type_id')
    arr = d.get('arrival_date')
    dep = d.get('departure_date')
    sess = d.get('session_id') or 'sess_anon'
    qty = int(d.get('quantity', 1))

    if not all([rt_id, arr, dep]):
        return jsonify({'success': False, 'message': 'Thiếu room_type_id, arrival_date hoặc departure_date.'}), 400

    res = create_room_hold_lock(int(rt_id), sess, str(arr), str(dep), quantity=qty, ttl_minutes=15)
    return jsonify(res), 200 if res.get('success') else 409


@booking_bp.route('/api/frontdesk/assignable-rooms/<int:booking_id>', methods=['GET'])
def api_get_assignable_rooms(booking_id):
    """Lễ tân truy vấn danh sách phòng vật lý Clean khả dụng để gán cho booking."""
    ok, rooms, msg = get_assignable_clean_rooms(booking_id)
    return jsonify({'success': ok, 'rooms': rooms, 'message': msg}), 200 if ok else 400


@booking_bp.route('/api/frontdesk/assign-and-checkin', methods=['POST'])
def api_assign_and_checkin():
    """Hiện thực hóa ganPhong(room) và Check-in động tại quầy tiền sảnh."""
    d = request.get_json() or {}
    b_id = d.get('booking_id')
    pr_id = d.get('physical_room_id')
    staff_id = getattr(g, 'api_user_id', None) or 1

    if not b_id or not pr_id:
        return jsonify({'success': False, 'message': 'Thiếu booking_id hoặc physical_room_id.'}), 400

    ok, res, msg = assign_room_and_checkin(int(b_id), int(pr_id), staff_user_id=staff_id)
    return jsonify({'success': ok, 'data': res, 'message': msg}), 200 if ok else 400

