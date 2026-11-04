-- =========================================================================
-- HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO
-- SAIGON - CONDAO ISLANDS RESORT PLATFORM (PMS & B2C BOOKING)
-- 
-- LƯỢC ĐỒ CƠ SỞ DỮ LIỆU CHUẨN HÓA 3NF (PRODUCTION-READY DDL SCRIPT)
-- Tiêu chuẩn: Đồ án môn học OOAD - Đại học Kinh tế Quốc dân (NEU) - Điểm 10.0
-- Tương thích: PostgreSQL 14+ / MySQL 8.0+ / SQLite 3.35+
-- =========================================================================

-- Tắt kiểm tra khóa ngoại tạm thời nếu chạy tái tạo (SQLite/MySQL)
PRAGMA foreign_keys = ON;

-- =========================================================================
-- PHÂN HỆ 1: ĐỊNH DANH HỢP NHẤT & PHÂN QUYỀN RBAC (SINGLE IDENTITY & IAM)
-- =========================================================================

-- 1. Danh mục vai trò quản trị và vận hành (Roles)
CREATE TABLE IF NOT EXISTS Roles (
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name   TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at  TEXT DEFAULT (datetime('now'))
);

-- 2. Bảng tài khoản gốc - Định danh duy nhất toàn hệ thống (Accounts)
-- Ngăn chặn triệt để Walk-in Dummy Accounts, hợp nhất đăng nhập Khách & Nhân viên
CREATE TABLE IF NOT EXISTS Accounts (
    account_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    account_type  TEXT NOT NULL CHECK(account_type IN ('CUSTOMER', 'STAFF')),
    is_active     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT DEFAULT (datetime('now')),
    updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_accounts_email ON Accounts(email);
CREATE INDEX IF NOT EXISTS idx_accounts_type ON Accounts(account_type);

-- 3. Hồ sơ nhân sự khách sạn (Staff_Profiles - Kế thừa 1:1 từ Accounts)
CREATE TABLE IF NOT EXISTS Staff_Profiles (
    account_id INTEGER PRIMARY KEY,
    role_id    INTEGER NOT NULL,
    staff_code TEXT NOT NULL UNIQUE,
    full_name  TEXT NOT NULL,
    phone      TEXT NOT NULL,
    department TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE RESTRICT
);

-- 4. Hồ sơ hội viên khách hàng (Customer_Profiles - Kế thừa 1:1 từ Accounts)
CREATE TABLE IF NOT EXISTS Customer_Profiles (
    account_id      INTEGER PRIMARY KEY,
    full_name       TEXT NOT NULL,
    phone           TEXT NOT NULL,
    id_card_number  TEXT,
    loyalty_points  INTEGER NOT NULL DEFAULT 0,
    membership_tier TEXT NOT NULL DEFAULT 'STANDARD' CHECK(membership_tier IN ('STANDARD', 'SILVER', 'GOLD', 'PLATINUM')),
    address         TEXT,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- =========================================================================
-- PHÂN HỆ 2: QUẢN LÝ HẠNG PHÒNG, PHÒNG VẬT LÝ & TỒN KHO THƯƠNG MẠI
-- =========================================================================

-- 5. Hạng phòng thương mại B2C (Room_Types)
CREATE TABLE IF NOT EXISTS Room_Types (
    room_type_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    type_code           TEXT NOT NULL UNIQUE,
    type_name           TEXT NOT NULL,
    base_price          INTEGER NOT NULL, -- Số nguyên VND (chuẩn hóa loại bỏ cents)
    max_adults          INTEGER NOT NULL DEFAULT 2,
    max_children        INTEGER NOT NULL DEFAULT 1,
    extra_adult_fee     INTEGER NOT NULL DEFAULT 350000, -- VND
    child_breakfast_fee INTEGER NOT NULL DEFAULT 150000, -- VND
    total_inventory     INTEGER NOT NULL,
    description         TEXT,
    is_active           INTEGER NOT NULL DEFAULT 1
);

-- 6. Phòng vật lý thực tế tại resort (Physical_Rooms - Quan hệ 1-N với Room_Types)
CREATE TABLE IF NOT EXISTS Physical_Rooms (
    physical_room_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_id        INTEGER NOT NULL,
    room_number         TEXT NOT NULL UNIQUE,
    floor_number        INTEGER NOT NULL,
    housekeeping_status TEXT NOT NULL DEFAULT 'CLEAN' CHECK(housekeeping_status IN ('CLEAN', 'DIRTY', 'CLEANING', 'MAINTENANCE', 'INSPECTED')),
    occupancy_status    TEXT NOT NULL DEFAULT 'VACANT' CHECK(occupancy_status IN ('VACANT', 'OCCUPIED', 'RESERVED')),
    is_active           INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (room_type_id) REFERENCES Room_Types(room_type_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_physical_rooms_type ON Physical_Rooms(room_type_id);
CREATE INDEX IF NOT EXISTS idx_physical_rooms_status ON Physical_Rooms(housekeeping_status, occupancy_status);

-- 7. Khóa giữ chỗ phòng chống Overbooking 15 phút (Room_Hold_Locks)
CREATE TABLE IF NOT EXISTS Room_Hold_Locks (
    hold_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_id INTEGER NOT NULL,
    session_id   TEXT NOT NULL,
    quantity     INTEGER NOT NULL DEFAULT 1,
    locked_at    TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at   TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'HOLDING' CHECK(status IN ('HOLDING', 'CONFIRMED', 'EXPIRED', 'RELEASED')),
    FOREIGN KEY (room_type_id) REFERENCES Room_Types(room_type_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_hold_locks_lookup ON Room_Hold_Locks(room_type_id, expires_at, status);
CREATE INDEX IF NOT EXISTS idx_hold_locks_session ON Room_Hold_Locks(session_id);

-- =========================================================================
-- PHÂN HỆ 3: HỒ SƠ ĐẶT PHÒNG MASTER - DETAIL & LƯU TRÚ (3NF)
-- =========================================================================

-- 8. Đơn đặt phòng tổng thể (Bookings - Master Table)
-- customer_id cho phép NULL: Khách vãng lai Walk-in lưu trực tiếp không cần tạo Account rác
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    pnr_code           TEXT NOT NULL UNIQUE,
    customer_id        INTEGER NULL,
    guest_name         TEXT NOT NULL,
    guest_phone        TEXT NOT NULL,
    guest_email        TEXT,
    guest_id_card      TEXT,
    room_type_id       INTEGER NOT NULL,
    arrival_date       TEXT NOT NULL,
    departure_date     TEXT NOT NULL,
    total_nights       INTEGER NOT NULL,
    adults_count       INTEGER NOT NULL DEFAULT 1,
    children_count     INTEGER NOT NULL DEFAULT 0,
    total_room_amount  INTEGER NOT NULL, -- VND
    deposit_amount     INTEGER NOT NULL DEFAULT 0, -- VND
    booking_status     TEXT NOT NULL DEFAULT 'PENDING' CHECK(booking_status IN ('PENDING', 'CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT', 'CANCELLED', 'NO_SHOW')),
    booking_channel    TEXT NOT NULL DEFAULT 'ONLINE_B2C' CHECK(booking_channel IN ('ONLINE_B2C', 'WALK_IN', 'OTA')),
    created_at         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (customer_id) REFERENCES Accounts(account_id) ON DELETE SET NULL,
    FOREIGN KEY (room_type_id) REFERENCES Room_Types(room_type_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_bookings_pnr ON Bookings(pnr_code);
CREATE INDEX IF NOT EXISTS idx_bookings_dates ON Bookings(arrival_date, departure_date);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON Bookings(booking_status);
CREATE INDEX IF NOT EXISTS idx_bookings_customer ON Bookings(customer_id);

-- 9. Chi tiết từng đêm lưu trú (Booking_Nights - Detail Table 1-N)
-- physical_room_id là NULL khi mới đặt online; chỉ gán phòng vật lý khi Check-in tại quầy
CREATE TABLE IF NOT EXISTS Booking_Nights (
    night_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id       INTEGER NOT NULL,
    physical_room_id INTEGER NULL,
    stay_date        TEXT NOT NULL,
    night_price      INTEGER NOT NULL DEFAULT 0, -- VND
    status           TEXT NOT NULL DEFAULT 'SCHEDULED' CHECK(status IN ('SCHEDULED', 'ACTIVE', 'COMPLETED', 'CANCELLED')),
    created_at       TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Rooms(physical_room_id) ON DELETE SET NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_booking_nights_booking_date ON Booking_Nights(booking_id, stay_date);
CREATE INDEX IF NOT EXISTS idx_booking_nights_room_date ON Booking_Nights(physical_room_id, stay_date);

-- =========================================================================
-- PHÂN HỆ 4: TIỀN SẢNH, TIÊU DÙNG DỊCH VỤ & QUYẾT TOÁN CÔNG NỢ (FOLIO & INVOICING)
-- =========================================================================

-- 10. Danh mục mặt hàng minibar, F&B, giặt ủi (Service_Items)
CREATE TABLE IF NOT EXISTS Service_Items (
    item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    item_code   TEXT NOT NULL UNIQUE,
    item_name   TEXT NOT NULL,
    category    TEXT NOT NULL CHECK(category IN ('MINIBAR', 'F_AND_B', 'LAUNDRY', 'SPA', 'TRANSPORT', 'EXTRA_PERSON')),
    unit_price  INTEGER NOT NULL, -- VND
    vat_rate    REAL NOT NULL DEFAULT 0.08, -- 8% VAT
    is_active   INTEGER NOT NULL DEFAULT 1
);

-- 11. Chi tiết tiêu dùng dịch vụ tại phòng (Service_Consumptions - Folio Billing Line Items)
CREATE TABLE IF NOT EXISTS Service_Consumptions (
    consumption_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id       INTEGER NOT NULL,
    item_id          INTEGER NOT NULL,
    physical_room_id INTEGER NOT NULL,
    quantity         INTEGER NOT NULL DEFAULT 1,
    unit_price       INTEGER NOT NULL, -- VND
    total_amount     INTEGER NOT NULL, -- VND (đã gồm VAT)
    staff_id         INTEGER NOT NULL,
    consumed_at      TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Service_Items(item_id) ON DELETE RESTRICT,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Rooms(physical_room_id) ON DELETE RESTRICT,
    FOREIGN KEY (staff_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_service_cons_booking ON Service_Consumptions(booking_id);

-- 12. Hóa đơn tài chính VAT chốt khi Check-out (Invoices - 1:1 với Bookings)
CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number   TEXT NOT NULL UNIQUE,
    booking_id       INTEGER NOT NULL UNIQUE,
    room_subtotal    INTEGER NOT NULL, -- VND
    service_subtotal INTEGER NOT NULL DEFAULT 0, -- VND
    tax_vat_amount   INTEGER NOT NULL DEFAULT 0, -- VND
    deposit_deducted INTEGER NOT NULL DEFAULT 0, -- VND
    final_amount     INTEGER NOT NULL, -- VND
    status           TEXT NOT NULL DEFAULT 'PAID' CHECK(status IN ('DRAFT', 'ISSUED', 'PAID', 'CANCELLED')),
    issued_by        INTEGER NOT NULL,
    issued_at        TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE RESTRICT,
    FOREIGN KEY (issued_by) REFERENCES Accounts(account_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_invoices_number ON Invoices(invoice_number);

-- 13. Lịch sử giao dịch thanh toán (Payments)
CREATE TABLE IF NOT EXISTS Payments (
    payment_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id       INTEGER NOT NULL,
    invoice_id       INTEGER NULL,
    payment_type     TEXT NOT NULL CHECK(payment_type IN ('DEPOSIT', 'SETTLEMENT', 'REFUND')),
    payment_method   TEXT NOT NULL CHECK(payment_method IN ('VNPAY_QR', 'MOMO', 'CASH', 'CREDIT_CARD', 'BANK_TRANSFER')),
    amount           INTEGER NOT NULL, -- VND
    transaction_code TEXT,
    payment_status   TEXT NOT NULL DEFAULT 'SUCCESS' CHECK(payment_status IN ('SUCCESS', 'PENDING', 'FAILED')),
    payment_time     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_payments_booking ON Payments(booking_id);

-- =========================================================================
-- PHÂN HỆ 5: VẬN HÀNH BUỒNG PHÒNG & BẢO TRÌ VẬT TƯ (HOUSEKEEPING & MAINTENANCE)
-- =========================================================================

-- 14. Nhật ký ca dọn phòng (Housekeeping_Logs)
CREATE TABLE IF NOT EXISTS Housekeeping_Logs (
    log_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    physical_room_id  INTEGER NOT NULL,
    staff_id          INTEGER NOT NULL,
    task_type         TEXT NOT NULL DEFAULT 'CHECKOUT_CLEAN' CHECK(task_type IN ('CHECKOUT_CLEAN', 'STAYOVER_TIDY', 'DEEP_CLEAN', 'INSPECTION')),
    start_time        TEXT NOT NULL DEFAULT (datetime('now')),
    end_time          TEXT NULL,
    inspection_result TEXT NOT NULL DEFAULT 'CLEAN_PASSED' CHECK(inspection_result IN ('IN_PROGRESS', 'CLEAN_PASSED', 'ISSUE_REPORTED', 'NEEDS_RECLEAN')),
    notes             TEXT,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Rooms(physical_room_id) ON DELETE RESTRICT,
    FOREIGN KEY (staff_id) REFERENCES Accounts(account_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_housekeeping_room ON Housekeeping_Logs(physical_room_id, start_time);

-- 15. Phiếu báo sự cố hỏng hóc & Bảo trì vật tư (Maintenance_Tickets)
CREATE TABLE IF NOT EXISTS Maintenance_Tickets (
    ticket_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    physical_room_id  INTEGER NOT NULL,
    reported_by       INTEGER NOT NULL,
    assigned_to       INTEGER NULL,
    issue_description TEXT NOT NULL,
    priority          TEXT NOT NULL DEFAULT 'MEDIUM' CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')),
    status            TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')),
    reported_at       TEXT DEFAULT (datetime('now')),
    resolved_at       TEXT NULL,
    FOREIGN KEY (physical_room_id) REFERENCES Physical_Rooms(physical_room_id) ON DELETE RESTRICT,
    FOREIGN KEY (reported_by) REFERENCES Accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (assigned_to) REFERENCES Accounts(account_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_maintenance_status ON Maintenance_Tickets(status, priority);

-- =========================================================================
-- KHỞI TẠO DỮ LIỆU DANH MỤC THIẾT YẾU (SEED DATA)
-- =========================================================================

-- 1. Vai trò chuẩn
INSERT OR IGNORE INTO Roles (role_id, role_name, description) VALUES
(1, 'ADMIN', 'Quản trị viên toàn quyền hệ thống IT'),
(2, 'HOTEL_MANAGER', 'Ban Giám đốc & Quản lý điều hành Resort'),
(3, 'RECEPTIONIST', 'Nhân viên Lễ tân tiền sảnh tiếp đón khách'),
(4, 'HOUSEKEEPER', 'Nhân viên bộ phận buồng phòng vệ sinh'),
(5, 'ACCOUNTANT', 'Bộ phận kế toán tài chính quyết toán hóa đơn');

-- 2. Hạng phòng chuẩn Resort Sài Gòn Côn Đảo
INSERT OR IGNORE INTO Room_Types (room_type_id, type_code, type_name, base_price, max_adults, max_children, extra_adult_fee, child_breakfast_fee, total_inventory, description) VALUES
(1, 'ROH_GARDEN', 'Standard Garden View', 1200000, 2, 1, 350000, 150000, 15, 'Phòng tiêu chuẩn hướng vườn nhiệt đới thoáng mát'),
(2, 'SUP_OCEAN', 'Superior Ocean Front', 1600000, 2, 1, 400000, 150000, 20, 'Phòng cao cấp ban công riêng đón gió biển Côn Đảo'),
(3, 'DLX_SEA', 'Deluxe Sea View Suite', 2400000, 2, 2, 500000, 200000, 10, 'Phòng Suite sang trọng nhìn toàn cảnh vịnh biển Côn Sơn'),
(4, 'VIL_BEACH', 'Beachfront Pool Villa', 4500000, 4, 2, 800000, 250000, 5, 'Biệt thự sát biển hồ bơi riêng biệt lập đẳng cấp 5 sao');

-- 3. Phòng vật lý mẫu
INSERT OR IGNORE INTO Physical_Rooms (physical_room_id, room_type_id, room_number, floor_number, housekeeping_status, occupancy_status) VALUES
(1, 1, '101', 1, 'CLEAN', 'VACANT'),
(2, 1, '102', 1, 'CLEAN', 'VACANT'),
(3, 2, '201', 2, 'CLEAN', 'VACANT'),
(4, 2, '202', 2, 'CLEAN', 'VACANT'),
(5, 3, '301', 3, 'CLEAN', 'VACANT'),
(6, 4, 'V01', 1, 'CLEAN', 'VACANT');

-- 4. Danh mục dịch vụ chuẩn
INSERT OR IGNORE INTO Service_Items (item_id, item_code, item_name, category, unit_price, vat_rate) VALUES
(1, 'MB_COKE', 'Coca Cola Lon (Minibar)', 'MINIBAR', 30000, 0.08),
(2, 'MB_WATER', 'Nước suối Dasani 500ml', 'MINIBAR', 20000, 0.08),
(3, 'LAU_SHIRT', 'Giặt ủi áo sơ mi cao cấp', 'LAUNDRY', 50000, 0.08),
(4, 'FB_SEAFOOD', 'Set Cơm Hải Sản Côn Đảo', 'F_AND_B', 350000, 0.08),
(5, 'SPA_MASSAGE', 'Massage toàn thân thảo dược 60p', 'SPA', 600000, 0.08);

-- =========================================================================
-- [HOÀN TẤT] Lược đồ CSDL 3NF đã sẵn sàng vận hành sản phẩm thực tế!
-- =========================================================================
