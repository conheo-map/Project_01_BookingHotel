# Implementation Plan: Hotel System Architectural Refactoring & 3NF Migration

**Branch**: `001-hotel-system-refactor` | **Date**: 2026-11-04 | **Spec**: [specs/001-hotel-system-refactor/spec.md](spec.md)

---

## 1. Summary

Kế hoạch tái cấu trúc mã nguồn Backend và Cơ sở dữ liệu của dự án Khách sạn Sài Gòn - Côn Đảo nhằm hiện thực hóa 100% các yêu cầu từ `spec.md`:
* Chuyển đổi mô hình CSDL từ bảng phẳng `New_Bookings` sang lược đồ chuẩn hóa 3NF khớp hoàn toàn với ERD 3NF và Class Diagram.
* Bổ sung cơ chế Khóa giữ chỗ tạm thời (`RoomHoldLocks`) với TTL 15 phút.
* Phân rã đơn đặt phòng thành danh sách đêm lưu trú (`BookingNights`) để phục vụ gán phòng động tại quầy và giá biến động theo ngày.
* Tái cấu trúc các route khổng lồ 1.200 dòng thành mô hình 3 tầng (**Routes $\rightarrow$ Services $\rightarrow$ Repositories/Models**).

---

## 2. Technical Context

* **Ngôn ngữ & Phiên bản**: Python 3.10+ / 3.13
* **Web Framework**: Flask (Blueprint-based architecture)
* **Cơ sở dữ liệu**: SQLite 3 (WAL mode: `PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;`)
* **Frontend**: HTML5, Jinja2, Bootstrap 5.3, Vanilla JS / GSAP
* **Primary Dependencies**: `Flask`, `Flask-Session`, `werkzeug`, `sqlite3`
* **Target Ports**: Backend API (Port 5000), Frontend Client (Port 5001)

---

## 3. Architecture & Project Structure

Mã nguồn được cấu trúc theo mô hình phân tầng hướng đối tượng chuẩn:

```text
C:\HocC\Project_Booking - Sao chép\
├── .BackEnd/
│   ├── app.py                      # Flask App Factory & Route Blueprints
│   ├── config.py                   # Cấu hình môi trường & DB Path
│   ├── db/
│   │   ├── HotelBooking.db         # File CSDL SQLite chính thức chuẩn 3NF
│   │   ├── HotelBooking.db.bak     # Bản sao lưu dự phòng CSDL cũ
│   │   ├── schema_3nf.sql          # Lược đồ DDL 15 bảng chuẩn hóa 3NF
│   │   └── migrate_to_3nf.py       # Script ETL chuyển dữ liệu từ cũ sang 3NF
│   ├── models/                     # Tầng Thực thể (Domain Entities)
│   │   ├── account.py              # Account, CustomerProfile, StaffProfile, Role
│   │   ├── room.py                 # RoomType, PhysicalRoom
│   │   ├── booking.py              # Booking, BookingNight, RoomHoldLock
│   │   └── finance.py              # FolioInvoice, PaymentTransaction, ServiceConsumption
│   ├── repositories/               # Tầng Truy xuất CSDL (Data Access Layer)
│   │   ├── base_repository.py      # SQLite Connection Context Manager & Transactions
│   │   ├── room_repository.py      # Truy vấn tồn kho, phòng vật lý sạch, lock
│   │   └── booking_repository.py   # CRUD Booking, BookingNight, Invoices
│   ├── services/                   # Tầng Nghiệp vụ Cốt lõi (Service Layer)
│   │   ├── room_lock_service.py    # Quản lý phiên giữ chỗ 15m (Create, Expire, Release)
│   │   ├── pricing_service.py      # Tính tiền theo đêm, phụ thu, áp mã giảm giá
│   │   ├── booking_service.py      # Điều phối đặt phòng online B2C & Walk-in
│   │   ├── checkin_service.py      # Lễ tân gán phòng động ganPhong() & Check-in
│   │   └── checkout_service.py     # Quyết toán hóa đơn, minibar, đổi trạng thái Dirty
│   └── routes/                     # Tầng Biên mỏng (Slender HTTP Controllers < 150 dòng)
│       ├── auth_routes.py          # Đăng nhập, phân quyền RBAC
│       ├── room_routes.py          # Tra cứu phòng trống & danh mục
│       ├── booking_routes.py       # API tạo lock, xác nhận booking, hủy phòng
│       └── manager_routes.py       # Nghiệp vụ Lễ tân: Check-in, Gán phòng, Check-out
└── FrontEnd/                       # Giao diện người dùng (Port 5001)
    ├── services/api.py             # Client HTTP gọi sang Backend Port 5000
    ├── templates/                  # Jinja2 Views
    └── static/                     # CSS, JS, Images
```

---

## 4. Phase-by-Phase Execution Plan

### Phase 1: Database Migration sang 3NF (DDL & ETL)
1. Tạo bản sao lưu an toàn `HotelBooking_Backup_Original.db`.
2. Tạo file `schema_3nf.sql` định nghĩa chuẩn xác 15 bảng:
   * `Roles`, `Accounts`, `CustomerProfiles`, `StaffProfiles`.
   * `RoomTypes`, `PhysicalRooms`, `RoomHoldLocks`.
   * `Bookings`, `BookingNights`.
   * `ServiceItems`, `ServiceConsumptions`, `FolioInvoices`, `PaymentTransactions`.
   * `HousekeepingLogs`, `MaintenanceTickets`.
3. Viết script ETL `migrate_to_3nf.py`: Đọc dữ liệu từ bảng cũ `New_Bookings`, `Rooms`, `Users` và ánh xạ sạch sẽ sang 15 bảng 3NF.

### Phase 2: Core Service Layer Implementation
1. `services/room_lock_service.py`: Hàm `create_hold_lock(room_type_id, qty, session_id, ttl_minutes=15)` và `check_availability(room_type_id, checkin, checkout)`.
2. `services/booking_service.py`: Hàm `process_b2c_booking(lock_id, customer_data, payment_info)` - chuyển Lock thành Booking và sinh các bản ghi `BookingNight` (chưa gán phòng).
3. `services/checkin_service.py`: Hàm `get_available_clean_rooms(room_type_id, dates)` và `assign_room_and_checkin(booking_id, room_number_or_id)`.
4. `services/checkout_service.py`: Hàm `summarize_folio(booking_id)` và `complete_checkout(booking_id, payment_data)`.

### Phase 3: Route Slenderizing (Bóc tách Fat Routes)
1. Viết lại `routes/booking_routes.py`: Loại bỏ toàn bộ SQL thô, chỉ gọi `booking_service` và `room_lock_service`.
2. Viết lại các endpoint lễ tân trong `routes/manager_routes.py`: Gọi `checkin_service` và `checkout_service`.

### Phase 4: Frontend API Compatibility & Verification
1. Đảm bảo `FrontEnd/services/api.py` gửi đúng payload và nhận đúng cấu trúc JSON mới.
2. Kiểm thử tự động (Unit / Integration Tests) và kiểm thử thủ công 4 kịch bản người dùng.
