"""
Pricing Service - Xử lý tính toán giá phòng, phụ phí người lớn/trẻ em, và giá linh hoạt theo ngày.
Quy ước: Toàn bộ giá trị tiền tệ được chuẩn hóa dạng INTEGER tính bằng VND.
Kiến trúc: Clean Service Layer
"""

from typing import List, Dict, Any, Tuple, Optional
from database import get_db_connection


def get_room_policy(cursor, room_type_id: int) -> Optional[Dict[str, Any]]:
    """Lấy quy tắc sức chứa và phụ thu của loại phòng."""
    cursor.execute("""
        SELECT
            room_type_id,
            room_type_code,
            max_adults,
            max_children,
            COALESCE(allow_child_sharing, 1) AS allow_child_sharing,
            COALESCE(extra_bed_capacity, 0) AS extra_bed_capacity,
            COALESCE(extra_adult_fee, 0) AS extra_adult_fee,
            COALESCE(child_breakfast_fee, 0) AS child_breakfast_fee,
            base_price
        FROM Dim_RoomType
        WHERE room_type_id = ?
    """, (room_type_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def evaluate_occupancy_policy(
    room_type_id: int,
    adults: int = 1,
    children: int = 0,
    extra_beds: int = 0,
    conn=None
) -> Dict[str, Any]:
    """
    Đánh giá sức chứa phòng và tính phụ thu mỗi đêm:
    - allowed: Có hợp lệ theo chính sách loại phòng hay không
    - extra_adults: Số người lớn phát sinh cần giường phụ (extra bed)
    - shared_children: Số trẻ em vượt định mức chia sẻ giường
    - surcharge_per_night: Phụ phí phát sinh mỗi đêm (VND nguyên)
    """
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        cursor = conn.cursor()
        policy = get_room_policy(cursor, room_type_id)
        if not policy:
            return {'allowed': False, 'reason': f'Không tìm thấy loại phòng ID {room_type_id}'}

        max_adults = int(policy['max_adults'] or 2)
        max_children = int(policy['max_children'] or 1)
        allow_child_sharing = int(policy['allow_child_sharing'] or 0) == 1
        extra_bed_capacity = int(policy['extra_bed_capacity'] or 0)
        extra_adult_fee = int(round(float(policy['extra_adult_fee'] or 0)))
        child_breakfast_fee = int(round(float(policy['child_breakfast_fee'] or 0)))

        adults = int(adults or 1)
        children = int(children or 0)

        # 1. Kiểm tra người lớn
        extra_adults = max(0, adults - max_adults)
        if extra_adults > extra_bed_capacity:
            return {
                'allowed': False,
                'reason': f'Vượt quá sức chứa tối đa ({max_adults} người lớn + {extra_bed_capacity} giường phụ).'
            }

        # 2. Kiểm tra trẻ em
        shared_children = 0
        if children > max_children:
            if not allow_child_sharing:
                return {'allowed': False, 'reason': 'Loại phòng này không hỗ trợ trẻ em ở ghép.'}
            shared_children = children - max_children
            if shared_children > 2:
                return {'allowed': False, 'reason': 'Số lượng trẻ em vượt quá giới hạn chính sách cho phép.'}

        surcharge_per_night = (extra_adults * extra_adult_fee) + (shared_children * child_breakfast_fee)
        return {
            'allowed': True,
            'extra_adults': extra_adults,
            'shared_children': shared_children,
            'surcharge_per_night': surcharge_per_night,
            'extra_adult_fee': extra_adult_fee,
            'child_breakfast_fee': child_breakfast_fee
        }
    finally:
        if owns_conn:
            conn.close()


def evaluate_room_occupancy(cursor, room_type_id: int, adults: int, children: int) -> Dict[str, Any]:
    """Tương thích ngược: evaluate_room_occupancy nhận cursor."""
    policy = get_room_policy(cursor, room_type_id)
    if not policy:
        return {'allowed': False, 'reason': 'Không tìm thấy thông tin loại phòng'}

    max_adults = int(policy['max_adults'] or 2)
    max_children = int(policy['max_children'] or 1)
    allow_child_sharing = int(policy['allow_child_sharing'] or 0) == 1
    extra_bed_capacity = int(policy['extra_bed_capacity'] or 0)
    extra_adult_fee = int(round(float(policy['extra_adult_fee'] or 0)))
    child_breakfast_fee = int(round(float(policy['child_breakfast_fee'] or 0)))

    adults = int(adults or 1)
    children = int(children or 0)

    extra_adults = max(0, adults - max_adults)
    if extra_adults > extra_bed_capacity:
        return {
            'allowed': False,
            'reason': f'Vượt quá sức chứa tối đa ({max_adults} người lớn + {extra_bed_capacity} giường phụ)'
        }

    shared_children = 0
    if children > max_children:
        if not allow_child_sharing:
            return {'allowed': False, 'reason': 'Loại phòng này không hỗ trợ trẻ em ở ghép'}
        shared_children = children - max_children
        if shared_children > 2:
            return {'allowed': False, 'reason': 'Số lượng trẻ em vượt quá giới hạn chính sách cho phép'}

    surcharge_per_night = (extra_adults * extra_adult_fee) + (shared_children * child_breakfast_fee)
    return {
        'allowed': True,
        'extra_adults': extra_adults,
        'shared_children': shared_children,
        'surcharge_per_night': surcharge_per_night
    }


def get_effective_daily_price(
    cursor,
    room_type_id: int,
    room_type_code: str,
    target_date_str: str,
    physical_room_id: Optional[int] = None
) -> int:
    """
    Lấy giá phòng hiệu lực cho 1 ngày:
    1. Ưu tiên tra cứu Room_Rates (giá ngày lễ, cuối tuần, ghi đè theo phòng vật lý hoặc loại phòng).
    2. Fallback lấy giá cơ bản từ Dim_RoomType.base_price.
    Trả về số nguyên (INTEGER VND).
    """
    # 1. Tra cứu giá ưu tiên theo phòng cụ thể
    if physical_room_id:
        cursor.execute("""
            SELECT base_price FROM Room_Rates
            WHERE physical_room_id = ? AND valid_date = ?
            LIMIT 1
        """, (physical_room_id, target_date_str))
        p_row = cursor.fetchone()
        if p_row and p_row['base_price'] is not None:
            return int(round(float(p_row['base_price'])))

    # 2. Tra cứu giá theo loại phòng
    if room_type_code:
        cursor.execute("""
            SELECT base_price FROM Room_Rates
            WHERE room_type_code = ? AND valid_date = ? AND physical_room_id IS NULL
            LIMIT 1
        """, (room_type_code, target_date_str))
        override_row = cursor.fetchone()
        if override_row and override_row['base_price'] is not None:
            return int(round(float(override_row['base_price'])))

    # 3. Fallback lấy giá gốc loại phòng
    cursor.execute("SELECT base_price FROM Dim_RoomType WHERE room_type_id = ?", (room_type_id,))
    base_row = cursor.fetchone()
    if base_row and base_row['base_price'] is not None:
        return int(round(float(base_row['base_price'])))

    return 1000000  # Default fallback 1.000.000 VND


def calculate_nightly_rates(
    room_type_id: int,
    physical_room_id: Optional[int],
    nights_list: List[str],
    conn=None
) -> List[Dict[str, Any]]:
    """
    Tra cứu bảng giá từng đêm cho phòng/loại phòng:
    Trả về danh sách: [{'date': str, 'base_price': int, 'is_holiday': int}]
    """
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT room_type_code, base_price FROM Dim_RoomType WHERE room_type_id = ?", (room_type_id,))
        rt = cursor.fetchone()
        room_type_code = rt['room_type_code'] if rt else ''
        standard_base_price = int(round(float(rt['base_price'] or 1000000))) if rt else 1000000

        result = []
        for night in nights_list:
            daily_price = get_effective_daily_price(cursor, room_type_id, room_type_code, night, physical_room_id)
            cursor.execute("""
                SELECT is_holiday FROM Room_Rates
                WHERE (room_type_code = ? OR physical_room_id = ?) AND valid_date = ?
                LIMIT 1
            """, (room_type_code, physical_room_id, night))
            h_row = cursor.fetchone()
            is_holiday = int(h_row['is_holiday'] or 0) if h_row else 0

            result.append({
                'date': night,
                'base_price': daily_price,
                'is_holiday': is_holiday
            })
        return result
    finally:
        if owns_conn:
            conn.close()


def calculate_total_quote(
    room_type_id: int,
    physical_room_id: Optional[int],
    nights_list: List[str],
    adults: int = 1,
    children: int = 0,
    extra_beds: int = 0,
    conn=None
) -> Dict[str, Any]:
    """
    Tổng hợp giá trọn gói:
    Tiền phòng từng đêm + Phụ thu khách vượt định mức = Tổng tiền dự toán (total_amount VND).
    """
    owns_conn = False
    if conn is None:
        conn = get_db_connection()
        owns_conn = True

    try:
        occupancy = evaluate_occupancy_policy(room_type_id, adults, children, extra_beds, conn=conn)
        if not occupancy.get('allowed'):
            return {
                'allowed': False,
                'message': occupancy.get('reason'),
                'total_amount': 0
            }

        surcharge_per_night = occupancy.get('surcharge_per_night', 0)
        nightly_rates = calculate_nightly_rates(room_type_id, physical_room_id, nights_list, conn=conn)

        nights_breakdown = []
        base_room_total = 0
        total_surcharges = 0

        for r in nightly_rates:
            night_total = r['base_price'] + surcharge_per_night
            base_room_total += r['base_price']
            total_surcharges += surcharge_per_night
            nights_breakdown.append({
                'date': r['date'],
                'base_price': r['base_price'],
                'surcharge': surcharge_per_night,
                'is_holiday': r['is_holiday'],
                'total': night_total
            })

        total_amount = base_room_total + total_surcharges

        return {
            'allowed': True,
            'number_of_nights': len(nights_list),
            'surcharge_per_night': surcharge_per_night,
            'total_surcharges': total_surcharges,
            'base_room_total': base_room_total,
            'total_amount': total_amount,
            'nights_breakdown': nights_breakdown
        }
    finally:
        if owns_conn:
            conn.close()


def calculate_booking_price(
    cursor,
    room_type_id: int,
    room_type_code: str,
    list_of_nights: List[str],
    adults: int = 1,
    children: int = 0
) -> Dict[str, Any]:
    """Tương thích ngược: calculate_booking_price nhận cursor."""
    occupancy = evaluate_room_occupancy(cursor, room_type_id, adults, children)
    if not occupancy.get('allowed'):
        return {'allowed': False, 'message': occupancy.get('reason')}

    surcharge_per_night = occupancy.get('surcharge_per_night', 0)
    nights_breakdown = []
    base_room_total = 0

    for night_str in list_of_nights:
        daily_price = get_effective_daily_price(cursor, room_type_id, room_type_code, night_str)
        night_total = daily_price + surcharge_per_night
        base_room_total += night_total
        nights_breakdown.append({
            'date': night_str,
            'base_price': daily_price,
            'surcharge': surcharge_per_night,
            'total': night_total
        })

    return {
        'allowed': True,
        'number_of_nights': len(list_of_nights),
        'surcharge_per_night': surcharge_per_night,
        'base_room_total': base_room_total,
        'nights_breakdown': nights_breakdown
    }
