---
name: hotel-system-code-refactor
description: >-
  Chuyên sâu tái cấu trúc mã nguồn (Code Refactoring & Database Migration) cho Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Python Flask, SQLite, Jinja2). Kích hoạt skill này khi cần rà soát mã nguồn, bóc tách các file route khổng lồ (Fat Routes 1.200 dòng) thành Service Layer, chuẩn hóa CSDL 3NF (tách God Table New_Bookings, hợp nhất Identity), fix lỗi Walk-in dummy account, và đảm bảo hệ thống chạy mượt mà trước khi lập hồ sơ PTTKHT.
---

# Kế Hoạch & Bộ Quy Chuẩn Tái Cấu Trúc Mã Nguồn Hệ Thống Resort (Code Refactor)

Tài liệu này là cẩm nang kỹ thuật thực thi dành cho AI nhằm **tái cấu trúc trực tiếp mã nguồn** dự án *Saigon - Condao Islands Resort Booking Platform* từ trạng thái chắp vá sang kiến trúc chuẩn công nghiệp (**Clean Architecture / 3-Tier Layered Architecture**), đảm bảo hệ thống chạy ổn định, không gãy tính năng trước khi tiến hành vẽ các biểu đồ PTTKHT.

---

## 1. Mục Tiêu Tái Cấu Trúc (Core Engineering Objectives)

1. **Khử tận gốc "Fat Routes" (1.200 dòng trong `booking_routes.py`)**:
   * Chuyển toàn bộ logic tính tiền, khóa phòng, áp voucher, và câu lệnh SQL từ file Route sang **Tầng Dịch vụ (Service Layer)**.
   * File Route chỉ giữ lại tối đa 15-20 dòng cho mỗi endpoint: *Nhận request $\rightarrow$ Gọi Service $\rightarrow$ Trả về Response/Render*.
2. **Chuẩn hóa CSDL 3NF & Khai tử "God Table" (`New_Bookings`)**:
   * Tách bảng 37 cột thành 4 thực thể Hợp thành: `BookingMaster`, `Invoice`, `BookingAttribution`, `CancellationRecord`.
   * Khai tử chuỗi CSV `selected_nights` (dùng 100% bảng quan hệ `Booking_Nights`).
   * Khai tử cơ chế tiền tệ kép (bỏ cột `_cents` trùng lặp, chuẩn hóa toàn hệ thống về số nguyên VND).
3. **Hợp nhất Mô hình Định danh (Unified Identity)**:
   * Chấm dứt việc duy trì 2 bảng riêng rẽ gây lỗi khóa ngoại (`Users` vs `Customer_Accounts`).
   * Chấm dứt việc tạo email giả `{phone}@walkin.local` cho khách vãng lai bằng cách cấu hình `customer_id` thành **Nullable Foreign Key**.
4. **Đảm bảo Tính Toàn vẹn & Chạy mượt mà**:
   * Duy trì hoạt động ổn định của Frontend (Port 5001) và Backend API (Port 5000), giữ nguyên giao diện đẹp mắt (GSAP, Bootstrap 5.3).

---

## 2. Kiến Trúc Mã Nguồn Mục Tiêu (Target Clean Architecture)

Tái cấu trúc thư mục Backend theo mô hình phân tầng hướng đối tượng chuẩn:

```text
.BackEnd/
├── app.py                      # Khởi tạo Flask App, đăng ký Blueprints & Config
├── db/
│   ├── HotelBooking.db         # SQLite file (WAL mode)
│   ├── schema.sql              # Lược đồ CSDL mới chuẩn 3NF
│   └── migrations.py           # Script chuyển đổi dữ liệu từ DB cũ sang DB mới
├── models/                     # TẦNG ENTITY (Đối tượng dữ liệu)
│   ├── account.py              # Account, CustomerAccount, StaffAccount
│   ├── room.py                 # Hotel, RoomType, PhysicalRoom, RoomRate
│   ├── booking.py              # BookingMaster, BookingNight, RoomLock
│   ├── finance.py              # Invoice, Payment, ExtraService
│   └── marketing.py            # Promotion, Review, Loyalty
├── repositories/               # TẦNG TRUY XUẤT DỮ LIỆU (Data Access Object / SQL)
│   ├── base_repository.py      # Quản lý kết nối SQLite, Context Manager Transaction
│   ├── room_repository.py      # Query phòng trống, kiểm tra khóa tạm
│   └── booking_repository.py   # Thao tác CRUD đơn phòng và chi tiết đêm
├── services/                   # TẦNG NGHIỆP VỤ CỐT LÕI (Business Logic / Controller)
│   ├── auth_service.py         # Xác thực, cấp token, phân quyền
│   ├── room_lock_service.py    # Quản lý giữ chỗ tạm thời 10 phút (TTL)
│   ├── pricing_service.py      # Tính giá hiệu lực theo ngày, phụ thu người lớn/trẻ em
│   ├── promotion_service.py    # Kiểm tra & trừ lượt dùng mã giảm giá nguyên tử
│   ├── booking_service.py      # Nhạc trưởng điều phối đặt phòng online & Walk-in
│   └── checkout_service.py     # Quyết toán trả phòng, cộng dồn ExtraServices, in hóa đơn
└── routes/                     # TẦNG BIÊN (Boundary HTTP Handlers - Mỏng & Sạch)
    ├── auth_routes.py
    ├── room_routes.py
    ├── booking_routes.py       # Giảm từ 1.200 dòng xuống còn ~150 dòng!
    ├── manager_routes.py
    └── housekeeping_routes.py
```

---

## 3. Lộ Trình 5 Bước Tái Cấu Trúc Mã Nguồn Thực Tế (Phase-by-Phase Roadmap)

### BƯỚC 1: Sao lưu & Tái cấu trúc Cơ sở Dữ liệu (Database Migration)
1. Tạo bản sao lưu dự phòng: `HotelBooking_Backup.db`.
2. Tạo script `db/schema.sql` mới chuẩn hóa:
   * Bảng `Accounts` (id, email, password_hash, account_type: 'customer' | 'staff', is_active, created_at).
   * Bảng `Customer_Profiles` (account_id PK/FK, full_name, phone, loyalty_points, tier).
   * Bảng `Staff_Profiles` (account_id PK/FK, full_name, role_id FK $\rightarrow$ Roles).
   * Bảng `Booking_Master` (booking_id PK, customer_id FK Nullable, hotel_id FK, room_type_id FK, arrival_date, departure_date, adults, children, total_amount, deposit_amount, booking_status).
   * Bảng `Invoices` (invoice_id PK, booking_id FK, invoice_number, issued_at, subtotal, service_total, final_total).
   * Bảng `Booking_Attributions` (id PK, booking_id FK, utm_source, utm_campaign, utm_medium).
3. Chạy script chuyển đổi dữ liệu từ bảng cũ sang bảng mới, loại bỏ vĩnh viễn cột CSV `selected_nights` và các cột `_cents`.

### BƯỚC 2: Xây dựng Tầng Dịch vụ Tách Biệt (Extracting Service Layer)
1. **Tạo `services/room_lock_service.py`**:
   * Đóng gói logic kiểm tra phòng bận, tạo khóa tạm với `locked_until = now + 10m`, và hàm tự động dọn dẹp khóa hết hạn.
2. **Tạo `services/pricing_service.py`**:
   * Đóng gói logic tra cứu bảng `Room_Rates`, fallback về `Dim_RoomType.base_price`, và tính phụ phí trẻ em/người lớn.
3. **Tạo `services/booking_service.py`**:
   * Đóng gói toàn bộ transaction đặt phòng: *Check lock $\rightarrow$ Calculate Price $\rightarrow$ Apply Voucher $\rightarrow$ Insert BookingMaster $\rightarrow$ Loop Insert BookingNights $\rightarrow$ Release Lock*.
   * Cung cấp method riêng cho Lễ tân: `create_walkin_booking(guest_name, guest_phone, room_id, nights)`.

### BƯỚC 3: Dọn Dẹp & Viết Lại Các File Routes (Slenderizing Controllers)
* Mở file `booking_routes.py`:
  * Xóa bỏ các câu lệnh SQL viết tay dài hàng chục dòng.
  * Thay bằng lời gọi dịch vụ đơn giản:
    ```python
    @booking_bp.route('/api/bookings', methods=['POST'])
    def create_booking():
        data = request.get_json()
        current_user = get_authenticated_user()
        try:
            booking = booking_service.process_online_booking(data, current_user)
            return jsonify({'success': True, 'booking_id': booking.id}), 201
        except BusinessLogicError as e:
            return jsonify({'success': False, 'message': str(e)}), 400
    ```

### BƯỚC 4: Chuẩn Hóa API Client Phía Frontend
* Rà soát `services/api.py` của Frontend (Port 5001):
  * Cập nhật các trường dữ liệu trả về tương thích với Schema mới (ví dụ: đọc `total_amount` thay vì `total_price_cents`).
  * Đảm bảo các view Jinja2 hiển thị đúng đơn vị tiền tệ VND (có format dấu phẩy ngăn cách hàng nghìn).

### BƯỚC 5: Kiểm Thử Đầu-Cuối (End-to-End Verification)
1. Chạy song song 2 server: Backend (Port 5000) và Frontend (Port 5001).
2. Kiểm tra thông suốt 4 kịch bản sống còn:
   * **Kịch bản 1**: Khách hàng vãng lai tìm kiếm $\rightarrow$ Khóa phòng $\rightarrow$ Thanh toán $\rightarrow$ Xác nhận thành công.
   * **Kịch bản 2**: Khách đặt cọc 50% $\rightarrow$ Lễ tân Check-in $\rightarrow$ Thêm nước suối minibar $\rightarrow$ Check-out quyết toán in hóa đơn.
   * **Kịch bản 3**: Lễ tân đặt phòng Walk-in cho khách không có tài khoản (kiểm tra không bị sinh email rác).
   * **Kịch bản 4**: Quản lý điều chỉnh giá ngày lễ $\rightarrow$ Khách tìm kiếm thấy ngay giá mới.
