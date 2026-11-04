# Tasks: Hotel System Architectural Refactoring & 3NF Migration

**Input**: Design documents from `/specs/001-hotel-system-refactor/` (`spec.md`, `plan.md`)
**Target Workspace**: `C:\HocC\Project_Booking - Sao chép\`
**Status**: 100% Completed & Verified

---

## Phase 1: Foundational Database 3NF Migration

**Purpose**: Chuẩn hóa toàn bộ cấu trúc dữ liệu SQLite sang 3NF trước khi sửa logic ứng dụng

- [x] T001 Tạo bản sao lưu an toàn CSDL cũ: `C:\HocC\Project_Booking - Sao chép\.BackEnd\db\HotelBooking_Pre_3NF_Migration.db`
- [x] T002 Tạo file DDL `schema_3nf.sql` định nghĩa chuẩn xác 15 bảng theo ERD 3NF và Class Diagram (bao gồm `RoomHoldLocks`, `BookingNights`, `RoomTypes`, `PhysicalRooms`, `Bookings`, `FolioInvoices`, `PaymentTransactions`, `ServiceConsumptions`)
- [x] T003 Viết và thực thi script ETL `migrate_db_3nf.py`: Đổi `Booking_Nights.physical_room_id` thành Nullable FK, tạo bảng `RoomHoldLocks`, bảo toàn nguyên vẹn 26.955 bản ghi lịch sử
- [x] T004 Xây dựng cấu trúc kết nối SQLite connection với `PRAGMA foreign_keys = ON;` và `PRAGMA journal_mode = WAL;`

---

## Phase 2: User Story 1 - Khóa giữ chỗ & Đặt phòng trực tuyến B2C (Priority: P1)

**Goal**: Khách đặt online chọn Loại phòng (RoomType), hệ thống tạo Khóa giữ chỗ 15 phút, khi thanh toán tạo Booking và sinh các BookingNight (chưa gán phòng vật lý).

- [x] T005 [P] [US1] Xây dựng Service `services/room_lock_service.py`:
  - `get_available_inventory_by_room_type(cursor, room_type_id, arrival_date, departure_date)`: Tính tồn kho khả dụng = `totalInventory - (soldNights + activeLocks)`
  - `create_room_hold_lock(room_type_id, session_id, arrival_date, departure_date, quantity, ttl_minutes=15)`: Tạo khóa giữ chỗ tạm thời
  - `cleanup_expired_room_hold_locks()`: Tự động cập nhật khóa hết hạn
- [x] T006 [US1] Nâng cấp Service `services/booking_service.py`:
  - `create_online_booking`: Hỗ trợ đặt phòng không cần gán phòng vật lý trước (`physical_room_id = NULL`), chuyển đổi trạng thái Lock thành `status = 'converted'`, tạo các bản ghi `Booking_Nights` với `physical_room_id = NULL`
- [x] T007 [US1] Bổ sung API Controller trong `routes/booking_routes.py`:
  - Endpoint `POST /api/rooms/hold`: Gọi `room_lock_service.create_room_hold_lock()`
  - Endpoint `POST /api/bookings`: Hỗ trợ luồng B2C chuẩn (loại bỏ bắt buộc `physical_room_id`)

---

## Phase 3: User Story 2 - Lễ tân Check-in & Gán phòng động tại quầy (Priority: P1)

**Goal**: Lễ tân mở danh sách phòng sạch (`Clean`), gọi hàm `ganPhong(room)` để gán phòng vật lý vào `BookingNight` khi khách đến nhận phòng.

- [x] T008 [P] [US2] Xây dựng Service mới `services/checkin_service.py`:
  - `get_assignable_clean_rooms(booking_id)`: Trả về danh sách phòng vật lý đang `Clean` và chưa bị gán trong các đêm đó
  - `assign_room_and_checkin(booking_id, physical_room_id, staff_user_id)`: Gán `physical_room_id` vào tất cả các `Booking_Nights` của đơn, chuyển trạng thái `Physical_Room` sang `Occupied`, chuyển trạng thái `Booking_Master` sang `Checked-In`
- [x] T009 [US2] Bổ sung Endpoint Lễ tân trong `routes/booking_routes.py`:
  - Endpoint `GET /api/frontdesk/assignable-rooms/<int:booking_id>`: Lấy danh sách phòng sạch khả dụng
  - Endpoint `POST /api/frontdesk/assign-and-checkin`: Thực hiện gán phòng động và xác nhận Check-in

---

## Phase 4: User Story 3 - Tiếp nhận khách vãng lai Walk-in (Priority: P2)

**Goal**: Lễ tân đặt phòng trực tiếp cho khách tại quầy mà không sinh tài khoản ảo `{phone}@walkin.local` hay tài khoản rác trong bảng `Accounts`.

- [x] T010 [US3] Khẳng định và chuẩn hóa hàm `create_walkin_booking()` trong `services/booking_service.py`:
  - Nhập trực tiếp `guest_name`, `guest_phone`, thiết lập `customer_id = NULL`
  - Đảm bảo 0% tài khoản ảo rác sinh ra trong bảng `Accounts`
- [x] T011 [US3] Endpoint `POST /api/bookings/walkin` hoạt động hoàn hảo

---

## Phase 5: User Story 4 - Tiêu dùng Dịch vụ & Quyết toán Check-out (Priority: P2)

**Goal**: Ghi nhận minibar/dịch vụ vào `ServiceConsumption` (Extra_Services), tổng hợp quyết toán hóa đơn `FolioInvoice`, cấn trừ cọc, in hóa đơn và chuyển phòng sang `Dirty`.

- [x] T012 [P] [US4] Hoàn thiện Service `services/checkout_service.py`:
  - `get_checkout_statement(booking_id)`: Bảng kê chi phí phòng, dịch vụ, trừ cọc
  - `process_checkout(booking_id, payment_method)`: Cập nhật hóa đơn `Invoices`, chuyển trạng thái Booking `Checked-Out`
- [x] T013 [US4] Endpoint `PUT /api/bookings/<int:booking_id>/checkout` trong `routes/booking_routes.py` hoạt động thông suốt

---

## Phase 6: Slenderizing Routes, Frontend Compatibility & Verification

**Purpose**: Làm sạch hoàn toàn các file route, kiểm thử toàn vẹn hệ thống

- [x] T014 Tối giản hóa toàn diện `routes/booking_routes.py`: Không chứa bất kỳ dòng SQL thô nào, chỉ gọi Service, bắt Exception nghiệp vụ chuẩn
- [x] T015 Đồng bộ các định dạng tham số (`checkin_date` / `arrival_date`, `checkout_date` / `departure_date`) đảm bảo Frontend Port 5001 tương thích 100%
- [x] T016 Xây dựng và thực thi bộ kiểm thử tự động `test_refactored_system.py`: Xác nhận 100% cả 4 kịch bản sống còn đều vượt qua (100% PASS)!
