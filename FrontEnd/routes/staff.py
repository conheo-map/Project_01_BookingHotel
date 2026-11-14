from datetime import date, datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.api import api_get, api_post, api_put, get_checkout_statement, process_checkout, create_walkin_booking

staff_bp = Blueprint('staff', __name__)


def _require_staff(roles=('Receptionist', 'Manager', 'Admin', 'Housekeeper')):
    if not session.get('token'):
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    if session.get('account_type') != 'staff':
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('search.home'))
    if session.get('role') not in roles:
        flash('Bạn không đủ quyền hạn.', 'error')
        return redirect(url_for('search.home'))
    return None


# ── Receptionist Dashboard ─────────────────────────────────────────────────────

ROOM_TYPE_NAME_MAP = {
    'CIT_SUI': 'Phòng City Suite',
    'CIT_DEL': 'Phòng City Deluxe',
    'CIT_SUP': 'Phòng City Superior',
    'RES_VDEL': 'Villa Deluxe Hướng Vườn',
    'RES_VSUI': 'Villa Suite Hướng Biển',
    'RES_VSUP': 'Villa Superior Cao Cấp',
}


@staff_bp.route('/receptionist')
def receptionist():
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    q = request.args.get('q', '').strip()
    status = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1

    per_page = 25
    if q:
        bookings = api_get('/api/bookings/search', params={'q': q}).get('bookings', [])
        total_bookings = len(bookings)
        total_pages = 1
    else:
        params = {'per_page': per_page, 'page': page}
        if status:
            params['status'] = status
        res = api_get('/api/bookings', params=params)
        bookings = res.get('bookings', [])
        total_bookings = res.get('total', len(bookings))
        total_pages = max(1, (total_bookings + per_page - 1) // per_page)

    ops = api_get('/api/operations/realtime')
    catalog = api_get('/api/service-catalog').get('catalog', [])
    today = date.today().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M')
    return render_template('receptionist.html',
                           bookings=bookings, ops=ops, catalog=catalog,
                           q=q, status=status, today=today, now_time=now_time,
                           page=page, total_pages=total_pages, total_bookings=total_bookings,
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


@staff_bp.route('/receptionist/room-plan')
def room_plan():
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    room_types = api_get('/api/inventory/comprehensive').get('inventory', [])
    ops = api_get('/api/operations/realtime')
    # Enrich hotel_name
    hotels = api_get('/api/hotels').get('hotels', [])
    hotel_map = {h['hotel_id']: h.get('hotel_name', '') for h in hotels}
    for rt in room_types:
        rt['hotel_name'] = hotel_map.get(rt.get('hotel_id'), '')
    return render_template('receptionist_room_plan.html', room_types=room_types, ops=ops, room_type_name_map=ROOM_TYPE_NAME_MAP)


@staff_bp.route('/receptionist/quick-clean/<int:room_id>', methods=['POST'])
def quick_clean(room_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    result = api_put(f'/api/physical-rooms/{room_id}', {'housekeeping_status': 'Clean'})
    flash('Phòng đã được chuyển sang trạng thái Sạch (Clean) thành công!' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('staff.room_plan'))


# ── Booking Actions ────────────────────────────────────────────────────────────

@staff_bp.route('/receptionist/checkin/<int:booking_id>', methods=['POST'])
def checkin(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    result = api_put(f'/api/bookings/{booking_id}/checkin', {})
    flash('Check-in thành công!' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('staff.receptionist'))


@staff_bp.route('/receptionist/checkout/<int:booking_id>', methods=['GET', 'POST'])
def do_checkout(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    if request.method == 'POST':
        pm = request.form.get('payment_method', 'cash')
        result = process_checkout(booking_id, payment_method=pm)
        flash('Check-out thành công!' if result.get('success') else result.get('message', 'Thất bại'),
              'success' if result.get('success') else 'error')
        return redirect(url_for('staff.receptionist'))

    statement_res = get_checkout_statement(booking_id)
    statement = statement_res.get('statement') or statement_res
    invoice_data = api_get(f'/api/bookings/invoice/{booking_id}')
    catalog = api_get('/api/service-catalog').get('catalog', [])
    return render_template('receptionist_checkout_detail.html',
                           booking=invoice_data.get('booking') or {},
                           statement=statement,
                           extra_services=invoice_data.get('extra_services', []),
                           payments=invoice_data.get('payments', []),
                           extra_grand_total=invoice_data.get('extra_grand_total', 0),
                           catalog=catalog,
                           booking_id=booking_id,
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


@staff_bp.route('/receptionist/noshow/<int:booking_id>', methods=['GET', 'POST'])
def noshow(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    if request.method == 'POST':
        result = api_put(f'/api/bookings/{booking_id}/noshow', {})
        flash('Đã đánh dấu No-Show.' if result.get('success') else result.get('message', 'Thất bại'),
              'success' if result.get('success') else 'error')
        return redirect(url_for('staff.receptionist'))
    invoice_data = api_get(f'/api/bookings/invoice/{booking_id}')
    return render_template('receptionist_noshow.html',
                           booking=invoice_data.get('booking') or {},
                           booking_id=booking_id)


@staff_bp.route('/receptionist/add-service/<int:booking_id>', methods=['POST'])
def add_service(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    result = api_post(f'/api/bookings/{booking_id}/extra-services', {
        'service_name': request.form.get('service_name', ''),
        'quantity': request.form.get('quantity', 1, type=int),
        'unit_price': request.form.get('unit_price', 0.0, type=float),
        'catalog_id': request.form.get('catalog_id', type=int),
    })
    flash('Đã thêm dịch vụ.' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('staff.do_checkout', booking_id=booking_id))


@staff_bp.route('/receptionist/cancel/<int:booking_id>', methods=['GET', 'POST'])
def cancel_booking(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    if request.method == 'POST':
        result = api_put(f'/api/bookings/{booking_id}/cancel', {
            'cancel_reason': request.form.get('cancel_reason', '').strip(),
        })
        flash('Đã hủy đặt phòng.' if result.get('success') else result.get('message', 'Thất bại'),
              'success' if result.get('success') else 'error')
        return redirect(url_for('staff.receptionist'))
    preview = api_get(f'/api/bookings/cancel-preview/{booking_id}').get('preview') or {}
    return render_template('receptionist_cancel.html', preview=preview, booking_id=booking_id)


@staff_bp.route('/receptionist/invoice/<int:booking_id>')
def invoice(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    invoice_data = api_get(f'/api/bookings/invoice/{booking_id}')
    if not invoice_data.get('success'):
        flash(invoice_data.get('message', 'Không tìm thấy hóa đơn.'), 'error')
        return redirect(url_for('staff.receptionist'))
    return render_template('receptionist_invoice.html',
                           booking=invoice_data.get('booking') or {},
                           extra_services=invoice_data.get('extra_services', []),
                           payments=invoice_data.get('payments', []),
                           extra_grand_total=invoice_data.get('extra_grand_total', 0),
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


@staff_bp.route('/receptionist/move-room/<int:booking_id>', methods=['GET', 'POST'])
def move_room(booking_id):
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    if request.method == 'POST':
        result = api_put(f'/api/bookings/{booking_id}/move-room', {
            'new_physical_room_id': request.form.get('new_physical_room_id', type=int),
            'reason': request.form.get('reason', '').strip(),
        })
        flash('Đã chuyển phòng thành công.' if result.get('success') else result.get('message', 'Thất bại'),
              'success' if result.get('success') else 'error')
        return redirect(url_for('staff.receptionist'))
    invoice_data = api_get(f'/api/bookings/invoice/{booking_id}')
    room_types = api_get('/api/inventory/comprehensive').get('inventory', [])
    return render_template('receptionist_move_room.html',
                           booking=invoice_data.get('booking') or {},
                           room_types=room_types,
                           booking_id=booking_id)


@staff_bp.route('/receptionist/walkin', methods=['GET', 'POST'])
def walkin():
    err = _require_staff(('Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    if request.method == 'POST':
        payload = {
            'customer_name': request.form.get('customer_name', '').strip(),
            'customer_phone': request.form.get('customer_phone', '').strip(),
            'guest_email': request.form.get('guest_email', '').strip(),
            'hotel_id': request.form.get('hotel_id', type=int),
            'room_type_id': request.form.get('room_type_id', type=int),
            'physical_room_id': request.form.get('physical_room_id', type=int),
            'checkin_date': request.form.get('checkin_date', ''),
            'checkout_date': request.form.get('checkout_date', ''),
            'adults': request.form.get('adults', 1, type=int),
            'children': request.form.get('children', 0, type=int),
            'deposit_paid': request.form.get('deposit_paid', 0.0, type=float),
            'payment_method': request.form.get('payment_method', 'cash'),
            'special_requests': request.form.get('special_requests', '').strip(),
        }
        result = create_walkin_booking(payload)
        if result.get('success'):
            flash(f"Walk-in #{result.get('booking_id')} tạo thành công!", 'success')
            return redirect(url_for('staff.receptionist'))
        flash(result.get('message', 'Tạo walk-in thất bại.'), 'error')
    hotels = api_get('/api/hotels').get('hotels', [])
    room_types = api_get('/api/inventory/comprehensive').get('inventory', [])
    today = date.today().strftime('%Y-%m-%d')
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    return render_template('receptionist_walkin_booking.html',
                           hotels=hotels, room_types=room_types,
                           today=today, tomorrow=tomorrow,
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


# ── Housekeeping ───────────────────────────────────────────────────────────────

@staff_bp.route('/housekeeping')
def housekeeping():
    err = _require_staff(('Housekeeper', 'Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    rooms = api_get('/api/housekeeping/rooms?all=1').get('rooms', [])
    ops = api_get('/api/operations/realtime')
    return render_template('housekeeping_dashboard.html',
                           rooms=rooms,
                           ops=ops,
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


@staff_bp.route('/housekeeping/clean/<int:room_id>', methods=['POST'])
def mark_clean(room_id):
    err = _require_staff(('Housekeeper', 'Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    result = api_post(f'/api/housekeeping/rooms/{room_id}/clean', {})
    flash('Phòng đã được đánh dấu sạch.' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('staff.housekeeping'))


@staff_bp.route('/housekeeping/status/<int:room_id>', methods=['POST'])
def update_housekeeping_status(room_id):
    err = _require_staff(('Housekeeper', 'Receptionist', 'Manager', 'Admin'))
    if err:
        return err
    new_status = request.form.get('housekeeping_status', 'Clean')
    result = api_post(f'/api/housekeeping/rooms/{room_id}/status', {
        'housekeeping_status': new_status
    })
    status_label = {'Clean': 'Sạch', 'Dirty': 'Cần dọn', 'Maintenance': 'Bảo trì kỹ thuật'}.get(new_status, new_status)
    flash(f'Đã cập nhật phòng sang trạng thái {status_label}.' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('staff.housekeeping'))
