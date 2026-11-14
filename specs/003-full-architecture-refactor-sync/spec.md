# Feature Specification: Full 4-Tier Architecture Refactoring & OOAD Synchronization

**Feature Branch / Directory**: `003-full-architecture-refactor-sync`  
**Created**: 2026-11-05  
**Status**: Ready for Implementation Planning  
**Input Source**: `C:\Users\Cuong\Downloads\Tong_Hop_Bieu_Do.drawio` & Refined Sequence Diagrams SD-01 to SD-05  
**Target Repository**: `C:\HocC\Project_Booking - Sao chép`

---

## 1. Executive Summary & Objective

Tái cấu trúc và chuẩn hóa toàn diện mã nguồn hệ thống *Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo* trên **4 tầng kiến trúc**:
1. **Tầng Cơ sở Dữ liệu (Database Tier - 3NF):** Triệt tiêu hoàn toàn God Table `New_Bookings`, chuẩn hóa 15 bảng 3NF, hợp nhất Identity, cơ chế khóa phòng `tbl_Room_Hold_Locks`, và lưu vết giao dịch `tbl_Payments` (`tbl_Payment_Transactions`).
2. **Tầng Mô hình Đối tượng (Domain Entities / Models Tier):** Xây dựng 15 Entity Classes độc lập, kiểu dữ liệu chặt chẽ khớp 100% với Domain Class Diagram (Trang-13) và ERD.
3. **Tầng Dịch vụ Nghiệp vụ (Service Layer Tier):** Bóc tách logic nghiệp vụ từ Fat Routes (1.200 dòng) thành 6 Service Classes chuyên biệt (`RoomHoldLockService`, `PaymentService`, `RoomAllocationService`, `ServiceConsumptionService`, `CheckoutSettlementService`, `HousekeepingService`).
4. **Tầng Giao diện & Điều khiển (UI & Route Handlers Tier):** Mỏng hóa Route Handlers (< 20 lines/endpoint), tích hợp đồng hồ đếm ngược 15:00 và Polling kết quả thanh toán trên B2C, Modal Check-in/Check-out gán phòng theo đêm, và giao diện Buồng phòng di động.

---

## 2. User Scenarios & Prioritized User Stories

### User Story 1 (Priority P1): Chuẩn hóa CSDL 3NF & Di chuyển Dữ liệu (Database Schema & Migration)
* **Là** Quản trị viên hệ thống và Nhà phát triển backend,
* **Tôi muốn** CSDL được chuẩn hóa thành 15 bảng theo chuẩn 3NF, loại bỏ God Table `New_Bookings` và chuỗi CSV `selected_nights`,
* **Để** Đảm bảo tính toàn vẹn dữ liệu (Data Integrity), hỗ trợ khóa ngoại Nullable cho khách vãng lai, và triệt tiêu rủi ro tranh chấp dữ liệu phòng.
* **Tiêu chí chấp nhận (Acceptance Criteria):**
  1. Script `database/schema_saigon_condao_3nf.sql` khởi tạo thành công 15 bảng: `tbl_Roles`, `tbl_Staff_Profiles`, `tbl_Accounts`, `tbl_Customer_Profiles`, `tbl_Room_Hold_Locks`, `tbl_Room_Types`, `tbl_Physical_Rooms`, `tbl_Housekeeping_Logs`, `tbl_Maintenance_Tickets`, `tbl_Bookings`, `tbl_Booking_Nights`, `tbl_Service_Items`, `tbl_Service_Consumptions`, `tbl_Invoices`, `tbl_Payments`.
  2. Không còn bất kỳ cột nào chứa dữ liệu gộp dạng CSV (`selected_nights`) hoặc tiền tệ kép (`_cents`).
  3. Script migration `db/migrate_data.py` chuyển đổi dữ liệu lịch sử từ DB cũ sang 15 bảng mới mà không mất mát thông tin.

### User Story 2 (Priority P1): Xây dựng Mô hình Đối tượng Thực thể (Domain Entities Layer)
* **Là** Lập trình viên Backend,
* **Tôi muốn** Có các lớp Model hướng đối tượng trong thư mục `.BackEnd/models/` phản ánh chính xác cấu trúc thực thể trong Domain Class Diagram,
* **Để** Cung cấp các phương thức thao tác dữ liệu an toàn, đúng cú pháp OOP và nghiệp vụ khách sạn.
* **Tiêu chí chấp nhận (Acceptance Criteria):**
  1. Có đủ 15 model tương ứng với 15 bảng: `Account`, `CustomerProfile`, `StaffProfile`, `Role`, `RoomType`, `PhysicalRoom`, `RoomHoldLock`, `Booking`, `BookingNight`, `ServiceItem`, `ServiceConsumption`, `FolioInvoice`, `PaymentTransaction`, `HousekeepingLog`, `MaintenanceTicket`.
  2. Các phương thức nghiệp vụ cốt lõi được định nghĩa sẵn trong Entity: `RoomHoldLock.is_expired()`, `PhysicalRoom.mark_dirty()`, `PhysicalRoom.mark_occupied()`, `BookingNight.assign_room()`, `Booking.calculate_total_nights()`.

### User Story 3 (Priority P1): Xây dựng Tầng Dịch vụ Nghiệp vụ (Service Layer & Concurrency)
* **Là** Khách hàng và Lễ tân khách sạn,
* **Tôi muốn** Các quy trình nghiệp vụ (Đặt phòng online, Khóa phòng 15P, Check-in, Tiêu dùng dịch vụ, Check-out, Dọn phòng) được điều phối bởi các Service chuyên trách,
* **Để** Đảm bảo tính đúng đắn của giao dịch tài chính và ngăn chặn hiện tượng đặt trùng phòng (Overbooking).
* **Tiêu chí chấp nhận (Acceptance Criteria):**
  1. `RoomHoldLockService`: Cung cấp hàm `create_hold_lock(room_type_id, qty, session_id, ttl_minutes=15)` kiểm tra nguyên tử tồn kho `[Total - Sold - ActiveLocks]`.
  2. `PaymentService`: Tạo mã VietQR, tiếp nhận Webhook/IPN bất đồng bộ, xác thực chữ ký số, lưu `PaymentTransaction`, và hỗ trợ API Polling trạng thái thanh toán.
  3. `RoomAllocationService`: Triển khai thuật toán tìm kiếm và đề xuất các phòng vật lý có trạng thái `CLEAN & VACANT`.
  4. `ServiceConsumptionService`: Ghi nhận tiêu dùng dịch vụ minibar/giặt ủi vào phòng đang lưu trú (`CHECKED_IN`), tự động tính thuế VAT.
  5. `CheckoutSettlementService`: Tính toán chính xác công nợ: $\text{Tổng thanh toán} = \text{Tiền phòng} + \text{Dịch vụ phát sinh} - \text{Tiền cọc}$, xuất hóa đơn VAT, và tự động đổi phòng sang `DIRTY`.
  6. `HousekeepingService`: Cập nhật trạng thái dọn dẹp (`DIRTY` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `CLEAN`), lưu `HousekeepingLog`, và tự động khóa phòng sang `MAINTENANCE` kèm sinh `MaintenanceTicket`.

### User Story 4 (Priority P2): Dọn dẹp & Mỏng hóa Controller (Slenderizing Routes)
* **Là** Lập trình viên bảo trì mã nguồn,
* **Tôi muốn** File `booking_routes.py` và các route handlers khác chỉ đóng vai trò Boundary HTTP handler (< 20 dòng mỗi endpoint),
* **Để** Code dễ đọc, dễ kiểm thử tự động, và tuân thủ nguyên lý Separation of Concerns.
* **Tiêu chí chấp nhận (Acceptance Criteria):**
  1. Các câu lệnh raw SQL trong file routes được loại bỏ 100%.
  2. File `booking_routes.py` giảm dung lượng từ 1.200 dòng xuống dưới 180 dòng.

### User Story 5 (Priority P2): Tích hợp & Kiểm thử Giao diện Người dùng (UI Layer Integration)
* **Là** Khách hàng B2C và Nhân viên khách sạn,
* **Tôi muốn** Giao diện web hiển thị đồng bộ với luồng nghiệp vụ trên biểu đồ trình tự (SD-01 đến SD-05),
* **Để** Trải nghiệm người dùng mượt mà, không gặp hiện tượng bị "hẫng" hay đứng trang.
* **Tiêu chí chấp nhận (Acceptance Criteria):**
  1. Giao diện Đặt phòng: Hiển thị đồng hồ đếm ngược 15:00, tự động Polling trạng thái Webhook để chuyển trang Voucher xác nhận (PNR) khi thanh toán thành công.
  2. Sơ đồ Gantt Lễ tân: Tách riêng Sơ đồ tổng quan và Modal Check-in; cập nhật màu trạng thái phòng theo thời gian thực (Xanh lá: Sạch, Đỏ: Đang ở / Chờ dọn, Vàng: Đang dọn, Xám: Bảo trì).
  3. Chạy toàn bộ bộ test `pytest` xác nhận các endpoint API và giao diện hoạt động trơn tru.

---

## 3. Data Flow & Entity Relationship Mapping

```
[tbl_Accounts] 1 ──── 0..1 [tbl_Customer_Profiles]
              1 ──── 0..1 [tbl_Staff_Profiles] (role_id FK -> tbl_Roles)

[tbl_Room_Types] 1 ──── * [tbl_Physical_Rooms]
                 1 ──── * [tbl_Room_Hold_Locks] (hold 15 mins)
                 1 ──── * [tbl_Bookings] (customer_id FK Nullable)

[tbl_Bookings] 1 ──── * [tbl_Booking_Nights] (assigned to tbl_Physical_Rooms)
               1 ──── * [tbl_Payments] (PaymentTransaction)
               1 ──── 0..1 [tbl_Invoices] (VAT financial invoice at checkout)
               1 ──── * [tbl_Service_Consumptions] (service charges during stay)

[tbl_Physical_Rooms] 1 ──── * [tbl_Housekeeping_Logs]
                     1 ──── * [tbl_Maintenance_Tickets]
```

---

## 4. Non-Functional Requirements & Constraints

1. **Tuân thủ OMG UML 2.5 & Kiến trúc BCE:** Tên gọi các class, service và phương thức phải phản ánh đúng nhãn trên biểu đồ `Tong_Hop_Bieu_Do.drawio`.
2. **ACID Transaction:** Mọi thao tác đặt phòng, cấn trừ cọc, hoàn tiền và chuyển trạng thái phòng phải được bao bọc trong transaction của cơ sở dữ liệu.
3. **Hiệu năng & Trải nghiệm:** API Polling kiểm tra trạng thái thanh toán phải đáp ứng dưới 100ms, không làm nghẽn kết nối SQLite.
