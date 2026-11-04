# -*- coding: utf-8 -*-
"""
Check-in Service - Hiện thực hóa quy trình Lễ tân Gán phòng động (ganPhong) & Check-in.
Khớp 100% với Sequence Diagram 02_SD_NhanPhong_CheckIn_GanPhong và Class Diagram UML 2.x.
"""

from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import sqlite3

from database import get_db_connection


def get_assignable_clean_rooms(booking_id: int) -> Tuple[bool, List[Dict[str, Any]], str]:
    """
    Trả về danh sách các phòng vật lý khả dụng để gán cho đơn đặt phòng:
    - Thuộc đúng loại phòng (RoomType) khách đã đặt
    - Đang có trạng thái buồng phòng là Sạch ('Clean')
    - Chưa bị bất kỳ đơn đặt phòng nào khác chiếm trong các đêm lưu trú tương ứng
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Lấy thông tin đơn đặt phòng
        cursor.execute("""
            SELECT booking_id, room_type_id, arrival_date, departure_date, booking_status
            FROM Booking_Master
            WHERE booking_id = ?
        """, (booking_id,))
        bm = cursor.fetchone()
        if not bm:
            return False, [], f"Không tìm thấy đơn đặt phòng #{booking_id}."

        room_type_id = bm['room_type_id']
        arrival_date = bm['arrival_date']
        departure_date = bm['departure_date']

        # 2. Lấy danh sách các đêm của booking này
        cursor.execute("""
            SELECT night_date FROM Booking_Nights
            WHERE booking_id = ?
            ORDER BY night_date
        """, (booking_id,))
        nights = [r['night_date'] for r in cursor.fetchall()]
        if not nights:
            # Fallback nếu chưa sinh Booking_Nights: lấy từ arrival đến departure
            nights = [arrival_date]

        # 3. Tìm các phòng vật lý thuộc loại phòng và có trạng thái 'Clean'
        cursor.execute("""
            SELECT physical_room_id, room_name, housekeeping_status
            FROM Physical_Room
            WHERE room_type_id = ? AND is_active = 1 AND housekeeping_status = 'Clean'
            ORDER BY room_name
        """, (room_type_id,))
        candidate_rooms = cursor.fetchall()

        if not candidate_rooms:
            return True, [], "Hiện không có phòng vật lý nào thuộc loại phòng này đang ở trạng thái Sạch (Clean)."

        assignable_rooms = []
        for cr in candidate_rooms:
            pr_id = cr['physical_room_id']

            # Kiểm tra xem phòng này có bị booking khác chiếm trong bất kỳ đêm nào không
            placeholders = ','.join(['?'] * len(nights))
            query = f"""
                SELECT COUNT(*) FROM Booking_Nights bn
                JOIN Booking_Master bm ON bn.booking_id = bm.booking_id
                WHERE bn.physical_room_id = ?
                  AND bn.booking_id != ?
                  AND bm.booking_status NOT IN ('Canceled', 'No-Show', 'Checked-Out', 'Checked-out')
                  AND bn.night_date IN ({placeholders})
            """
            params = [pr_id, booking_id] + nights
            cursor.execute(query, params)
            conflict_count = cursor.fetchone()[0]

            if conflict_count == 0:
                assignable_rooms.append({
                    'physical_room_id': pr_id,
                    'room_name': cr['room_name'],
                    'housekeeping_status': cr['housekeeping_status']
                })

        return True, assignable_rooms, "Thành công"
    except Exception as e:
        return False, [], f"Lỗi truy vấn phòng sạch khả dụng: {str(e)}"
    finally:
        conn.close()


def assign_room_and_checkin(
    booking_id: int,
    physical_room_id: int,
    staff_user_id: Optional[int] = 1
) -> Tuple[bool, Dict[str, Any], str]:
    """
    Hiện thực hóa hàm nghiệp vụ ganPhong(room: PhysicalRoom):
    1. Gán physical_room_id vào tất cả các Booking_Nights của đơn
    2. Cập nhật Booking_Master.physical_room_id và chuyển trạng thái sang 'Checked-In'
    3. Chuyển trạng thái Physical_Room sang 'Occupied'
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Kiểm tra đơn đặt phòng
        cursor.execute("SELECT * FROM Booking_Master WHERE booking_id = ?", (booking_id,))
        bm = cursor.fetchone()
        if not bm:
            return False, {}, f"Không tìm thấy đơn đặt phòng #{booking_id}."

        if bm['booking_status'] in ('Canceled', 'No-Show'):
            return False, {}, f"Đơn đặt phòng #{booking_id} đang ở trạng thái '{bm['booking_status']}', không thể Check-in."

        # 2. Kiểm tra phòng vật lý
        cursor.execute("SELECT * FROM Physical_Room WHERE physical_room_id = ?", (physical_room_id,))
        pr = cursor.fetchone()
        if not pr:
            return False, {}, f"Không tìm thấy phòng vật lý #{physical_room_id}."

        # 3. Gán phòng vào tất cả các đêm của booking
        cursor.execute("""
            UPDATE Booking_Nights
            SET physical_room_id = ?
            WHERE booking_id = ?
        """, (physical_room_id, booking_id))

        # 4. Cập nhật Booking_Master
        cursor.execute("""
            UPDATE Booking_Master
            SET physical_room_id = ?, booking_status = 'Checked-In'
            WHERE booking_id = ?
        """, (physical_room_id, booking_id))

        # 5. Cập nhật trạng thái phòng vật lý sang Occupied
        cursor.execute("""
            UPDATE Physical_Room
            SET housekeeping_status = 'Occupied'
            WHERE physical_room_id = ?
        """, (physical_room_id,))

        conn.commit()

        return True, {
            'booking_id': booking_id,
            'physical_room_id': physical_room_id,
            'room_name': pr['room_name'],
            'booking_status': 'Checked-In',
            'housekeeping_status': 'Occupied'
        }, f"Đã gán thành công phòng {pr['room_name']} và hoàn tất thủ tục Check-in cho đơn #{booking_id}."

    except Exception as e:
        conn.rollback()
        return False, {}, f"Lỗi hệ thống khi gán phòng và Check-in: {str(e)}"
    finally:
        conn.close()
