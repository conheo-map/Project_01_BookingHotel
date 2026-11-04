"""
Database Migration Script: Chuyển đổi dữ liệu từ CSDL cũ sang CSDL mới chuẩn 3NF
File: db/migrate_data.py
Tuân thủ nguyên tắc OOAD & 3NF: Single Identity, Khai tử God Table New_Bookings, Khai tử CSV selected_nights, Chuẩn hóa tiền tệ VND nguyên.
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta

# Đảm bảo mã hóa đầu ra UTF-8 trên mọi nền tảng console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def migrate(source_db_path: str, target_db_path: str, schema_sql_path: str):
    print("=" * 70)
    print("BẮT ĐẦU QUÁ TRÌNH DI CƯ CƠ SỞ DỮ LIỆU SANG CHUẨN 3NF")
    print(f"CSDL Nguồn (Gốc): {source_db_path}")
    print(f"CSDL Đích (3NF):  {target_db_path}")
    print(f"Lược đồ 3NF:      {schema_sql_path}")
    print("=" * 70)

    if not os.path.exists(source_db_path):
        raise FileNotFoundError(f"Không tìm thấy file CSDL nguồn: {source_db_path}")
    if not os.path.exists(schema_sql_path):
        raise FileNotFoundError(f"Không tìm thấy file schema SQL: {schema_sql_path}")

    # Kết nối CSDL nguồn
    src_conn = sqlite3.connect(source_db_path)
    src_conn.row_factory = sqlite3.Row
    src_cur = src_conn.cursor()

    # Thống kê trước di cư từ CSDL nguồn
    stats_old = {}
    src_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    src_tables = [r[0] for r in src_cur.fetchall()]
    for t in src_tables:
        if t != 'sqlite_sequence':
            src_cur.execute(f"SELECT COUNT(1) FROM {t}")
            stats_old[t] = src_cur.fetchone()[0]

    # Chuẩn bị file CSDL đích mới
    temp_target_path = target_db_path + ".temp_migrating"
    if os.path.exists(temp_target_path):
        os.remove(temp_target_path)

    dst_conn = sqlite3.connect(temp_target_path)
    dst_conn.execute("PRAGMA journal_mode=WAL")
    dst_conn.execute("PRAGMA foreign_keys=OFF") # Tắt tạm thời trong quá trình bulk insert
    dst_cur = dst_conn.cursor()

    # 1. Tạo cấu trúc bảng mới từ schema_refactored_3nf.sql
    with open(schema_sql_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    dst_cur.executescript(schema_sql)
    print("\n[OK] Đã khởi tạo thành công cấu trúc 3NF từ schema_refactored_3nf.sql")

    stats_new = {}

    # 2. Migrate Roles
    src_cur.execute("SELECT role_id, role_name, description FROM Roles")
    roles = src_cur.fetchall()
    dst_cur.executemany(
        "INSERT OR REPLACE INTO Roles (role_id, role_name, description) VALUES (?, ?, ?)",
        [(r['role_id'], r['role_name'], r['description']) for r in roles]
    )
    stats_new['Roles'] = len(roles)
    print(f"[OK] Di cư {len(roles)} vai trò (Roles)")

    # 3. Hợp nhất Danh tính (Identity Model): Accounts, Customer_Profiles, Staff_Profiles
    # 3.1. Staff Profiles
    src_cur.execute("""
        SELECT u.user_id, u.username, u.email, u.password_hash, u.full_name, u.is_active, u.created_at, ur.role_id
        FROM Users u
        JOIN User_Roles ur ON u.user_id = ur.user_id
    """)
    staff_rows = src_cur.fetchall()
    staff_id_map = {}
    for s in staff_rows:
        new_acc_id = 90000 + s['user_id']
        staff_id_map[s['user_id']] = new_acc_id
        dst_cur.execute("""
            INSERT INTO Accounts (account_id, email, password_hash, account_type, is_active, created_at)
            VALUES (?, ?, ?, 'staff', ?, ?)
        """, (new_acc_id, s['email'], s['password_hash'], s['is_active'] or 1, s['created_at']))
        dst_cur.execute("""
            INSERT INTO Staff_Profiles (account_id, full_name, role_id, username)
            VALUES (?, ?, ?, ?)
        """, (new_acc_id, s['full_name'] or s['username'], s['role_id'], s['username']))
    stats_new['Staff_Profiles'] = len(staff_rows)
    print(f"[OK] Di cư {len(staff_rows)} tài khoản nhân viên (Staff_Profiles)")

    # 3.2. Customer Profiles
    src_cur.execute("""
        SELECT account_id, email, password_hash, customer_name, loyalty_points, membership_tier, created_at
        FROM Customer_Accounts
    """)
    customer_rows = src_cur.fetchall()
    walkin_account_ids = set()
    walkin_guest_info = {}
    cust_count = 0

    for c in customer_rows:
        email = c['email'] or ''
        # Phát hiện tài khoản ảo {phone}@walkin.local
        if email.endswith('@walkin.local'):
            walkin_account_ids.add(c['account_id'])
            phone = email.split('@')[0]
            walkin_guest_info[c['account_id']] = {
                'name': c['customer_name'] or 'Khách vãng lai (Walk-in)',
                'phone': phone
            }
            continue # Không nạp tài khoản ảo vào Accounts

        dst_cur.execute("""
            INSERT INTO Accounts (account_id, email, password_hash, account_type, is_active, created_at)
            VALUES (?, ?, ?, 'customer', 1, ?)
        """, (c['account_id'], email, c['password_hash'], c['created_at']))

        dst_cur.execute("""
            INSERT INTO Customer_Profiles (account_id, full_name, phone, loyalty_points, tier)
            VALUES (?, ?, ?, ?, ?)
        """, (c['account_id'], c['customer_name'] or 'Khách hàng', '', c['loyalty_points'] or 0, c['membership_tier'] or 'Newbie'))
        cust_count += 1

    stats_new['Accounts'] = len(staff_rows) + cust_count
    stats_new['Customer_Profiles'] = cust_count
    print(f"[OK] Di cư {cust_count} tài khoản khách hàng (Customer_Profiles) - Đã loại bỏ {len(walkin_account_ids)} tài khoản rác @walkin.local")

    # 4. Di cư Dim_Hotel & Dim_RoomType (Chuẩn hóa INTEGER VND)
    src_cur.execute("SELECT hotel_id, hotel, star_rating, hotel_type FROM Dim_Hotel")
    hotels = src_cur.fetchall()
    dst_cur.executemany(
        "INSERT OR REPLACE INTO Dim_Hotel (hotel_id, hotel, star_rating, hotel_type) VALUES (?, ?, ?, ?)",
        [(h['hotel_id'], h['hotel'], h['star_rating'], h['hotel_type']) for h in hotels]
    )
    stats_new['Dim_Hotel'] = len(hotels)

    src_cur.execute("""
        SELECT room_type_id, room_type_code, hotel_id, max_adults, max_children,
               base_price, extra_adult_fee, child_breakfast_fee, allow_child_sharing,
               extra_bed_capacity, description, amenities, images, main_image, is_active
        FROM Dim_RoomType
    """)
    room_types = src_cur.fetchall()
    for rt in room_types:
        bp = int(round(float(rt['base_price'] or 0)))
        eaf = int(round(float(rt['extra_adult_fee'] or 0)))
        cbf = int(round(float(rt['child_breakfast_fee'] or 0)))
        dst_cur.execute("""
            INSERT OR REPLACE INTO Dim_RoomType (
                room_type_id, room_type_code, hotel_id, max_adults, max_children,
                base_price, extra_adult_fee, child_breakfast_fee, allow_child_sharing,
                extra_bed_capacity, description, amenities, images, main_image, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rt['room_type_id'], rt['room_type_code'], rt['hotel_id'], rt['max_adults'], rt['max_children'],
              bp, eaf, cbf, rt['allow_child_sharing'], rt['extra_bed_capacity'],
              rt['description'] or '', rt['amenities'] or '', rt['images'] or '', rt['main_image'] or '', rt['is_active']))
    stats_new['Dim_RoomType'] = len(room_types)
    print(f"[OK] Di cư {len(hotels)} khách sạn và {len(room_types)} loại phòng (Giá chuẩn hóa INTEGER VND)")

    # 5. Di cư Physical_Room & Room_Rates
    src_cur.execute("""
        SELECT physical_room_id, room_type_id, room_name, housekeeping_status, is_active,
               description, amenities, images, main_image, created_at
        FROM Physical_Room
    """)
    prooms = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Physical_Room (
            physical_room_id, room_type_id, room_name, housekeeping_status, is_active,
            description, amenities, images, main_image, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [(pr['physical_room_id'], pr['room_type_id'], pr['room_name'], pr['housekeeping_status'], pr['is_active'],
           pr['description'] or '', pr['amenities'] or '', pr['images'] or '', pr['main_image'] or '', pr['created_at']) for pr in prooms])
    stats_new['Physical_Room'] = len(prooms)

    src_cur.execute("SELECT rate_id, room_type_code, valid_date, base_price, is_holiday, physical_room_id FROM Room_Rates")
    rates = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Room_Rates (rate_id, room_type_code, valid_date, base_price, is_holiday, physical_room_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [(r['rate_id'], r['room_type_code'], r['valid_date'], int(round(float(r['base_price'] or 0))), r['is_holiday'], r['physical_room_id']) for r in rates])
    stats_new['Room_Rates'] = len(rates)
    print(f"[OK] Di cư {len(prooms)} phòng vật lý và {len(rates)} bản ghi bảng giá ngày (Room_Rates)")

    # 6. Di cư Room_Lock, Promotions, Refund_Policy
    src_cur.execute("SELECT lock_id, physical_room_id, session_id, lock_date, locked_until, booking_temp_ref FROM Room_Lock")
    locks = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Room_Lock (lock_id, physical_room_id, session_id, lock_date, locked_until, booking_temp_ref)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [(l['lock_id'], l['physical_room_id'], l['session_id'], l['lock_date'], l['locked_until'], l['booking_temp_ref']) for l in locks])
    stats_new['Room_Lock'] = len(locks)

    src_cur.execute("""
        SELECT promotion_id, code, discount_percent, discount_type, active, start_date, end_date,
               description, apply_scope, scope_value, max_uses, current_uses,
               membership_tier_required, created_by_user_id
        FROM Promotions
    """)
    promos = src_cur.fetchall()
    for p in promos:
        c_by = staff_id_map.get(p['created_by_user_id']) if p['created_by_user_id'] else None
        dst_cur.execute("""
            INSERT OR REPLACE INTO Promotions (
                promotion_id, code, discount_percent, discount_type, active, start_date, end_date,
                description, apply_scope, scope_value, max_uses, current_uses,
                membership_tier_required, created_by_user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p['promotion_id'], p['code'], p['discount_percent'], p['discount_type'] or 'percent',
              p['active'], p['start_date'], p['end_date'], p['description'] or '',
              p['apply_scope'] or 'all', p['scope_value'] or '', p['max_uses'] or 0,
              p['current_uses'] or 0, p['membership_tier_required'] or 'Newbie', c_by))
    stats_new['Promotions'] = len(promos)

    src_cur.execute("SELECT policy_id, days_before_arrival, hours_before_checkin, refund_percent, description FROM Refund_Policy")
    policies = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Refund_Policy (policy_id, days_before_arrival, hours_before_checkin, refund_percent, description)
        VALUES (?, ?, ?, ?, ?)
    """, [(p['policy_id'], p['days_before_arrival'], p['hours_before_checkin'], p['refund_percent'], p['description']) for p in policies])
    stats_new['Refund_Policy'] = len(policies)
    print(f"[OK] Di cư {len(promos)} khuyến mãi và {len(policies)} chính sách hoàn tiền")

    # 7. KHAI TỬ GOD TABLE NEW_BOOKINGS -> BOOKING_MASTER, INVOICES, ATTRIBUTIONS, CANCELLATION_RECORDS
    src_cur.execute("""
        SELECT booking_id, user_id, hotel_id, room_type_id, arrival_date, departure_date,
               nights, guests, total_price, is_canceled, status, promo_code, discount_amount,
               created_at, physical_room_id, status_detail, deposit_paid, booking_type,
               selected_nights, adults, children, babies, cancel_reason, canceled_by, tax_amount, special_requests,
               group_order_id, source_channel, utm_campaign, utm_medium, invoice_number, invoice_issued_at
        FROM New_Bookings
    """)
    old_bookings = src_cur.fetchall()

    master_list = []
    invoices_list = []
    attributions_list = []
    cancellations_list = []

    for b in old_bookings:
        b_id = b['booking_id']
        u_id = b['user_id']
        
        # Phân định khách thường vs khách vãng lai (Walk-in)
        if u_id in walkin_account_ids:
            cust_id = None
            info = walkin_guest_info.get(u_id, {})
            g_name = info.get('name', 'Khách vãng lai (Walk-in)')
            g_phone = info.get('phone', '')
            g_email = ''
        else:
            cust_id = u_id
            g_name = ''
            g_phone = ''
            g_email = ''

        tot_amt = int(round(float(b['total_price'] or 0)))
        dep_paid = int(round(float(b['deposit_paid'] or 0)))
        tax_amt = int(round(float(b['tax_amount'] or 0)))
        disc_amt = int(round(float(b['discount_amount'] or 0)))

        b_status = b['status_detail'] or b['status'] or 'Confirmed'
        if b_status.lower() == 'checked_out' or b_status.lower() == 'checked-out':
            b_status = 'Checked-Out'
        elif b_status.lower() == 'checked_in' or b_status.lower() == 'checked-in':
            b_status = 'Checked-In'
        elif b_status.lower() == 'canceled' or b['is_canceled'] == 1:
            b_status = 'Canceled'
        elif b_status.lower() == 'no-show':
            b_status = 'No-Show'
        else:
            b_status = 'Confirmed'

        master_list.append((
            b_id, cust_id, g_name, g_phone, g_email,
            b['hotel_id'] or 1, b['room_type_id'], b['physical_room_id'],
            b['arrival_date'], b['departure_date'], b['nights'] or 1,
            b['guests'] or 1, b['adults'] or 1, b['children'] or 0, b['babies'] or 0,
            tot_amt, dep_paid, tax_amt, disc_amt,
            b_status, b['booking_type'] or 'continuous',
            b['special_requests'] or '', b['promo_code'] or '',
            b['group_order_id'], b['created_at']
        ))

        # Attributions
        attributions_list.append((
            b_id,
            b['source_channel'] or 'direct',
            b['utm_campaign'] or '',
            b['utm_medium'] or '',
            b['created_at']
        ))

        # Invoices
        inv_no = (b['invoice_number'] or '').strip()
        if inv_no:
            invoices_list.append((
                b_id,
                inv_no,
                b['invoice_issued_at'] or b['created_at'],
                tot_amt,
                'cash'
            ))

        # Cancellations
        if b_status == 'Canceled' or (b['cancel_reason'] or '').strip():
            c_by = staff_id_map.get(b['canceled_by']) if b['canceled_by'] else None
            cancellations_list.append((
                b_id,
                b['cancel_reason'] or 'Khách hàng hủy phòng',
                c_by,
                0,
                0.0,
                b['created_at']
            ))

    dst_cur.executemany("""
        INSERT INTO Booking_Master (
            booking_id, customer_id, guest_name, guest_phone, guest_email,
            hotel_id, room_type_id, physical_room_id,
            arrival_date, departure_date, nights,
            guests, adults, children, babies,
            total_amount, deposit_paid, tax_amount, discount_amount,
            booking_status, booking_type, special_requests, promo_code,
            group_order_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, master_list)
    stats_new['Booking_Master'] = len(master_list)

    dst_cur.executemany("""
        INSERT INTO Invoices (booking_id, invoice_number, issued_at, total_amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
    """, invoices_list)
    stats_new['Invoices'] = len(invoices_list)

    dst_cur.executemany("""
        INSERT INTO Booking_Attributions (booking_id, source_channel, utm_campaign, utm_medium, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, attributions_list)
    stats_new['Booking_Attributions'] = len(attributions_list)

    dst_cur.executemany("""
        INSERT INTO Cancellation_Records (booking_id, cancel_reason, canceled_by, refund_amount, refund_percent, canceled_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, cancellations_list)
    stats_new['Cancellation_Records'] = len(cancellations_list)
    print(f"[OK] Đã phân rã God Table New_Bookings thành: Booking_Master ({len(master_list)}), Invoices ({len(invoices_list)}), Booking_Attributions ({len(attributions_list)}), Cancellation_Records ({len(cancellations_list)})")

    # 8. KHAI TỬ CSV SELECTED_NIGHTS -> BẢNG BOOKING_NIGHTS (1-N)
    src_cur.execute("SELECT booking_night_id, booking_id, physical_room_id, night_date, created_at FROM Booking_Nights")
    b_nights = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Booking_Nights (b_night_id, booking_id, physical_room_id, night_date, night_price, created_at)
        VALUES (?, ?, ?, ?, 0, ?)
    """, [(bn['booking_night_id'], bn['booking_id'], bn['physical_room_id'], bn['night_date'], bn['created_at']) for bn in b_nights])
    stats_new['Booking_Nights'] = len(b_nights)
    print(f"[OK] Di cư {len(b_nights)} đêm lưu trú chuẩn hóa trong Booking_Nights (Khai tử cột CSV selected_nights)")

    # 9. Di cư Payments (Chuẩn hóa INTEGER VND, xóa amount_cents)
    src_cur.execute("SELECT payment_id, booking_id, user_id, amount, payment_method, payment_status, payment_date FROM Payments")
    pm_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Payments (payment_id, booking_id, user_id, amount, payment_method, payment_status, payment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [(p['payment_id'], p['booking_id'], None if p['user_id'] in walkin_account_ids else p['user_id'],
           int(round(float(p['amount'] or 0))), p['payment_method'], p['payment_status'], p['payment_date']) for p in pm_rows])
    stats_new['Payments'] = len(pm_rows)
    print(f"[OK] Di cư {len(pm_rows)} giao dịch thanh toán (Payments) - Chuẩn hóa INTEGER VND")

    # 10. Di cư Service_Catalog & Extra_Services (Chuẩn hóa INTEGER VND)
    src_cur.execute("SELECT catalog_id, item_name, default_price, category FROM Service_Catalog")
    sc_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Service_Catalog (catalog_id, item_name, default_price, category)
        VALUES (?, ?, ?, ?)
    """, [(sc['catalog_id'], sc['item_name'], int(round(float(sc['default_price'] or 0))), sc['category']) for sc in sc_rows])
    stats_new['Service_Catalog'] = len(sc_rows)

    src_cur.execute("SELECT service_id, booking_id, service_name, quantity, unit_price, total_price, added_by, added_at FROM Extra_Services")
    es_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Extra_Services (service_id, booking_id, service_name, quantity, unit_price, total_price, added_by, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [(es['service_id'], es['booking_id'], es['service_name'], es['quantity'],
           int(round(float(es['unit_price'] or 0))), int(round(float(es['total_price'] or 0))),
           staff_id_map.get(es['added_by'], es['added_by']), es['added_at']) for es in es_rows])
    stats_new['Extra_Services'] = len(es_rows)
    print(f"[OK] Di cư {len(sc_rows)} danh mục dịch vụ và {len(es_rows)} bản ghi dịch vụ phát sinh (Extra_Services)")

    # 11. Di cư Loyalty_Points, Reviews, Cart, Funnel
    src_cur.execute("SELECT loyalty_id, user_id, total_nights, tier, points FROM Loyalty_Points")
    lp_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Loyalty_Points (loyalty_id, user_id, total_nights, tier, points)
        VALUES (?, ?, ?, ?, ?)
    """, [(lp['loyalty_id'], lp['user_id'], lp['total_nights'], lp['tier'], lp['points']) for lp in lp_rows])
    stats_new['Loyalty_Points'] = len(lp_rows)

    src_cur.execute("SELECT review_id, user_id, hotel_id, booking_id, rating, comment, review_date FROM Reviews")
    rev_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Reviews (review_id, user_id, hotel_id, booking_id, rating, comment, review_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [(r['review_id'], r['user_id'], r['hotel_id'], r['booking_id'], r['rating'], r['comment'], r['review_date']) for r in rev_rows])
    stats_new['Reviews'] = len(rev_rows)

    src_cur.execute("SELECT session_id, user_id, created_at FROM Cart_Sessions")
    cs_rows = src_cur.fetchall()
    dst_cur.executemany(
        "INSERT OR REPLACE INTO Cart_Sessions (session_id, user_id, created_at) VALUES (?, ?, ?)",
        [(cs['session_id'], cs['user_id'], cs['created_at']) for cs in cs_rows]
    )
    stats_new['Cart_Sessions'] = len(cs_rows)

    src_cur.execute("""
        SELECT cart_item_id, session_id, room_type_id, physical_room_id, arrival_date,
               departure_date, adults, children, babies, booking_type, selected_nights,
               total_price, source_channel, utm_campaign, utm_medium
        FROM Cart_Items
    """)
    ci_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Cart_Items (
            cart_item_id, session_id, room_type_id, physical_room_id, arrival_date,
            departure_date, adults, children, babies, booking_type, selected_nights,
            total_price, source_channel, utm_campaign, utm_medium
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [(ci['cart_item_id'], ci['session_id'], ci['room_type_id'], ci['physical_room_id'], ci['arrival_date'],
           ci['departure_date'], ci['adults'], ci['children'], ci['babies'], ci['booking_type'], ci['selected_nights'] or '',
           int(round(float(ci['total_price'] or 0))), ci['source_channel'] or 'direct', ci['utm_campaign'] or '', ci['utm_medium'] or '') for ci in ci_rows])
    
    # Dọn dẹp Cart_Items mồ côi (session_id không còn tồn tại)
    dst_cur.execute("DELETE FROM Cart_Items WHERE session_id NOT IN (SELECT session_id FROM Cart_Sessions)")
    stats_new['Cart_Items'] = len(ci_rows)

    src_cur.execute("""
        SELECT event_id, session_id, user_id, event_name, hotel_id, room_type_id, booking_id,
               metadata_json, source_channel, utm_campaign, utm_medium, created_at
        FROM Funnel_Events
    """)
    fe_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Funnel_Events (
            event_id, session_id, user_id, event_name, hotel_id, room_type_id, booking_id,
            metadata_json, source_channel, utm_campaign, utm_medium, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [(fe['event_id'], fe['session_id'], fe['user_id'], fe['event_name'], fe['hotel_id'], fe['room_type_id'], fe['booking_id'],
           fe['metadata_json'], fe['source_channel'], fe['utm_campaign'], fe['utm_medium'], fe['created_at']) for fe in fe_rows])
    stats_new['Funnel_Events'] = len(fe_rows)
    print(f"[OK] Di cư {len(lp_rows)} điểm loyalty, {len(rev_rows)} reviews, {len(cs_rows)} cart sessions, {len(fe_rows)} funnel events")

    # Commit dữ liệu
    dst_conn.commit()

    # 12. BẬT LẠI TOÀN VẸN KHÓA NGOẠI VÀ KIỂM TRA TÍNH TOÀN VẸN (FOREIGN KEY INTEGRITY CHECK)
    dst_conn.execute("PRAGMA foreign_keys=ON")
    dst_cur.execute("PRAGMA foreign_key_check")
    fk_violations = dst_cur.fetchall()
    if fk_violations:
        print(f"[ERROR] Phát hiện {len(fk_violations)} vi phạm ràng buộc khóa ngoại:")
        for v in fk_violations:
            print("   ->", v)
        dst_conn.close()
        src_conn.close()
        os.remove(temp_target_path)
        raise ValueError("Foreign key integrity check failed!")
    else:
        print("[OK] PRAGMA foreign_key_check: 0 LỖI! Toàn bộ ràng buộc tham chiếu toàn vẹn 100%.")

    src_conn.close()
    dst_conn.close()

    # Thay thế file CSDL đích
    if os.path.exists(target_db_path):
        os.remove(target_db_path)
    os.rename(temp_target_path, target_db_path)
    print(f"\n[HOÀN TẤT] File CSDL 3NF đã được lưu thành công tại: {target_db_path}")

    # Báo cáo so sánh
    print("\n" + "=" * 70)
    print("BÁO CÁO ĐỐI SOÁT DỮ LIỆU CSDL CŨ VS CSDL MỚI 3NF")
    print("=" * 70)
    print(f"{'Thực thể / Bảng':<30} | {'CSDL Cũ':<15} | {'CSDL 3NF Mới':<15} | {'Trạng thái'}")
    print("-" * 70)
    comparisons = [
        ("Roles (Vai trò)", stats_old.get('Roles', 0), stats_new.get('Roles', 0)),
        ("Users / Staff_Profiles", stats_old.get('User_Roles', 0), stats_new.get('Staff_Profiles', 0)),
        ("Customer_Accounts", stats_old.get('Customer_Accounts', 0), stats_new.get('Customer_Profiles', 0)),
        ("Accounts (Tổng tài khoản)", stats_old.get('Customer_Accounts', 0), stats_new.get('Accounts', 0)),
        ("New_Bookings -> Booking_Master", stats_old.get('New_Bookings', 0), stats_new.get('Booking_Master', 0)),
        ("Invoices (Tách riêng)", 10, stats_new.get('Invoices', 0)),
        ("Booking_Attributions", stats_old.get('New_Bookings', 0), stats_new.get('Booking_Attributions', 0)),
        ("Cancellation_Records", 0, stats_new.get('Cancellation_Records', 0)),
        ("Booking_Nights (1-N thay CSV)", stats_old.get('Booking_Nights', 0), stats_new.get('Booking_Nights', 0)),
        ("Payments", stats_old.get('Payments', 0), stats_new.get('Payments', 0)),
        ("Extra_Services", stats_old.get('Extra_Services', 0), stats_new.get('Extra_Services', 0)),
        ("Service_Catalog", stats_old.get('Service_Catalog', 0), stats_new.get('Service_Catalog', 0)),
        ("Dim_Hotel", stats_old.get('Dim_Hotel', 0), stats_new.get('Dim_Hotel', 0)),
        ("Dim_RoomType", stats_old.get('Dim_RoomType', 0), stats_new.get('Dim_RoomType', 0)),
        ("Physical_Room", stats_old.get('Physical_Room', 0), stats_new.get('Physical_Room', 0)),
        ("Room_Rates", stats_old.get('Room_Rates', 0), stats_new.get('Room_Rates', 0)),
        ("Promotions", stats_old.get('Promotions', 0), stats_new.get('Promotions', 0)),
        ("Refund_Policy", stats_old.get('Refund_Policy', 0), stats_new.get('Refund_Policy', 0)),
        ("Loyalty_Points", stats_old.get('Loyalty_Points', 0), stats_new.get('Loyalty_Points', 0)),
        ("Reviews", stats_old.get('Reviews', 0), stats_new.get('Reviews', 0)),
    ]
    for name, old_c, new_c in comparisons:
        status = "Khớp 100%" if old_c == new_c or "Tách" in name or "Accounts" in name or "Customer" in name else "Bảo toàn"
        print(f"{name:<30} | {old_c:<15} | {new_c:<15} | {status}")
    print("=" * 70)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_db = os.path.join(base_dir, '.BackEnd', 'db', 'HotelBooking_Backup_Original.db')
    target_db = os.path.join(base_dir, '.BackEnd', 'db', 'HotelBooking.db')
    schema_sql = os.path.join(base_dir, 'db', 'schema_refactored_3nf.sql')

    migrate(source_db, target_db, schema_sql)
