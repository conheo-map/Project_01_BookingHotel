# Tasks: Hotel System Architectural Refactoring & 3NF Migration

**Input**: Design documents from `/specs/001-hotel-system-refactor/` (`spec.md`, `plan.md`)
**Target Workspace**: `C:\HocC\Project_Booking - Sao chép\`

---

## Phase 1: Foundational Database 3NF Migration

**Purpose**: Chuẩn hóa toàn bộ cấu trúc dữ liệu SQLite sang 3NF trước khi sửa logic ứng dụng

- [ ] T001 Tạo bản sao lưu an toàn CSDL cũ: `C:\HocC\Project_Booking - Sao chép\.BackEnd\db\HotelBooking_Backup_Original.db`
- [ ] T002 Tạo file DDL `schema_3nf.sql` định nghĩa chuẩn xác 15 bảng theo ERD 3NF và Class Diagram (bao gồm `RoomHoldLocks`, `BookingNights`, `RoomTypes`, `PhysicalRooms`, `Bookings`, `FolioInvoices`, `PaymentTransactions`, `ServiceConsumptions`)
- [ ] T003 Viết và thực thi script ETL `migrate_to_3nf.py`: Đọc dữ liệu từ bảng cũ `New_Bookings`, bóc tách thành `Bookings` + `BookingNights` + `FolioInvoices`, chuyển đổi `Users` thành `Accounts` + `CustomerProfiles` / `StaffProfiles`
- [ ] T004 Xây dựng `repositories/base_repository.py`: Quản lý context manager SQLite connection với `PRAGMA foreign_keys = ON;` và `PRAGMA journal_mode = WAL;`

---

## Phase 2: User Story 1 - Khóa giữ chỗ & Đặt phòng trực tuyến B2C (Priority: P1)

**Goal**: Khách đặt online chọn Loại phòng (RoomType), hệ thống tạo Khóa giữ chỗ 15 phút, khi thanh toán tạo Booking và sinh các BookingNight (chưa gán phòng vật lý).

- [ ] T005 [P] [US1] Xây dựng Service `services/room_lock_service.py`:
  - `check_availability(room_type_id, arrival_date, departure_date)`: Tính tồn kho khả dụng = `totalInventory - (soldNights + activeLocks)`
  - `create_hold_lock(room_type_id, quantity, session_id, ttl_minutes=15)`: Tạo khóa giữ chỗ tạm thời
  - `release_expired_locks()`: Tự động dọn dẹp khóa hết hạn
- [ ] T006 [US1] Xây dựng Service `services/booking_service.py`:
  - `create_booking_from_lock(lock_id, guest_info, deposit_amount)`: Chuyển Lock thành `Bookings` + tạo các bản ghi `BookingNights` (với `physicalRoomId = NULL`)
- [ ] T007 [US1] Viết lại API Controller trong `routes/booking_routes.py`:
  - Endpoint `POST /api/rooms/hold`: Gọi `room_lock_service.create_hold_lock()`
  - Endpoint `POST /api/bookings/confirm`: Gọi `booking_service.create_booking_from_lock()`
  - Loại bỏ hoàn toàn 100% các câu lệnh gán cứng số phòng vật lý cũ

---

## Phase 3: User Story 2 - Lễ tân Check-in & Gán phòng động tại quầy (Priority: P1)

**Goal**: Lễ tân mở danh sách phòng sạch (`Clean`), gọi hàm `ganPhong(room)` để gán phòng vật lý vào `BookingNight` khi khách đến nhận phòng.

- [ ] T008 [P] [US2] Xây dựng Service `services/checkin_service.py`:
  - `get_assignable_clean_rooms(room_type_id, arrival_date, departure_date)`: Trả về danh sách phòng vật lý đang `Clean` và chưa bị gán trong các đêm đó
  - `assign_room_and_checkin(booking_id, physical_room_id)`: Gán `physicalRoomId` vào tất cả các `BookingNights` của đơn, chuyển trạng thái `PhysicalRoom` sang `Occupied`, chuyển trạng thái `Booking` sang `CheckedIn`
- [ ] T009 [US2] Viết lại Endpoint Lễ tân trong `routes/manager_routes.py`:
  - Endpoint `GET /api/frontdesk/assignable-rooms`: Lấy danh sách phòng sạch khả dụng
  - Endpoint `POST /api/frontdesk/check-in`: Thực hiện gán phòng động và xác nhận Check-in

---

## Phase 4: User Story 3 - Tiếp nhận khách vãng lai Walk-in (Priority: P2)

**Goal**: Lễ tân đặt phòng trực tiếp cho khách tại quầy mà không sinh tài khoản ảo `{phone}@walkin.local` hay tài khoản rác trong bảng `Accounts`.

- [ ] T010 [US3] Bổ sung hàm `create_walkin_booking()` trong `services/booking_service.py`:
  - Nhập trực tiếp `guestName`, `guestPhone`, thiết lập `customerId = NULL`
  - Cho phép chọn phòng vật lý trực tiếp và chuyển ngay sang trạng thái `CheckedIn`
- [ ] T011 [US3] Cập nhật Endpoint `POST /api/frontdesk/walk-in` trong `routes/manager_routes.py`

---

## Phase 5: User Story 4 - Tiêu dùng Dịch vụ & Quyết toán Check-out (Priority: P2)

**Goal**: Ghi nhận minibar/dịch vụ vào `ServiceConsumption`, tổng hợp quyết toán hóa đơn `FolioInvoice`, cấn trừ cọc, in hóa đơn và chuyển phòng sang `Dirty`.

- [ ] T012 [P] [US4] Xây dựng Service `services/checkout_service.py`:
  - `add_service_consumption(booking_id, item_id, quantity)`: Ghi nhận tiêu dùng dịch vụ
  - `calculate_folio(booking_id)`: Tính tổng tiền phòng, tiền dịch vụ, trừ cọc, tính VAT, ra số tiền cuối cùng `finalAmount`
  - `complete_checkout(booking_id, payment_data)`: Lưu `PaymentTransaction`, chuyển trạng thái Booking `CheckedOut`, đổi trạng thái `PhysicalRoom` sang `Dirty`
- [ ] T013 [US4] Cập nhật Endpoint `POST /api/frontdesk/checkout` trong `routes/manager_routes.py`

---

## Phase 6: Slenderizing Routes, Frontend Compatibility & Verification

**Purpose**: Làm sạch hoàn toàn các file route, kiểm thử toàn vẹn hệ thống

- [ ] T014 Tối giản hóa toàn diện `routes/booking_routes.py` và `routes/manager_routes.py`: Đảm bảo mỗi endpoint không vượt quá 20 dòng, chuyển toàn bộ logic nghiệp vụ về `services/`
- [ ] T015 Rà soát `FrontEnd/services/api.py`: Đảm bảo payload gửi lên và phản hồi JSON trả về khớp với các trường mới (VND format, snake_case/camelCase)
- [ ] T016 Chạy kiểm thử tự động xác nhận CSDL 3NF và kiểm thử luồng end-to-end trên 2 cổng: Backend (Port 5000) và Frontend (Port 5001)
