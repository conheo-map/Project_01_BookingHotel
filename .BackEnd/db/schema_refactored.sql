-- =========================================================================
-- SAIGON - CONDAO ISLANDS RESORT BOOKING PLATFORM
-- REFACTORED DATABASE SCHEMA (3NF, CLEAN ARCHITECTURE, SINGLE IDENTITY, INTEGER VND)
-- =========================================================================

-- 1. DANH MỤC VAI TRÒ HỆ THỐNG
CREATE TABLE IF NOT EXISTS Roles (
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name   TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 2. BẢNG DANH TÍNH DUY NHẤT (SINGLE IDENTITY MODEL)
CREATE TABLE IF NOT EXISTS Accounts (
    account_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    account_type  TEXT NOT NULL CHECK(account_type IN ('customer', 'staff')),
    full_name     TEXT,
    phone         TEXT,
    is_active     INTEGER DEFAULT 1,
    created_at    TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_accounts_email ON Accounts(email);
CREATE INDEX IF NOT EXISTS idx_accounts_type ON Accounts(account_type);

-- 2.1. HỒ SƠ KHÁCH HÀNG (KẾ THỪA 1-1 TỪ ACCOUNTS)
CREATE TABLE IF NOT EXISTS Customer_Profiles (
    account_id     INTEGER PRIMARY KEY,
    loyalty_points INTEGER DEFAULT 0,
    tier           TEXT DEFAULT 'Newbie',
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- 2.2. HỒ SƠ NHÂN VIÊN (KẾ THỪA 1-1 TỪ ACCOUNTS)
CREATE TABLE IF NOT EXISTS Staff_Profiles (
    account_id INTEGER PRIMARY KEY,
    role_id    INTEGER NOT NULL,
    username   TEXT UNIQUE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- 3. KHÁCH SẠN VÀ LOẠI PHÒNG
CREATE TABLE IF NOT EXISTS Dim_Hotel (
    hotel_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel       TEXT NOT NULL,
    star_rating INTEGER DEFAULT 3,
    hotel_type  TEXT DEFAULT 'City Hotel'
);

CREATE TABLE IF NOT EXISTS Dim_RoomType (
    room_type_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_code      TEXT NOT NULL UNIQUE,
    hotel_id            INTEGER DEFAULT 1,
    max_adults          INTEGER DEFAULT 2,
    max_children        INTEGER DEFAULT 1,
    base_price          INTEGER NOT NULL DEFAULT 1000000, -- Lưu VND nguyên (INTEGER)
    extra_adult_fee     INTEGER DEFAULT 0,                -- VND nguyên
    child_breakfast_fee INTEGER DEFAULT 0,                -- VND nguyên
    allow_child_sharing INTEGER DEFAULT 1,
    extra_bed_capacity  INTEGER DEFAULT 0,
    description         TEXT DEFAULT '',
    amenities           TEXT DEFAULT '',
    images              TEXT DEFAULT '',
    main_image          TEXT DEFAULT '',
    is_active           INTEGER DEFAULT 1,
    FOREIGN KEY (hotel_id) REFERENCES Dim_Hotel(hotel_id)
);

-- 4. PHÒNG VẬT LÝ VÀ TRẠNG THÁI BUỒNG PHÒNG
CREATE TABLE IF NOT EXISTS Physical_Room (
    physical_room_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_id        INTEGER NOT NULL,
    room_name           TEXT NOT NULL UNIQUE,
    housekeeping_status TEXT NOT NULL DEFAULT 'Clean', -- 'Clean', 'Dirty', 'Inspected'
    is_active           INTEGER DEFAULT 1,
    description         TEXT DEFAULT '',
    amenities           TEXT DEFAULT '',
    images              TEXT DEFAULT '',
    main_image          TEXT DEFAULT '',
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (room_type_id) REFERENCES Dim_RoomType(room_type_id)
);
CREATE INDEX IF NOT EXISTS idx_physical_room_type ON Physical_Room(room_type_id);

-- 5. BẢNG GIÁ THEO NGÀY (ROOM RATES)
CREATE TABLE IF NOT EXISTS Room_Rates (
    rate_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_code   TEXT NOT NULL,
    valid_date       TEXT NOT NULL,
    base_price       INTEGER NOT NULL, -- VND nguyên
    is_holiday       INTEGER DEFAULT 0,
    physical_room_id INTEGER,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Room(physical_room_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_room_rates_lookup ON Room_Rates(room_type_code, valid_date);

-- 6. KHÓA GIỮ PHÒNG TẠM THỜI (ANTI OVERBOOKING / ROOM LOCKS)
CREATE TABLE IF NOT EXISTS Room_Lock (
    lock_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    physical_room_id INTEGER NOT NULL,
    session_id       TEXT NOT NULL,
    lock_date        TEXT NOT NULL,
    locked_until     TEXT NOT NULL,
    booking_temp_ref TEXT,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Room(physical_room_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_room_lock_date ON Room_Lock(physical_room_id, locked_until);
CREATE INDEX IF NOT EXISTS idx_room_lock_session ON Room_Lock(session_id);

-- 7. KHUYẾN MÃI VÀ CHÍNH SÁCH HOÀN TIỀN
CREATE TABLE IF NOT EXISTS Promotions (
    promotion_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    code                     TEXT NOT NULL UNIQUE,
    discount_percent         REAL DEFAULT 0.0,
    discount_type            TEXT DEFAULT 'percent', -- 'percent', 'fixed'
    active                   INTEGER DEFAULT 1,
    start_date               TEXT,
    end_date                 TEXT,
    description              TEXT DEFAULT '',
    apply_scope              TEXT DEFAULT 'all',     -- 'all', 'hotel', 'room_type'
    scope_value              TEXT DEFAULT '',
    max_uses                 INTEGER DEFAULT 0,
    current_uses             INTEGER DEFAULT 0,
    membership_tier_required TEXT DEFAULT 'Newbie',
    created_by_user_id       INTEGER
);

CREATE TABLE IF NOT EXISTS Refund_Policy (
    policy_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    days_before_arrival  INTEGER,
    hours_before_checkin INTEGER,
    refund_percent       REAL NOT NULL,
    description          TEXT DEFAULT ''
);

-- 8. BOOKING MASTER (CHUẨN 3NF - TÁCH KHỎI GOD TABLE NEW_BOOKINGS)
CREATE TABLE IF NOT EXISTS Booking_Master (
    booking_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id      INTEGER NULLABLE,  -- NULL cho khách walkin không tài khoản
    guest_name       TEXT,              -- Thông tin khách walkin hoặc người đại diện
    guest_phone      TEXT,              -- SĐT liên hệ
    guest_email      TEXT,              -- Email liên hệ
    hotel_id         INTEGER NOT NULL,
    room_type_id     INTEGER NOT NULL,
    physical_room_id INTEGER NULLABLE,
    arrival_date     TEXT NOT NULL,
    departure_date   TEXT NOT NULL,
    nights           INTEGER NOT NULL,
    guests           INTEGER DEFAULT 1,
    adults           INTEGER DEFAULT 1,
    children         INTEGER DEFAULT 0,
    babies           INTEGER DEFAULT 0,
    total_amount     INTEGER NOT NULL,  -- VND nguyên
    deposit_paid     INTEGER DEFAULT 0, -- VND nguyên
    tax_amount       INTEGER DEFAULT 0, -- VND nguyên
    discount_amount  INTEGER DEFAULT 0, -- VND nguyên
    booking_status   TEXT NOT NULL DEFAULT 'Confirmed', -- 'Confirmed', 'Checked-in', 'Checked-out', 'Canceled', 'No-Show'
    booking_type     TEXT DEFAULT 'continuous',         -- 'continuous', 'fragmented'
    special_requests TEXT DEFAULT '',
    promo_code       TEXT DEFAULT '',
    group_order_id   TEXT,
    created_at       TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (customer_id) REFERENCES Accounts(account_id) ON DELETE SET NULL,
    FOREIGN KEY (hotel_id) REFERENCES Dim_Hotel(hotel_id),
    FOREIGN KEY (room_type_id) REFERENCES Dim_RoomType(room_type_id),
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Room(physical_room_id)
);
CREATE INDEX IF NOT EXISTS idx_bm_dates ON Booking_Master(arrival_date, departure_date);
CREATE INDEX IF NOT EXISTS idx_bm_status ON Booking_Master(booking_status);
CREATE INDEX IF NOT EXISTS idx_bm_customer ON Booking_Master(customer_id);
CREATE INDEX IF NOT EXISTS idx_bm_pr ON Booking_Master(physical_room_id, booking_status);

-- 9. BOOKING NIGHTS (QUAN HỆ 1-N THAY THẾ HOÀN TOÀN CSV SELECTED_NIGHTS)
CREATE TABLE IF NOT EXISTS Booking_Nights (
    booking_night_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id       INTEGER NOT NULL,
    physical_room_id INTEGER NOT NULL,
    night_date       TEXT NOT NULL,
    created_at       TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Booking_Master(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Room(physical_room_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_booking_nights_booking_date ON Booking_Nights(booking_id, night_date);
CREATE INDEX IF NOT EXISTS idx_booking_nights_room_date ON Booking_Nights(physical_room_id, night_date);

-- 10. INVOICES (BẢNG HÓA ĐƠN ĐỘC LẬP)
CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id     INTEGER NOT NULL UNIQUE,
    invoice_number TEXT NOT NULL UNIQUE,
    issued_at      TEXT DEFAULT (datetime('now')),
    total_amount   INTEGER NOT NULL, -- VND nguyên
    payment_method TEXT DEFAULT 'cash',
    FOREIGN KEY (booking_id) REFERENCES Booking_Master(booking_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_invoices_number ON Invoices(invoice_number);

-- 11. BOOKING ATTRIBUTIONS (NGUỒN DỮ LIỆU MARKETING)
CREATE TABLE IF NOT EXISTS Booking_Attributions (
    attribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id     INTEGER NOT NULL UNIQUE,
    source_channel TEXT DEFAULT 'direct',
    utm_campaign   TEXT DEFAULT '',
    utm_medium     TEXT DEFAULT '',
    created_at     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Booking_Master(booking_id) ON DELETE CASCADE
);

-- 12. CANCELLATION RECORDS (BẢN GHI HỦY PHÒNG)
CREATE TABLE IF NOT EXISTS Cancellation_Records (
    cancellation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id      INTEGER NOT NULL UNIQUE,
    cancel_reason   TEXT DEFAULT '',
    canceled_by     INTEGER NULLABLE,
    refund_amount   INTEGER DEFAULT 0, -- VND nguyên
    refund_percent  REAL DEFAULT 0.0,
    canceled_at     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Booking_Master(booking_id) ON DELETE CASCADE
);

-- 13. THANH TOÁN (PAYMENTS)
CREATE TABLE IF NOT EXISTS Payments (
    payment_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id     INTEGER NOT NULL,
    user_id        INTEGER NULLABLE,
    amount         INTEGER NOT NULL, -- VND nguyên
    payment_method TEXT DEFAULT 'cash',
    payment_status TEXT DEFAULT 'Completed',
    payment_date   TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Booking_Master(booking_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_payments_booking ON Payments(booking_id);

-- 14. DỊCH VỤ PHÁT SINH (EXTRA SERVICES) & DANH MỤC
CREATE TABLE IF NOT EXISTS Service_Catalog (
    catalog_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name     TEXT NOT NULL,
    default_price INTEGER NOT NULL, -- VND nguyên
    category      TEXT DEFAULT 'Food'
);

CREATE TABLE IF NOT EXISTS Extra_Services (
    service_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id   INTEGER NOT NULL,
    service_name TEXT NOT NULL,
    quantity     INTEGER DEFAULT 1,
    unit_price   INTEGER NOT NULL, -- VND nguyên
    total_price  INTEGER NOT NULL, -- VND nguyên
    added_by     INTEGER,
    added_at     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Booking_Master(booking_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_extra_services_booking ON Extra_Services(booking_id);

-- 15. ĐÁNH GIÁ, ĐIỂM THƯỞNG, GIỎ HÀNG, TRACKING
CREATE TABLE IF NOT EXISTS Loyalty_Points (
    loyalty_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    total_nights INTEGER DEFAULT 0,
    tier         TEXT DEFAULT 'Newbie',
    points       INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reviews (
    review_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    hotel_id    INTEGER NOT NULL,
    booking_id  INTEGER NULLABLE,
    rating      INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comment     TEXT DEFAULT '',
    review_date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES Dim_Hotel(hotel_id)
);

CREATE TABLE IF NOT EXISTS Cart_Sessions (
    session_id TEXT PRIMARY KEY,
    user_id    INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Cart_Items (
    cart_item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id       TEXT NOT NULL,
    room_type_id     INTEGER NOT NULL,
    physical_room_id INTEGER,
    arrival_date     TEXT NOT NULL,
    departure_date   TEXT NOT NULL,
    adults           INTEGER DEFAULT 1,
    children         INTEGER DEFAULT 0,
    babies           INTEGER DEFAULT 0,
    booking_type     TEXT DEFAULT 'continuous',
    selected_nights  TEXT DEFAULT '',
    total_price      INTEGER NOT NULL,
    source_channel   TEXT DEFAULT 'direct',
    utm_campaign     TEXT DEFAULT '',
    utm_medium       TEXT DEFAULT '',
    FOREIGN KEY (session_id) REFERENCES Cart_Sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Funnel_Events (
    event_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id     TEXT,
    user_id        INTEGER,
    event_name     TEXT NOT NULL,
    hotel_id       INTEGER,
    room_type_id   INTEGER,
    booking_id     INTEGER,
    metadata_json  TEXT DEFAULT '{}',
    source_channel TEXT DEFAULT 'direct',
    utm_campaign   TEXT DEFAULT '',
    utm_medium     TEXT DEFAULT '',
    created_at     TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Auth_Sessions (
    token          TEXT PRIMARY KEY,
    principal_type TEXT,
    user_id        INTEGER,
    account_id     INTEGER,
    role_id        INTEGER,
    expires_at     TEXT
);

-- =========================================================================
-- BACKWARD COMPATIBILITY VIEWS (ĐẢM BẢO KHÔNG BỊ GÃY HỆ THỐNG CŨ)
-- =========================================================================

CREATE VIEW IF NOT EXISTS New_Bookings AS
SELECT 
    bm.booking_id,
    bm.customer_id AS user_id,
    bm.hotel_id,
    bm.room_type_id,
    bm.arrival_date,
    bm.departure_date,
    bm.nights,
    bm.guests,
    bm.total_amount AS total_price,
    CASE WHEN bm.booking_status = 'Canceled' THEN 1 ELSE 0 END AS is_canceled,
    bm.booking_status AS status,
    bm.promo_code,
    bm.discount_amount,
    bm.created_at,
    bm.physical_room_id AS room_id,
    bm.booking_status AS status_detail,
    bm.deposit_paid,
    bm.physical_room_id,
    bm.booking_type,
    '' AS selected_nights,
    bm.adults,
    bm.children,
    bm.babies,
    COALESCE(cr.cancel_reason, '') AS cancel_reason,
    cr.canceled_by,
    bm.tax_amount,
    bm.special_requests,
    bm.group_order_id,
    COALESCE(ba.source_channel, 'direct') AS source_channel,
    COALESCE(ba.utm_campaign, '') AS utm_campaign,
    COALESCE(ba.utm_medium, '') AS utm_medium,
    COALESCE(inv.invoice_number, '') AS invoice_number,
    inv.issued_at AS invoice_issued_at,
    bm.total_amount AS total_price_cents,
    bm.discount_amount AS discount_amount_cents,
    bm.tax_amount AS tax_amount_cents,
    bm.deposit_paid AS deposit_paid_cents
FROM Booking_Master bm
LEFT JOIN Invoices inv ON bm.booking_id = inv.booking_id
LEFT JOIN Booking_Attributions ba ON bm.booking_id = ba.booking_id
LEFT JOIN Cancellation_Records cr ON bm.booking_id = cr.booking_id;

CREATE VIEW IF NOT EXISTS Users AS
SELECT 
    a.account_id AS user_id,
    COALESCE(sp.username, a.email) AS username,
    a.password_hash,
    a.email,
    a.full_name,
    a.is_active,
    a.created_at
FROM Accounts a
LEFT JOIN Staff_Profiles sp ON a.account_id = sp.account_id;

CREATE VIEW IF NOT EXISTS Customer_Accounts AS
SELECT 
    a.account_id,
    a.email,
    a.password_hash,
    a.full_name AS customer_name,
    COALESCE(cp.loyalty_points, 0) AS loyalty_points,
    COALESCE(cp.tier, 'Newbie') AS membership_tier,
    a.created_at
FROM Accounts a
JOIN Customer_Profiles cp ON a.account_id = cp.account_id;

CREATE VIEW IF NOT EXISTS User_Roles AS
SELECT 
    sp.account_id AS user_id,
    sp.role_id
FROM Staff_Profiles sp;
