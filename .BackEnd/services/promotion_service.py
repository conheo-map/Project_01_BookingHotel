"""
Promotion Service - Kiểm tra và áp dụng mã khuyến mãi với cập nhật nguyên tử (Atomic Update).
Toàn bộ số tiền giảm giá và thanh toán đều là INTEGER VND.
Kiến trúc: Clean Service Layer
"""

from typing import Tuple, Optional, Dict, Any, Union
from datetime import datetime
from database import get_db_connection
from services.exceptions import PromotionInvalidError


def validate_and_apply_promo_internal(
    cursor,
    code: str,
    user_tier: str = 'Newbie',
    total_amount: int = 0,
    checkin_date_str: Optional[str] = None,
    atomic_increment: bool = True
) -> Tuple[bool, int, int, str]:
    """
    Thực thi kiểm tra và áp dụng voucher:
    - Kiểm tra tồn tại, kích hoạt, ngày bắt đầu / kết thúc
    - Kiểm tra số lượt sử dụng tối đa
    - Kiểm tra hạng thành viên
    - Thực hiện cập nhật nguyên tử (Atomic UPDATE) để bảo vệ Race Condition
    """
    if not code:
        return True, 0, total_amount, "Không áp dụng voucher."

    clean_code = code.strip().upper()
    target_date = checkin_date_str or datetime.now().strftime('%Y-%m-%d')

    cursor.execute("""
        SELECT promotion_id, code, discount_percent, discount_type, max_uses, current_uses,
               membership_tier_required, start_date, end_date, active
        FROM Promotions
        WHERE UPPER(code) = ? AND active = 1
    """, (clean_code,))
    promo = cursor.fetchone()

    if not promo:
        return False, 0, total_amount, f"Mã khuyến mãi '{clean_code}' không tồn tại hoặc đã bị vô hiệu hóa."

    # 1. Kiểm tra ngày hiệu lực
    if promo['start_date'] and promo['start_date'] > target_date:
        return False, 0, total_amount, f"Mã khuyến mãi '{clean_code}' chỉ có hiệu lực từ ngày {promo['start_date']}."
    if promo['end_date'] and promo['end_date'] < target_date:
        return False, 0, total_amount, f"Mã khuyến mãi '{clean_code}' đã hết hạn sử dụng (hạn chót: {promo['end_date']})."

    # 2. Kiểm tra giới hạn lượt dùng
    max_uses = int(promo['max_uses'] or 0)
    current_uses = int(promo['current_uses'] or 0)
    if max_uses > 0 and current_uses >= max_uses:
        return False, 0, total_amount, f"Mã khuyến mãi '{clean_code}' đã hết lượt sử dụng ({current_uses}/{max_uses})."

    # 3. Kiểm tra hạng thành viên
    tier_rank = {'Newbie': 0, 'Silver': 1, 'Gold': 2}
    user_rank_val = tier_rank.get(user_tier or 'Newbie', 0)
    req_tier = promo['membership_tier_required'] or 'Newbie'
    req_rank_val = tier_rank.get(req_tier, 0)

    if user_rank_val < req_rank_val:
        return False, 0, total_amount, f"Mã khuyến mãi này chỉ dành riêng cho hội viên hạng {req_tier} trở lên (Hạng hiện tại: {user_tier})."

    # 4. Tính số tiền chiết khấu (INTEGER VND)
    discount_val = float(promo['discount_percent'] or 0)
    if promo['discount_type'] == 'fixed':
        discount_amount = min(int(round(discount_val)), total_amount)
    else:  # percent
        discount_amount = int(round(total_amount * (discount_val / 100.0)))
        discount_amount = min(discount_amount, total_amount)

    final_amount = max(0, total_amount - discount_amount)

    # 5. Cập nhật lượt sử dụng nguyên tử (Atomic Update)
    if atomic_increment:
        cursor.execute("""
            UPDATE Promotions
            SET current_uses = COALESCE(current_uses, 0) + 1
            WHERE UPPER(code) = ? AND active = 1 AND (max_uses = 0 OR current_uses < max_uses)
        """, (clean_code,))
        if cursor.rowcount == 0:
            return False, 0, total_amount, f"Mã khuyến mãi '{clean_code}' vừa hết lượt sử dụng trong thời gian thực."

    return True, discount_amount, final_amount, "Áp dụng mã khuyến mãi thành công."


def validate_and_apply_promo(*args, **kwargs) -> Tuple[bool, int, int, str]:
    """
    Hỗ trợ 2 phong cách gọi:
    1. Kiểu Service độc lập: validate_and_apply_promo(code, customer_tier='Newbie', current_total_amount=0, ...)
    2. Kiểu Cursor nội bộ: validate_and_apply_promo(cursor, code, user_tier='Newbie', total_amount=0, ...)
    """
    raise_on_error = kwargs.get('raise_on_error', False)

    if len(args) > 0 and hasattr(args[0], 'execute'):
        cursor = args[0]
        code = args[1] if len(args) > 1 else kwargs.get('code', '')
        user_tier = args[2] if len(args) > 2 else kwargs.get('user_tier', 'Newbie')
        total_amount = args[3] if len(args) > 3 else kwargs.get('total_amount', 0)
        checkin_date_str = args[4] if len(args) > 4 else kwargs.get('checkin_date_str')
        atomic_increment = args[5] if len(args) > 5 else kwargs.get('atomic_increment', True)

        valid, disc, final_amt, msg = validate_and_apply_promo_internal(
            cursor, code, user_tier, total_amount, checkin_date_str, atomic_increment
        )
        if not valid and raise_on_error:
            raise PromotionInvalidError(msg)
        return valid, disc, final_amt, msg
    else:
        code = args[0] if len(args) > 0 else kwargs.get('code', '')
        customer_tier = args[1] if len(args) > 1 else kwargs.get('customer_tier', kwargs.get('user_tier', 'Newbie'))
        current_total_amount = args[2] if len(args) > 2 else kwargs.get('current_total_amount', kwargs.get('total_amount', 0))
        checkin_date_str = kwargs.get('checkin_date_str')
        atomic_increment = kwargs.get('atomic_increment', True)

        conn = kwargs.get('conn')
        owns_conn = False
        if conn is None:
            conn = get_db_connection()
            owns_conn = True

        try:
            cursor = conn.cursor()
            valid, disc, final_amt, msg = validate_and_apply_promo_internal(
                cursor, code, customer_tier, current_total_amount, checkin_date_str, atomic_increment
            )
            if owns_conn:
                if valid and atomic_increment:
                    conn.commit()
                else:
                    conn.rollback()

            if not valid and raise_on_error:
                raise PromotionInvalidError(msg)
            return valid, disc, final_amt, msg
        finally:
            if owns_conn:
                conn.close()


def apply_promo_atomic(code: str, customer_tier: str = 'Newbie', current_total_amount: int = 0) -> Tuple[int, int]:
    """
    Helper chuẩn Clean Architecture: Trả về (discount_amount, final_amount).
    Ném lỗi PromotionInvalidError nếu voucher không hợp lệ.
    """
    valid, disc, final_amt, msg = validate_and_apply_promo(
        code, customer_tier=customer_tier, current_total_amount=current_total_amount, raise_on_error=True
    )
    return disc, final_amt
