from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from services.api import api_get, api_post, api_put, api_delete, api_upload

management_bp = Blueprint('management', __name__)


def _require_manager(roles=('Manager', 'Admin')):
    if not session.get('token'):
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    if session.get('account_type') != 'staff':
        flash('Không có quyền truy cập.', 'error')
        return redirect(url_for('search.home'))
    if session.get('role') not in roles:
        flash('Bạn không đủ quyền hạn để truy cập khu vực quản lý.', 'error')
        return redirect(url_for('search.home'))
    return None


# ── Analytics ──────────────────────────────────────────────────────────────────

@management_bp.route('/analytics')
def analytics():
    err = _require_manager(('Manager', 'Admin', 'Receptionist'))
    if err:
        return err
    group_by = request.args.get('group_by', 'month')
    year = request.args.get('year', datetime.now().year, type=int)
    hotel_id = request.args.get('hotel_id', type=int)
    params = {'group_by': group_by, 'year': year}
    if hotel_id:
        params['hotel_id'] = hotel_id
    res = api_get('/api/analytics/advanced', params=params)
    data = res.get('data', [])
    summary_period = res.get('summary_period')
    if not summary_period:
        tot_bookings = sum(d.get('total_bookings', 0) for d in data)
        tot_canceled = sum(d.get('total_canceled', 0) for d in data)
        tot_revenue = sum(d.get('revenue', 0) for d in data)
        tot_nights = sum(d.get('total_nights', 0) for d in data)
        summary_period = {
            'total_bookings': tot_bookings,
            'total_canceled': tot_canceled,
            'total_revenue': tot_revenue,
            'total_nights': tot_nights,
            'cancel_rate': round(100.0 * tot_canceled / tot_bookings, 1) if tot_bookings > 0 else 0.0,
            'avg_adr': round(tot_revenue / tot_nights, 0) if tot_nights > 0 else 0
        }

    summary = api_get('/api/analytics/summary').get('summary', {})
    hotels = api_get('/api/hotels').get('hotels', [])
    ops = api_get('/api/operations/realtime')
    conversion = api_get('/api/analytics/conversion', params={'days': 30})
    return render_template('analytics.html',
                           analytics_data=data,
                           summary=summary,
                           summary_period=summary_period,
                           hotels=hotels,
                           group_by=group_by,
                           year=year,
                           selected_hotel=hotel_id,
                           ops=ops,
                           conversion=conversion)


# ── Manager Dashboard ──────────────────────────────────────────────────────────

@management_bp.route('/manager')
def manager_dashboard():
    err = _require_manager()
    if err:
        return err
    summary = api_get('/api/analytics/summary')
    ops = api_get('/api/operations/realtime')
    bookings = api_get('/api/bookings', params={'per_page': 10}).get('bookings', [])
    hotels = api_get('/api/hotels').get('hotels', [])
    return render_template('manager_dashboard.html',
                           summary=summary.get('summary', {}),
                           by_hotel=summary.get('by_hotel', []),
                           ops=ops,
                           bookings=bookings,
                           hotels=hotels)


ROOM_TYPE_NAME_MAP = {
    'CIT_SUI': 'Phòng City Suite',
    'CIT_DEL': 'Phòng City Deluxe',
    'CIT_SUP': 'Phòng City Superior',
    'RES_VDEL': 'Villa Deluxe Hướng Vườn',
    'RES_VSUI': 'Villa Suite Hướng Biển',
    'RES_VSUP': 'Villa Superior Cao Cấp',
}

ROOM_SPECS = {
    'CIT_DEL': {'area': '32 m²', 'bed': '1 Giường đôi hoặc 2 Giường đơn', 'view': 'View phố cổ Côn Đảo', 'bath': 'Bồn tắm đứng cao cấp'},
    'CIT_SUP': {'area': '28 m²', 'bed': '1 Giường King lớn', 'view': 'View vườn nhiệt đới', 'bath': 'Bồn tắm đứng cao cấp'},
    'CIT_SUI': {'area': '52 m²', 'bed': '1 Giường King & phòng khách', 'view': 'View toàn cảnh Côn Đảo', 'bath': 'Bồn tắm nằm & bồn đứng'},
    'RES_VDEL': {'area': '45 m²', 'bed': '1 Giường King lớn', 'view': 'View biển Côn Sơn', 'bath': 'Bồn tắm nằm ngắm biển'},
    'RES_VSUI': {'area': '65 m²', 'bed': '1 Giường Super King', 'view': 'Trực diện bãi biển', 'bath': 'Bồn Jacuzzi & tắm ngoài trời'},
    'RES_VSUP': {'area': '38 m²', 'bed': '1 Giường đôi Queen', 'view': 'View vườn xanh mát', 'bath': 'Bồn tắm đứng hiện đại'},
}

# ── Inventory & Pricing ────────────────────────────────────────────────────────

@management_bp.route('/manager/inventory-pricing', methods=['GET', 'POST'])
def inventory_pricing():
    err = _require_manager()
    if err:
        return err
    hotel_id = request.args.get('hotel_id', type=int)
    if request.method == 'POST':
        payload = {
            'mode': request.form.get('mode', 'type'),
            'target_id': request.form.get('target_id', '').strip() or request.form.get('room_type_code', '').strip(),
            'start_date': request.form.get('start_date', ''),
            'end_date': request.form.get('end_date', ''),
            'new_price': request.form.get('new_price', type=float),
            'is_holiday': 1 if request.form.get('is_holiday') else 0,
        }
        result = api_post('/api/room-rates/comprehensive', payload)
        flash('Cập nhật giá thành công!' if result.get('success') else result.get('message', 'Thất bại'),
              'success' if result.get('success') else 'error')
        return redirect(url_for('management.inventory_pricing', hotel_id=hotel_id))
    params = {'hotel_id': hotel_id} if hotel_id else {}
    data = api_get('/api/inventory/comprehensive', params=params)
    inventory = data.get('inventory', [])
    dates = data.get('dates', [])
    hotels = api_get('/api/hotels').get('hotels', [])

    total_rooms = sum(len(rt.get('physical_rooms', [])) for rt in inventory)
    total_clean = sum(sum(1 for pr in rt.get('physical_rooms', []) if pr.get('housekeeping_status') == 'Clean') for rt in inventory)
    total_occupied = sum(sum(1 for pr in rt.get('physical_rooms', []) if pr.get('current_booking_id')) for rt in inventory)
    total_dirty = sum(sum(1 for pr in rt.get('physical_rooms', []) if pr.get('housekeeping_status') == 'Dirty') for rt in inventory)
    avg_price = int(sum(rt.get('base_price', 0) for rt in inventory) / len(inventory)) if inventory else 0

    return render_template('manager_inventory_pricing.html',
                           inventory=inventory, hotels=hotels, selected_hotel=hotel_id,
                           room_type_name_map=ROOM_TYPE_NAME_MAP, room_specs=ROOM_SPECS,
                           total_rooms=total_rooms, total_clean=total_clean,
                           total_occupied=total_occupied, total_dirty=total_dirty,
                           avg_price=avg_price, dates=dates)

@management_bp.route('/manager/room-pricing-detailed')
def room_pricing_detailed():
    err = _require_manager()
    if err:
        return err
    hotel_id = request.args.get('hotel_id', type=int)
    start_date_str = request.args.get('start_date')
    
    # Mặc định hôm nay nếu không có start_date
    if start_date_str:
        try:
            current_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except:
            current_date = date.today()
    else:
        current_date = date.today()
        
    prev_week = (current_date - timedelta(days=7)).strftime('%Y-%m-%d')
    next_week = (current_date + timedelta(days=7)).strftime('%Y-%m-%d')
    start_date_str = current_date.strftime('%Y-%m-%d')
    
    params = {'hotel_id': hotel_id, 'start_date': start_date_str} if hotel_id else {'start_date': start_date_str}
    data = api_get('/api/inventory/comprehensive', params=params)
    inventory = data.get('inventory', [])
    dates = data.get('dates', [])
    hotels = api_get('/api/hotels').get('hotels', [])

    total_rooms = sum(len(rt.get('physical_rooms', [])) for rt in inventory)
    total_clean = sum(sum(1 for pr in rt.get('physical_rooms', []) if pr.get('housekeeping_status') == 'Clean') for rt in inventory)
    total_occupied = sum(sum(1 for pr in rt.get('physical_rooms', []) if pr.get('current_booking_id')) for rt in inventory)
    
    return render_template('manager_room_pricing_detailed.html',
                           inventory=inventory, hotels=hotels, selected_hotel=hotel_id,
                           dates=dates, start_date=start_date_str, 
                           prev_week=prev_week, next_week=next_week,
                           room_type_name_map=ROOM_TYPE_NAME_MAP, room_specs=ROOM_SPECS,
                           total_rooms=total_rooms, total_clean=total_clean,
                           total_occupied=total_occupied)


# ── Physical Rooms ─────────────────────────────────────────────────────────────

@management_bp.route('/manager/physical-rooms', methods=['GET', 'POST'])
def physical_rooms():
    err = _require_manager()
    if err:
        return err
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'create':
            result = api_post('/api/physical-rooms', {
                'room_type_id': request.form.get('room_type_id', type=int),
                'room_name': request.form.get('room_name', '').strip(),
            })
            flash('Tạo phòng thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'delete':
            pr_id = request.form.get('physical_room_id', type=int)
            result = api_delete(f'/api/physical-rooms/{pr_id}')
            flash('Đã ẩn phòng.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'update_status':
            pr_id = request.form.get('physical_room_id', type=int)
            new_status = request.form.get('housekeeping_status', 'Clean')
            result = api_put(f'/api/physical-rooms/{pr_id}', {'housekeeping_status': new_status})
            flash('Cập nhật trạng thái thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        return redirect(url_for('management.physical_rooms'))
    inventory = api_get('/api/inventory/comprehensive').get('inventory', [])
    room_types = api_get('/api/dimensions/room-types').get('room_types', [])
    hotels = api_get('/api/hotels').get('hotels', [])

    total_rooms = sum(len(rt.get('physical_rooms', [])) for rt in inventory)
    occupied_rooms = sum(1 for rt in inventory for pr in rt.get('physical_rooms', []) if pr.get('current_booking_id'))
    dirty_rooms = sum(1 for rt in inventory for pr in rt.get('physical_rooms', []) if pr.get('housekeeping_status') == 'Dirty')
    maintenance_rooms = sum(1 for rt in inventory for pr in rt.get('physical_rooms', []) if pr.get('housekeeping_status') == 'Maintenance')
    clean_vacant = max(0, total_rooms - occupied_rooms - dirty_rooms - maintenance_rooms)

    metrics = {
        'total': total_rooms,
        'occupied': occupied_rooms,
        'clean_vacant': clean_vacant,
        'dirty': dirty_rooms,
        'maintenance': maintenance_rooms,
    }

    return render_template('manager_physical_rooms.html',
                           inventory=inventory,
                           room_types=room_types,
                           hotels=hotels,
                           metrics=metrics)


# ── Promotions ─────────────────────────────────────────────────────────────────

@management_bp.route('/manager/promotions', methods=['GET', 'POST'])
def promotions():
    err = _require_manager()
    if err:
        return err
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'create':
            result = api_post('/api/promotions', {
                'promo_code': request.form.get('promo_code', '').strip(),
                'discount_percent': request.form.get('discount_percent', 0, type=float),
                'discount_type': request.form.get('discount_type', 'percent'),
                'start_date': request.form.get('start_date') or None,
                'end_date': request.form.get('end_date') or None,
                'description': request.form.get('description', '').strip(),
                'apply_scope': request.form.get('apply_scope', 'all'),
                'scope_value': request.form.get('scope_value', '').strip(),
                'max_uses': request.form.get('max_uses', 0, type=int),
                'membership_tier_required': request.form.get('membership_tier_required', 'All').strip() or 'All',
            })
            flash('Tạo khuyến mãi thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'delete':
            promo_id = request.form.get('promo_id', type=int)
            result = api_delete(f'/api/promotions/{promo_id}')
            flash('Đã xóa khuyến mãi.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'toggle':
            promo_id = request.form.get('promo_id', type=int)
            is_active = request.form.get('is_active', '0') == '1'
            all_promos = api_get('/api/promotions').get('promotions', [])
            promo = next((p for p in all_promos if p.get('promo_id') == promo_id), {})
            result = api_put(f'/api/promotions/{promo_id}', {**promo, 'is_active': 0 if is_active else 1})
            flash('Cập nhật thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        return redirect(url_for('management.promotions'))
    promos = api_get('/api/promotions').get('promotions', [])
    room_types = api_get('/api/dimensions/room-types').get('room_types', [])
    hotels = api_get('/api/hotels').get('hotels', [])

    total_promos = len(promos)
    active_promos = sum(1 for p in promos if p.get('is_active'))
    max_discount = max([p.get('discount_percent', 0) for p in promos if p.get('discount_type') == 'percent'] or [0])
    member_promos = sum(1 for p in promos if p.get('apply_scope') in ('membership', 'tier'))

    return render_template('manager_promotions.html',
                           promotions=promos, room_types=room_types, hotels=hotels,
                           total_promos=total_promos, active_promos=active_promos,
                           max_discount=max_discount, member_promos=member_promos,
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


# ── Refund Policy ──────────────────────────────────────────────────────────────

@management_bp.route('/manager/refund-policy', methods=['GET', 'POST'])
def refund_policy():
    err = _require_manager()
    if err:
        return err
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'create':
            days = request.form.get('days_before_arrival', type=float) or 0
            hours = request.form.get('hours_before_checkin', type=float)
            if hours is None and days:
                hours = days * 24.0
            elif days == 0 and hours:
                days = hours / 24.0
            result = api_post('/api/refund-policy', {
                'hours_before_checkin': hours or 0,
                'days_before_arrival': days or 0,
                'refund_percent': request.form.get('refund_percent', type=float),
                'description': request.form.get('description', '').strip(),
            })
            flash('Tạo chính sách hoàn tiền thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'delete':
            policy_id = request.form.get('policy_id', type=int)
            result = api_delete(f'/api/refund-policy/{policy_id}')
            flash('Đã xóa chính sách hoàn tiền.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        return redirect(url_for('management.refund_policy'))
    policies = api_get('/api/refund-policy').get('policies', [])
    total_tiers = len(policies)
    max_refund = max([p.get('refund_percent', 0) for p in policies] or [0])
    min_refund = min([p.get('refund_percent', 0) for p in policies] or [0])
    strict_tier = next((p for p in policies if p.get('refund_percent') == 0), {})

    return render_template('manager_refund_policy.html', 
                           policies=policies,
                           total_tiers=total_tiers,
                           max_refund=max_refund,
                           min_refund=min_refund,
                           strict_tier=strict_tier)


# ── Room Rates ─────────────────────────────────────────────────────────────────

@management_bp.route('/manager/room-rates', methods=['GET', 'POST'])
def room_rates():
    err = _require_manager()
    if err:
        return err
    if request.method == 'POST':
        result = api_post('/api/room-rates/comprehensive', {
            'mode': request.form.get('mode', 'type'),
            'target_id': request.form.get('target_id', '').strip(),
            'start_date': request.form.get('start_date', ''),
            'end_date': request.form.get('end_date', ''),
            'new_price': request.form.get('new_price', type=float),
            'is_holiday': 1 if request.form.get('is_holiday') else 0,
        })
        flash('Cập nhật giá thành công!' if result.get('success') else result.get('message', 'Thất bại'),
              'success' if result.get('success') else 'error')
        return redirect(url_for('management.room_rates'))
    room_type_code = request.args.get('room_type_code', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    params = {}
    if room_type_code:
        params['room_type_code'] = room_type_code
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    rates = api_get('/api/room-rates', params=params).get('rates', [])
    room_types = api_get('/api/dimensions/room-types').get('room_types', [])
    return render_template('manager_room_rates.html',
                           rates=rates, room_types=room_types,
                           filters={'room_type_code': room_type_code,
                                    'start_date': start_date,
                                    'end_date': end_date})


# ── Room Catalog ───────────────────────────────────────────────────────────────

@management_bp.route('/manager/room-catalog', methods=['GET', 'POST'])
def room_catalog():
    err = _require_manager()
    if err:
        return err
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'create':
            result = api_post('/api/dimensions/room-types', {
                'room_type_code': request.form.get('room_type_code', '').strip(),
                'hotel_id': request.form.get('hotel_id', 1, type=int),
                'max_adults': request.form.get('max_adults', 2, type=int),
                'max_children': request.form.get('max_children', 1, type=int),
                'base_price': request.form.get('base_price', 100.0, type=float),
                'description': request.form.get('description', '').strip(),
                'amenities': request.form.get('amenities', '').strip(),
                'allow_child_sharing': 1 if request.form.get('allow_child_sharing') else 0,
                'extra_bed_capacity': request.form.get('extra_bed_capacity', 0, type=int),
                'extra_adult_fee': request.form.get('extra_adult_fee', 0.0, type=float),
                'child_breakfast_fee': request.form.get('child_breakfast_fee', 0.0, type=float),
            })
            flash('Tạo loại phòng thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'update':
            rt_id = request.form.get('room_type_id', type=int)
            result = api_put(f'/api/dimensions/room-types/{rt_id}', {
                'room_type_code': request.form.get('room_type_code', '').strip(),
                'hotel_id': request.form.get('hotel_id', 1, type=int),
                'max_adults': request.form.get('max_adults', 2, type=int),
                'max_children': request.form.get('max_children', 1, type=int),
                'base_price': request.form.get('base_price', 100.0, type=float),
                'description': request.form.get('description', '').strip(),
                'amenities': request.form.get('amenities', '').strip(),
                'allow_child_sharing': 1 if request.form.get('allow_child_sharing') else 0,
                'extra_bed_capacity': request.form.get('extra_bed_capacity', 0, type=int),
                'extra_adult_fee': request.form.get('extra_adult_fee', 0.0, type=float),
                'child_breakfast_fee': request.form.get('child_breakfast_fee', 0.0, type=float),
                'is_active': 1,
            })
            flash('Cập nhật thành công!' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'delete':
            rt_id = request.form.get('room_type_id', type=int)
            result = api_delete(f'/api/dimensions/room-types/{rt_id}')
            flash('Đã xóa loại phòng.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        return redirect(url_for('management.room_catalog'))
    room_types = api_get('/api/dimensions/room-types').get('room_types', [])
    hotels = api_get('/api/hotels').get('hotels', [])
    return render_template('manager_room_catalog.html',
                           room_types=room_types,
                           hotels=hotels,
                           room_type_name_map=ROOM_TYPE_NAME_MAP,
                           room_specs=ROOM_SPECS)


# ── Room Edit (Chi tiết loại phòng) ────────────────────────────────────────────

@management_bp.route('/manager/room-edit/<int:room_type_id>', methods=['GET'])
def room_edit(room_type_id):
    err = _require_manager()
    if err:
        return err
    rt_data = api_get(f'/api/dimensions/room-types/{room_type_id}')
    if not rt_data.get('success'):
        flash('Không tìm thấy loại phòng.', 'error')
        return redirect(url_for('management.inventory_pricing'))
    hotels = api_get('/api/hotels').get('hotels', [])
    return render_template('manager_room_edit.html',
                           room_type=rt_data['room_type'],
                           hotels=hotels,
                           room_type_name_map=ROOM_TYPE_NAME_MAP,
                           room_specs=ROOM_SPECS)


@management_bp.route('/manager/room-edit/<int:room_type_id>', methods=['POST'])
def room_edit_save(room_type_id):
    err = _require_manager()
    if err:
        return err
    payload = {
        'room_type_code': request.form.get('room_type_code', '').strip(),
        'hotel_id': request.form.get('hotel_id', 1, type=int),
        'max_adults': request.form.get('max_adults', 2, type=int),
        'max_children': request.form.get('max_children', 1, type=int),
        'base_price': request.form.get('base_price', 100.0, type=float),
        'description': request.form.get('description', '').strip(),
        'amenities': request.form.get('amenities', '').strip(),
        'is_active': 1 if request.form.get('is_active') else 0,
        'allow_child_sharing': 1 if request.form.get('allow_child_sharing') else 0,
        'extra_bed_capacity': request.form.get('extra_bed_capacity', 0, type=int),
        'extra_adult_fee': request.form.get('extra_adult_fee', 0.0, type=float),
        'child_breakfast_fee': request.form.get('child_breakfast_fee', 0.0, type=float),
    }
    result = api_put(f'/api/dimensions/room-types/{room_type_id}', payload)
    flash('Cập nhật thành công!' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.room_edit', room_type_id=room_type_id))


@management_bp.route('/manager/room-edit/<int:room_type_id>/upload', methods=['POST'])
def room_edit_upload(room_type_id):
    err = _require_manager()
    if err:
        return err
    print(f"[FRONTEND] room_edit_upload: RT={room_type_id}")
    if 'image' not in request.files:
        print("[FRONTEND] Error: No 'image' in request.files")
        return jsonify({'success': False, 'message': 'Chưa chọn file ảnh.'})
    
    file = request.files['image']
    print(f"[FRONTEND] Received file: {file.filename}")

    result = api_upload(f'/api/room-types/{room_type_id}/upload-image',
                        files={'image': (file.filename, file.stream, file.content_type)})
    
    print(f"[FRONTEND] Backend result: {result}")
    return jsonify({
        'success': result.get('success', False),
        'message': result.get('message', 'Upload xong'),
        'image_url': result.get('image_url')
    })


@management_bp.route('/manager/room-edit/<int:room_type_id>/delete-image', methods=['POST'])
def room_edit_delete_image(room_type_id):
    err = _require_manager()
    if err:
        return err
    image_url = request.form.get('image_url', '').strip()
    result = api_post(f'/api/room-types/{room_type_id}/delete-image', {'image_url': image_url})
    flash('Đã xóa ảnh.' if result.get('success') else result.get('message', 'Xóa thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.room_edit', room_type_id=room_type_id))


@management_bp.route('/manager/room-edit/<int:room_type_id>/set-main', methods=['POST'])
def room_edit_set_main(room_type_id):
    err = _require_manager()
    if err:
        return err
    image_url = request.form.get('image_url', '').strip()
    result = api_post(f'/api/room-types/{room_type_id}/set-main-image', {'image_url': image_url})
    flash('Đã đặt làm ảnh đại diện.' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.room_edit', room_type_id=room_type_id))


# ── Physical Room Edit (Chỉnh sửa từng phòng) ────────────────────────────────

@management_bp.route('/manager/physical-room-edit/<int:pr_id>', methods=['GET'])
def physical_room_edit(pr_id):
    err = _require_manager()
    if err:
        return err
    room_data = api_get(f'/api/room-detail/{pr_id}')
    if not room_data.get('success'):
        flash('Không tìm thấy phòng.', 'error')
        return redirect(url_for('management.inventory_pricing'))
    # Lấy danh sách loại phòng để cho chuyển đổi
    rt_data = api_get('/api/dimensions/room-types')
    room_types = rt_data.get('room_types', [])
    return render_template('manager_physical_room_edit.html',
                           room=room_data['room'],
                           room_types=room_types,
                           room_type_name_map=ROOM_TYPE_NAME_MAP)


@management_bp.route('/manager/physical-room-edit/<int:pr_id>', methods=['POST'])
def physical_room_edit_save(pr_id):
    err = _require_manager()
    if err:
        return err
    payload = {
        'room_name': request.form.get('room_name', '').strip(),
        'room_type_id': request.form.get('room_type_id', type=int),
        'description': request.form.get('description', '').strip(),
        'amenities': request.form.get('amenities', '').strip(),
        'housekeeping_status': request.form.get('housekeeping_status', 'Dirty'),
        'is_active': 1 if request.form.get('is_active') else 0,
    }
    result = api_put(f'/api/room-detail/{pr_id}', payload)
    flash('Cập nhật phòng thành công!' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.physical_room_edit', pr_id=pr_id))


@management_bp.route('/manager/physical-room-edit/<int:pr_id>/upload', methods=['POST'])
def physical_room_edit_upload(pr_id):
    err = _require_manager()
    if err:
        return err
    print(f"[FRONTEND] physical_room_edit_upload: PR={pr_id}")
    if 'image' not in request.files:
        print("[FRONTEND] Error: No 'image' in request.files")
        return jsonify({'success': False, 'message': 'Chưa chọn file ảnh.'})
    
    file = request.files['image']
    print(f"[FRONTEND] Received file: {file.filename}")

    result = api_upload(f'/api/room-detail/{pr_id}/upload-image',
                        files={'image': (file.filename, file.stream, file.content_type)})
    
    print(f"[FRONTEND] Backend result: {result}")
    return jsonify({
        'success': result.get('success', False),
        'message': result.get('message', 'Upload xong'),
        'image_url': result.get('image_url')
    })


@management_bp.route('/manager/physical-room-edit/<int:pr_id>/delete-image', methods=['POST'])
def physical_room_edit_delete_image(pr_id):
    err = _require_manager()
    if err:
        return err
    image_url = request.form.get('image_url', '').strip()
    result = api_post(f'/api/room-detail/{pr_id}/delete-image', {'image_url': image_url})
    flash('Đã xóa ảnh.' if result.get('success') else result.get('message', 'Xóa thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.physical_room_edit', pr_id=pr_id))


@management_bp.route('/manager/physical-room-edit/<int:pr_id>/set-main', methods=['POST'])
def physical_room_edit_set_main(pr_id):
    err = _require_manager()
    if err:
        return err
    image_url = request.form.get('image_url', '').strip()
    result = api_post(f'/api/room-detail/{pr_id}/set-main-image', {'image_url': image_url})
    flash('Đã đặt làm ảnh đại diện.' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.physical_room_edit', pr_id=pr_id))


# ── Reports ────────────────────────────────────────────────────────────────────

@management_bp.route('/manager/reports')
def reports():
    err = _require_manager()
    if err:
        return err
    summary = api_get('/api/analytics/summary')
    monthly = api_get('/api/analytics/monthly', params={'year': datetime.now().year})
    conversion = api_get('/api/analytics/conversion', params={'days': 30})
    ops = api_get('/api/operations/realtime')
    hotels = api_get('/api/hotels').get('hotels', [])

    # Chuẩn hóa dữ liệu biểu đồ báo cáo: đảm bảo đầy đủ các key period, total_revenue, total_bookings, total_nights
    raw_monthly = monthly.get('monthly_data', [])
    clean_monthly = []
    for m in raw_monthly:
        m_num = m.get('month_num', 0)
        p_name = m.get('period') or m.get('month_name') or f"Tháng {m_num}"
        rev = m.get('total_revenue')
        if rev is None:
            rev = int(m.get('total_bookings', 0) * m.get('avg_adr', 0))
        clean_monthly.append({
            'period': str(p_name),
            'month_name': str(p_name),
            'month_num': m_num,
            'total_bookings': int(m.get('total_bookings', 0)),
            'total_nights': int(m.get('total_nights', 0)),
            'total_revenue': int(rev),
            'avg_adr': float(m.get('avg_adr', 0)),
            'avg_occupancy_rate': float(m.get('avg_occupancy_rate', 0.22)),
            'canceled': int(m.get('canceled', 0)),
        })

    return render_template('manager_reports.html',
                           summary=summary.get('summary', {}),
                           by_hotel=summary.get('by_hotel', []),
                           monthly_data=clean_monthly,
                           conversion=conversion,
                           ops=ops,
                           hotels=hotels)


# ── Admin: Users ───────────────────────────────────────────────────────────────

@management_bp.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    err = _require_manager(('Admin',))
    if err:
        return err
    user_type = request.args.get('type', 'staff').strip()
    data = api_get('/api/users', params={'type': user_type})
    users = data.get('users', [])
    stats = data.get('stats', {})
    roles = ['Admin', 'Manager', 'Receptionist', 'Housekeeper']
    return render_template('admin_users.html', 
                           users=users, 
                           roles=roles,
                           stats=stats,
                           current_type=user_type)


@management_bp.route('/admin/users/<int:user_id>/role', methods=['POST'])
def update_user_role(user_id):
    err = _require_manager(('Admin',))
    if err:
        return err
    result = api_put(f'/api/users/{user_id}/role', {
        'new_role_name': request.form.get('new_role_name', ''),
    })
    flash('Cập nhật vai trò thành công!' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.admin_users'))


@management_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    err = _require_manager(('Admin',))
    if err:
        return err
    result = api_delete(f'/api/users/{user_id}')
    flash('Đã xóa tài khoản.' if result.get('success') else result.get('message', 'Thất bại'),
          'success' if result.get('success') else 'error')
    return redirect(url_for('management.admin_users'))


# ── Admin: Dimensions ──────────────────────────────────────────────────────────

@management_bp.route('/admin/dimensions', methods=['GET', 'POST'])
def admin_dimensions():
    err = _require_manager(('Admin',))
    if err:
        return err
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action in ('create_room_type', 'add_room_type'):
            result = api_post('/api/dimensions/room-types', {
                'room_type_code': request.form.get('room_type_code', '').strip().upper(),
                'hotel_id': request.form.get('hotel_id', 1, type=int),
                'max_adults': request.form.get('max_adults', 2, type=int),
                'max_children': request.form.get('max_children', 1, type=int),
                'base_price': request.form.get('base_price', 1200000.0, type=float),
            })
            flash('Đã tạo loại phòng thành công.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'update_room_type':
            rt_id = request.form.get('room_type_id', type=int)
            result = api_put(f'/api/dimensions/room-types/{rt_id}', {
                'room_type_code': request.form.get('room_type_code', '').strip().upper(),
                'hotel_id': request.form.get('hotel_id', 1, type=int),
                'max_adults': request.form.get('max_adults', 2, type=int),
                'max_children': request.form.get('max_children', 1, type=int),
                'base_price': request.form.get('base_price', 1200000.0, type=float),
                'is_active': 1,
                'allow_child_sharing': 1, 'extra_bed_capacity': 0,
                'extra_adult_fee': 0.0, 'child_breakfast_fee': 0.0,
            })
            flash('Đã cập nhật loại phòng.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        elif action == 'delete_room_type':
            rt_id = request.form.get('room_type_id', type=int)
            result = api_delete(f'/api/dimensions/room-types/{rt_id}')
            flash('Đã xóa.' if result.get('success') else result.get('message', 'Thất bại'),
                  'success' if result.get('success') else 'error')
        return redirect(url_for('management.admin_dimensions'))
    hotels = api_get('/api/dimensions/hotels').get('hotels', [])
    room_types = api_get('/api/dimensions/room-types').get('room_types', [])
    total_hotels = len(hotels)
    total_room_types = len(room_types)
    total_rooms = sum(h.get('physical_rooms_count', 0) for h in hotels)
    total_active_types = sum(1 for rt in room_types if rt.get('is_active'))
    return render_template('admin_dimensions.html', 
                           hotels=hotels, 
                           room_types=room_types,
                           room_type_name_map=ROOM_TYPE_NAME_MAP,
                           room_specs=ROOM_SPECS,
                           total_hotels=total_hotels,
                           total_room_types=total_room_types,
                           total_rooms=total_rooms,
                           total_active_types=total_active_types)
