import os
import sqlite3
import sys
from datetime import datetime, timedelta

def run_migration(source_db_path, target_db_path, schema_sql_path):
    print(f"Starting migration from {source_db_path} to {target_db_path}...")
    
    # 1. Kết nối DB nguồn
    src_conn = sqlite3.connect(source_db_path)
    src_conn.row_factory = sqlite3.Row
    src_cur = src_conn.cursor()

    # 2. Xóa DB đích nếu tồn tại để tạo mới hoàn toàn sạch
    if os.path.exists(target_db_path):
        os.remove(target_db_path)

    dst_conn = sqlite3.connect(target_db_path)
    dst_conn.execute("PRAGMA journal_mode=WAL")
    dst_conn.execute("PRAGMA foreign_keys=OFF") # Tắt FK trong quá trình nạp dữ liệu hàng loạt
    dst_cur = dst_conn.cursor()

    # 3. Tạo schema mới
    with open(schema_sql_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    dst_cur.executescript(schema_sql)
    print("Schema created successfully.")

    # 4. Migrate Roles
    src_cur.execute("SELECT role_id, role_name, description FROM Roles")
    roles = src_cur.fetchall()
    dst_cur.executemany("INSERT OR REPLACE INTO Roles (role_id, role_name, description) VALUES (?, ?, ?)",
                        [(r['role_id'], r['role_name'], r['description']) for r in roles])
    print(f"Migrated {len(roles)} roles.")

    # 5. Migrate Staff & Identity
    # 5.1 Staff Profiles
    src_cur.execute("""
        SELECT u.user_id, u.username, u.email, u.password_hash, u.full_name, u.is_active, u.created_at, ur.role_id
        FROM Users u
        JOIN User_Roles ur ON u.user_id = ur.user_id
    """)
    staff_rows = src_cur.fetchall()
    staff_id_map = {}
    for s in staff_rows:
        new_account_id = 90000 + s['user_id']
        staff_id_map[s['user_id']] = new_account_id
        dst_cur.execute("""
            INSERT INTO Accounts (account_id, email, password_hash, account_type, full_name, is_active, created_at)
            VALUES (?, ?, ?, 'staff', ?, ?, ?)
        """, (new_account_id, s['email'], s['password_hash'], s['full_name'], s['is_active'] or 1, s['created_at']))
        dst_cur.execute("""
            INSERT INTO Staff_Profiles (account_id, role_id, username)
            VALUES (?, ?, ?)
        """, (new_account_id, s['role_id'], s['username']))
    print(f"Migrated {len(staff_rows)} staff accounts.")

    # 5.2 Customer Profiles
    src_cur.execute("SELECT account_id, email, password_hash, customer_name, loyalty_points, membership_tier, created_at FROM Customer_Accounts")
    customer_rows = src_cur.fetchall()
    cust_count = 0
    walkin_account_ids = set()
    for c in customer_rows:
        email = c['email'] or ''
        if email.endswith('@walkin.local'):
            walkin_account_ids.add(c['account_id'])
            continue # Chấm dứt việc lưu tài khoản rác cho walk-in
        dst_cur.execute("""
            INSERT INTO Accounts (account_id, email, password_hash, account_type, full_name, is_active, created_at)
            VALUES (?, ?, ?, 'customer', ?, 1, ?)
        """, (c['account_id'], email, c['password_hash'], c['customer_name'], c['created_at']))
        dst_cur.execute("""
            INSERT INTO Customer_Profiles (account_id, loyalty_points, tier)
            VALUES (?, ?, ?)
        """, (c['account_id'], c['loyalty_points'] or 0, c['membership_tier'] or 'Newbie'))
        cust_count += 1
    print(f"Migrated {cust_count} customer accounts (filtered {len(walkin_account_ids)} walkin garbage accounts).")

    # 6. Migrate Dim_Hotel
    src_cur.execute("SELECT hotel_id, hotel, star_rating, hotel_type FROM Dim_Hotel")
    hotels = src_cur.fetchall()
    dst_cur.executemany("INSERT OR REPLACE INTO Dim_Hotel (hotel_id, hotel, star_rating, hotel_type) VALUES (?, ?, ?, ?)",
                        [(h['hotel_id'], h['hotel'], h['star_rating'], h['hotel_type']) for h in hotels])
    print(f"Migrated {len(hotels)} hotels.")

    # 7. Migrate Dim_RoomType (Chuyển tiền VND nguyên, xóa _cents)
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
    print(f"Migrated {len(room_types)} room types.")

    # 8. Migrate Physical_Room
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
    print(f"Migrated {len(prooms)} physical rooms.")

    # 9. Migrate Room_Rates (Chuẩn hóa VND nguyên, bỏ _cents)
    src_cur.execute("SELECT rate_id, room_type_code, valid_date, base_price, is_holiday, physical_room_id FROM Room_Rates")
    rates = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Room_Rates (rate_id, room_type_code, valid_date, base_price, is_holiday, physical_room_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [(r['rate_id'], r['room_type_code'], r['valid_date'], int(round(float(r['base_price'] or 0))), r['is_holiday'], r['physical_room_id']) for r in rates])
    print(f"Migrated {len(rates)} room rates.")

    # 10. Migrate Room_Lock
    src_cur.execute("SELECT lock_id, physical_room_id, session_id, lock_date, locked_until, booking_temp_ref FROM Room_Lock")
    locks = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Room_Lock (lock_id, physical_room_id, session_id, lock_date, locked_until, booking_temp_ref)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [(l['lock_id'], l['physical_room_id'], l['session_id'], l['lock_date'], l['locked_until'], l['booking_temp_ref']) for l in locks])
    print(f"Migrated {len(locks)} room locks.")

    # 11. Migrate Promotions & Refund_Policy
    src_cur.execute("""
        SELECT promotion_id, code, discount_percent, discount_type, active, start_date, end_date,
               description, apply_scope, scope_value, max_uses, current_uses,
               membership_tier_required, created_by_user_id
        FROM Promotions
    """)
    promos = src_cur.fetchall()
    for p in promos:
        created_by = staff_id_map.get(p['created_by_user_id']) if p['created_by_user_id'] else None
        dst_cur.execute("""
            INSERT OR REPLACE INTO Promotions (
                promotion_id, code, discount_percent, discount_type, active, start_date, end_date,
                description, apply_scope, scope_value, max_uses, current_uses,
                membership_tier_required, created_by_user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p['promotion_id'], p['code'], p['discount_percent'], p['discount_type'] or 'percent',
              p['active'], p['start_date'], p['end_date'], p['description'] or '',
              p['apply_scope'] or 'all', p['scope_value'] or '', p['max_uses'] or 0,
              p['current_uses'] or 0, p['membership_tier_required'] or 'Newbie', created_by))
    print(f"Migrated {len(promos)} promotions.")

    src_cur.execute("SELECT policy_id, days_before_arrival, hours_before_checkin, refund_percent, description FROM Refund_Policy")
    policies = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Refund_Policy (policy_id, days_before_arrival, hours_before_checkin, refund_percent, description)
        VALUES (?, ?, ?, ?, ?)
    """, [(p['policy_id'], p['days_before_arrival'], p['hours_before_checkin'], p['refund_percent'], p['description']) for p in policies])
    print(f"Migrated {len(policies)} refund policies.")

    # 12. TÁCH GOD TABLE NEW_BOOKINGS -> BOOKING_MASTER, INVOICES, ATTRIBUTIONS, CANCELLATIONS
    src_cur.execute("""
        SELECT booking_id, user_id, hotel_id, room_type_id, arrival_date, departure_date,
               nights, guests, total_price, is_canceled, status, promo_code, discount_amount,
               created_at, physical_room_id, status_detail, deposit_paid, booking_type,
               adults, children, babies, cancel_reason, canceled_by, tax_amount, special_requests,
               group_order_id, source_channel, utm_campaign, utm_medium, invoice_number, invoice_issued_at
        FROM New_Bookings
    """)
    bookings = src_cur.fetchall()

    invoices_batch = []
    attributions_batch = []
    cancellations_batch = []
    master_batch = []

    for b in bookings:
        b_id = b['booking_id']
        u_id = b['user_id']
        cust_id = u_id
        g_name = ''
        g_phone = ''

        # Nếu là walkin không có account
        if u_id in walkin_account_ids:
            cust_id = None
            # Tìm email để lấy số điện thoại
            src_cur.execute("SELECT email, customer_name FROM Customer_Accounts WHERE account_id = ?", (u_id,))
            walk_row = src_cur.fetchone()
            if walk_row:
                g_phone = walk_row['email'].split('@')[0] if '@' in walk_row['email'] else ''
                g_name = walk_row['customer_name'] or 'Walk-in Guest'

        total_amount = int(round(float(b['total_price'] or 0)))
        deposit_paid = int(round(float(b['deposit_paid'] or 0)))
        tax_amount = int(round(float(b['tax_amount'] or 0)))
        discount_amount = int(round(float(b['discount_amount'] or 0)))

        # Status
        status_detail = b['status_detail'] or b['status'] or 'Confirmed'
        if b['is_canceled'] == 1 and status_detail != 'Canceled':
            status_detail = 'Canceled'

        master_batch.append((
            b_id, cust_id, g_name, g_phone, '',
            b['hotel_id'] or 1, b['room_type_id'], b['physical_room_id'],
            b['arrival_date'], b['departure_date'], b['nights'] or 1,
            b['guests'] or 1, b['adults'] or 1, b['children'] or 0, b['babies'] or 0,
            total_amount, deposit_paid, tax_amount, discount_amount,
            status_detail, b['booking_type'] or 'continuous',
            b['special_requests'] or '', b['promo_code'] or '',
            b['group_order_id'], b['created_at']
        ))

        # Attributions
        attributions_batch.append((
            b_id,
            b['source_channel'] or 'direct',
            b['utm_campaign'] or '',
            b['utm_medium'] or '',
            b['created_at']
        ))

        # Invoices
        inv_num = (b['invoice_number'] or '').strip()
        if inv_num:
            invoices_batch.append((
                b_id,
                inv_num,
                b['invoice_issued_at'] or b['created_at'],
                total_amount,
                'cash'
            ))

        # Cancellations
        if status_detail == 'Canceled' or (b['cancel_reason'] or '').strip():
            canc_by = staff_id_map.get(b['canceled_by']) if b['canceled_by'] else None
            cancellations_batch.append((
                b_id,
                b['cancel_reason'] or 'Khách yêu cầu hủy',
                canc_by,
                0, # refund_amount
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
    """, master_batch)
    print(f"Migrated {len(master_batch)} records to Booking_Master.")

    dst_cur.executemany("""
        INSERT INTO Booking_Attributions (booking_id, source_channel, utm_campaign, utm_medium, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, attributions_batch)
    print(f"Migrated {len(attributions_batch)} records to Booking_Attributions.")

    dst_cur.executemany("""
        INSERT INTO Invoices (booking_id, invoice_number, issued_at, total_amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
    """, invoices_batch)
    print(f"Migrated {len(invoices_batch)} records to Invoices.")

    dst_cur.executemany("""
        INSERT INTO Cancellation_Records (booking_id, cancel_reason, canceled_by, refund_amount, refund_percent, canceled_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, cancellations_batch)
    print(f"Migrated {len(cancellations_batch)} records to Cancellation_Records.")

    # 13. Migrate Booking_Nights (Quan hệ 1-N chuẩn hóa)
    src_cur.execute("SELECT booking_night_id, booking_id, physical_room_id, night_date, created_at FROM Booking_Nights")
    bn_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Booking_Nights (booking_night_id, booking_id, physical_room_id, night_date, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, [(bn['booking_night_id'], bn['booking_id'], bn['physical_room_id'], bn['night_date'], bn['created_at']) for bn in bn_rows])
    print(f"Migrated {len(bn_rows)} records to Booking_Nights.")

    # 14. Migrate Payments (VND nguyên, bỏ amount_cents)
    src_cur.execute("SELECT payment_id, booking_id, user_id, amount, payment_method, payment_status, payment_date FROM Payments")
    pm_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Payments (payment_id, booking_id, user_id, amount, payment_method, payment_status, payment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [(p['payment_id'], p['booking_id'], p['user_id'], int(round(float(p['amount'] or 0))), p['payment_method'], p['payment_status'], p['payment_date']) for p in pm_rows])
    print(f"Migrated {len(pm_rows)} payments.")

    # 15. Migrate Service_Catalog & Extra_Services (VND nguyên, bỏ _cents)
    src_cur.execute("SELECT catalog_id, item_name, default_price, category FROM Service_Catalog")
    sc_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Service_Catalog (catalog_id, item_name, default_price, category)
        VALUES (?, ?, ?, ?)
    """, [(sc['catalog_id'], sc['item_name'], int(round(float(sc['default_price'] or 0))), sc['category']) for sc in sc_rows])
    print(f"Migrated {len(sc_rows)} service catalog items.")

    src_cur.execute("SELECT service_id, booking_id, service_name, quantity, unit_price, total_price, added_by, added_at FROM Extra_Services")
    es_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Extra_Services (service_id, booking_id, service_name, quantity, unit_price, total_price, added_by, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [(es['service_id'], es['booking_id'], es['service_name'], es['quantity'],
           int(round(float(es['unit_price'] or 0))), int(round(float(es['total_price'] or 0))),
           staff_id_map.get(es['added_by'], es['added_by']), es['added_at']) for es in es_rows])
    print(f"Migrated {len(es_rows)} extra services.")

    # 16. Migrate Loyalty_Points, Reviews, Cart, Funnel
    src_cur.execute("SELECT loyalty_id, user_id, total_nights, tier, points FROM Loyalty_Points")
    lp_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Loyalty_Points (loyalty_id, user_id, total_nights, tier, points)
        VALUES (?, ?, ?, ?, ?)
    """, [(lp['loyalty_id'], lp['user_id'], lp['total_nights'], lp['tier'], lp['points']) for lp in lp_rows])
    print(f"Migrated {len(lp_rows)} loyalty points records.")

    src_cur.execute("SELECT review_id, user_id, hotel_id, booking_id, rating, comment, review_date FROM Reviews")
    rev_rows = src_cur.fetchall()
    dst_cur.executemany("""
        INSERT OR REPLACE INTO Reviews (review_id, user_id, hotel_id, booking_id, rating, comment, review_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [(r['review_id'], r['user_id'], r['hotel_id'], r['booking_id'], r['rating'], r['comment'], r['review_date']) for r in rev_rows])
    print(f"Migrated {len(rev_rows)} reviews.")

    src_cur.execute("SELECT session_id, user_id, created_at FROM Cart_Sessions")
    cs_rows = src_cur.fetchall()
    dst_cur.executemany("INSERT OR REPLACE INTO Cart_Sessions (session_id, user_id, created_at) VALUES (?, ?, ?)",
                        [(cs['session_id'], cs['user_id'], cs['created_at']) for cs in cs_rows])
    print(f"Migrated {len(cs_rows)} cart sessions.")

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
    print(f"Migrated {len(ci_rows)} cart items.")

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
    print(f"Migrated {len(fe_rows)} funnel events.")

    # 16. Dọn dẹp Cart_Items mồ côi (session_id không có trong Cart_Sessions)
    dst_cur.execute("DELETE FROM Cart_Items WHERE session_id NOT IN (SELECT session_id FROM Cart_Sessions)")

    dst_conn.commit()
    dst_conn.execute("PRAGMA foreign_keys=ON")
    print("Migration completed and foreign keys re-enabled successfully!")
    src_conn.close()
    dst_conn.close()

if __name__ == '__main__':
    source_db = '.BackEnd/db/HotelBooking.db'
    target_db = '.BackEnd/db/HotelBooking.db'
    schema_sql = '.BackEnd/db/schema_refactored.sql'
    
    # Tạo bản sao nguồn tạm thời để đọc, rồi ghi đè sạch sẽ vào target
    temp_source = '.BackEnd/db/HotelBooking_source_temp.db'
    import shutil
    shutil.copy2(source_db, temp_source)
    try:
        run_migration(temp_source, target_db, schema_sql)
        print("Successfully migrated active database to 3NF schema!")
    finally:
        if os.path.exists(temp_source):
            os.remove(temp_source)
