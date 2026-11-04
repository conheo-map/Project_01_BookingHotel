# Feature Specification: Hotel System Architectural Refactoring & 3NF Migration

**Feature Branch**: `001-hotel-system-refactor`
**Created**: 2026-11-04
**Status**: Approved / In-Planning
**Feature Directory**: `specs/001-hotel-system-refactor`

---

## Executive Summary & Scope

Dự án tái cấu trúc toàn diện mã nguồn và cơ sở dữ liệu Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Python Flask, SQLite, Jinja2) nhằm:
1. Đồng bộ 100% mã nguồn thực tế khớp với **Biểu đồ Lớp Lĩnh vực (Domain Class Diagram UML 2.x)** và **Lược đồ CSDL 3NF (ERD 3NF)** đã được phê duyệt.
2. Khai tử hoàn toàn Anti-Pattern "God Table" `New_Bookings`, bóc tách thành các bảng 3NF chuyên biệt (`RoomHoldLocks`, `BookingNights`, `RoomTypes`, `PhysicalRooms`, `FolioInvoices`, `PaymentTransactions`).
3. Sửa triệt để luồng đặt phòng trực tuyến (B2C): Không gán cứng phòng vật lý khi đặt online, áp dụng cơ chế Khóa giữ chỗ tạm thời (TTL 15 phút) chống Race condition / Overbooking.
4. Khai tử tài khoản ảo "Walk-in", hiện thực hóa hàm gán phòng động (`ganPhong(room)`) khi Lễ tân Check-in tại quầy.
5. Tái cấu trúc mã nguồn theo kiến trúc 3 tầng chuẩn (**Controllers / Routes $\rightarrow$ Service Layer $\rightarrow$ Models / Repositories**), giảm tải các file route khổng lồ từ 1.200 dòng xuống dưới 150 dòng.

---

## User Scenarios & Testing (Prioritized User Journeys)

### User Story 1 - Khóa giữ chỗ & Đặt phòng trực tuyến B2C an toàn (Priority: P1)

Khách hàng truy cập website đặt phòng, chọn Loại phòng (RoomType), số lượng phòng và khoảng thời gian lưu trú (từ ngày đến ngày). Hệ thống tính toán tồn kho khả dụng theo công thức:
$$\text{Available} = \text{TotalInventory} - (\text{SoldNights} + \text{ActiveLocks})$$
Nếu còn phòng, hệ thống lập tức tạo bản ghi khóa giữ chỗ tạm thời `RoomHoldLock` trong **15 phút**. Trong 15 phút này, các khách khác không thể chiếm mất số lượng phòng này. Khách thanh toán cọc thành công, hệ thống chuyển đổi Lock thành Đơn đặt phòng `Booking` chính thức và tự động phân rã thành các đêm lưu trú `BookingNight` (chưa gán số phòng vật lý cụ thể).

* **Independent Test**: Chạy 2 phiên duyệt web đồng thời cùng đặt loại phòng có tồn kho chỉ còn 1 phòng; người thứ nhất bấm đặt phải tạo được khóa giữ chỗ 15 phút, người thứ hai sẽ nhận thông báo hết phòng. Khi người thứ nhất thanh toán thành công, `Booking` được tạo với các `BookingNight` tương ứng.
* **Acceptance Scenarios**:
  1. **Given** Loại phòng Deluxe còn 1 phòng trống ngày 10/11 - 12/11 (2 đêm), **When** Khách hàng A bấm "Xác nhận đặt phòng", **Then** Hệ thống tạo 1 bản ghi `RoomHoldLock` với `expiresAt = now + 15m`, tồn kho khả dụng trả về 0.
  2. **Given** Khách hàng B tìm kiếm cùng loại phòng trong thời gian khóa, **Then** Hệ thống báo loại phòng tạm hết.
  3. **Given** Khách hàng A thanh toán cọc thành công trong 15 phút, **Then** `RoomHoldLock` được giải phóng, `Booking` được tạo (trạng thái `Confirmed`), sinh 2 bản ghi `BookingNight` (stayDate: 10/11, 11/11), `physicalRoomId` là `NULL`.
  4. **Given** Khách hàng A không thanh toán sau 15 phút, **Then** Cron/Worker tự động giải phóng lock, trả lại tồn kho khả dụng cho khách khác.

---

### User Story 2 - Lễ tân Check-in & Gán phòng động tại quầy (Priority: P1)

Khi khách hàng đến khách sạn xuất trình CCCD hoặc mã PNR, Lễ tân thực hiện thủ tục Check-in. Hệ thống hiển thị danh sách các phòng vật lý (`PhysicalRoom`) thuộc loại phòng đã đặt, có trạng thái dọn dẹp là **Sạch (`Clean`)** và chưa bị gán trong các đêm đó. Lễ tân chọn phòng cụ thể (ví dụ: Phòng 204) và nhấn "Gán phòng & Check-in", hệ thống cập nhật `BookingNight.physicalRoomId` và chuyển trạng thái phòng sang `Occupied`.

* **Independent Test**: Tạo một Booking đã thanh toán nhưng chưa có phòng. Vào giao diện Lễ tân, chọn gán một phòng vật lý sạch; kiểm tra DB xem `BookingNight` đã được gán `physicalRoomId` và trạng thái `PhysicalRoom` chuyển thành `Occupied`.
* **Acceptance Scenarios**:
  1. **Given** Đơn đặt phòng mã PNR `SGCD-8899` có 2 đêm lưu trú chưa gán phòng, **When** Lễ tân mở giao diện Check-in, **Then** Hệ thống chỉ liệt kê các phòng vật lý thuộc loại phòng đó có trạng thái `Clean` và khả dụng.
  2. **Given** Lễ tân chọn phòng 204 và nhấn "Gán phòng", **Then** Cả 2 bản ghi `BookingNight` được gán `physicalRoomId = 204`, trạng thái `PhysicalRoom 204` chuyển thành `Occupied`, trạng thái Booking chuyển thành `CheckedIn`.

---

### User Story 3 - Lễ tân tiếp nhận khách vãng lai (Walk-in) không cần tài khoản (Priority: P2)

Khách vãng lai đến quầy lễ tân đặt phòng trực tiếp không có tài khoản thành viên trên hệ thống. Lễ tân chỉ cần nhập Họ tên (`guestName`) và Số điện thoại (`guestPhone`) vào biểu mẫu đặt phòng tại quầy. Hệ thống tạo đơn `Booking` với trường `customerId = NULL`, tuyệt đối không sinh email giả lập dạng `{phone}@walkin.local` hay tài khoản rác trong bảng `Accounts`.

* **Independent Test**: Lễ tân đặt phòng Walk-in tại quầy; kiểm tra bảng `Bookings` có `customer_id IS NULL`, `guest_name` và `guest_phone` lưu đúng thông tin, bảng `Accounts` không bị tăng thêm bản ghi rác.
* **Acceptance Scenarios**:
  1. **Given** Khách vãng lai Nguyễn Văn A đến quầy, **When** Lễ tân nhập tên, SĐT, chọn loại phòng và thanh toán tại quầy, **Then** Đơn đặt phòng được tạo với `customerId = NULL`, gán trực tiếp phòng vật lý sẵn sàng, xuất hóa đơn `FolioInvoice`.

---

### User Story 4 - Tiêu dùng Dịch vụ & Quyết toán Check-out xuất Hóa đơn (Priority: P2)

Trong thời gian lưu trú, khách sử dụng dịch vụ minibar / ăn uống (`ServiceItem`). Lễ tân ghi nhận tiêu dùng vào `ServiceConsumption` gắn với phòng hoặc mã Booking. Khi khách làm thủ tục Check-out, hệ thống tự động tổng hợp tiền phòng, tiền dịch vụ, cấn trừ tiền cọc (`depositDeducted`), tính thuế VAT và in hóa đơn `FolioInvoice`, đồng thời tạo giao dịch thanh toán `PaymentTransaction` và đổi trạng thái phòng sang `Dirty` (bẩn) để chờ buồng phòng dọn.

* **Acceptance Scenarios**:
  1. **Given** Khách phòng 204 gọi thêm 2 chai nước suối (20.000đ/chai), **When** Lễ tân ghi nhận dịch vụ, **Then** Bản ghi `ServiceConsumption` được tạo với `totalAmount = 40.000đ`.
  2. **Given** Khách làm thủ tục Check-out, **When** Lễ tân nhấn "Quyết toán", **Then** Hóa đơn `FolioInvoice` tổng hợp: Tiền phòng + Tiền dịch vụ - Cọc = Tiền còn lại; ghi nhận `PaymentTransaction`; phòng 204 chuyển sang `housekeepingStatus = 'Dirty'`.

---

## Functional Requirements (FR)

* **FR-001 (CSDL 3NF)**: Hệ thống MUST xóa bỏ hoàn toàn bảng `New_Bookings` và chuyển đổi sang cấu trúc chuẩn hóa 15 bảng theo Lược đồ ERD 3NF và Class Diagram.
* **FR-002 (RoomHoldLock)**: Hệ thống MUST cung cấp bảng `RoomHoldLocks` với các cột: `hold_id`, `room_type_id`, `session_id`, `quantity`, `locked_at`, `expires_at`, `status` ('active', 'expired', 'converted'). Thời gian hết hạn mặc định là 15 phút.
* **FR-003 (BookingNight)**: Hệ thống MUST phân rã mỗi đơn đặt phòng thành các bản ghi `BookingNights` tương ứng với từng ngày lưu trú: `night_id`, `booking_id`, `stay_date`, `night_price`, `physical_room_id` (NULLable), `status`.
* **FR-004 (Room Separation)**: Hệ thống MUST tách bạch rõ ràng giữa Loại phòng định danh (`RoomTypes`: basePrice, totalInventory) và Phòng vật lý cụ thể (`PhysicalRooms`: roomNumber, floorNumber, housekeepingStatus: 'Clean'|'Dirty'|'Inspecting', occupancyStatus: 'Available'|'Occupied'|'Maintenance').
* **FR-005 (B2C Inventory Check)**: Hệ thống MUST tính toán số phòng trống khả dụng theo thời gian thực trước khi cho phép giữ chỗ hoặc đặt phòng.
* **FR-006 (No Hardcoded Room on B2C)**: API đặt phòng online TUYỆT ĐỐI KHÔNG được gán `physicalRoomId` vào thời điểm khách đặt online.
* **FR-007 (Dynamic Room Assignment)**: Hệ thống MUST cung cấp hàm `ganPhong(booking_night_id, physical_room_id)` cho phép Lễ tân gán phòng động tại thời điểm Check-in.
* **FR-008 (Nullable Customer for Walk-in)**: Bảng `Bookings` MUST hỗ trợ `customer_id` NULL để phục vụ khách vãng lai không có tài khoản.
* **FR-009 (Service Layer Architecture)**: Hệ thống MUST tổ chức mã nguồn theo 3 tầng: `routes/` (Controllers mỏng), `services/` (Xử lý nghiệp vụ tập trung), `repositories/` hoặc `models/` (Truy xuất CSDL).

---

## Measurable Success Criteria

* **SC-001**: 100% dữ liệu cũ trong `HotelBooking.db` được chuyển đổi toàn vẹn sang CSDL mới chuẩn 3NF mà không bị mất mát thông tin lịch sử.
* **SC-002**: Không còn bất kỳ câu lệnh SQL thô dài dòng nào trong `routes/booking_routes.py`, độ dài file giảm từ 1.200 dòng xuống dưới 180 dòng.
* **SC-003**: 0% xảy ra lỗi trùng phòng (Overbooking) khi có 10 yêu cầu giữ chỗ đồng thời vào cùng một phòng cuối cùng.
* **SC-004**: Tất cả 4 kịch bản người dùng (B2C Booking, Lễ tân gán phòng Check-in, Khách vãng lai Walk-in, Check-out hóa đơn) chạy thông suốt trên cả Backend (Port 5000) và Frontend (Port 5001).
