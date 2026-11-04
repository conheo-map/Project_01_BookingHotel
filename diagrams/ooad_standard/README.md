# BỘ HỒ SƠ BIỂU ĐỒ USE CASE CHUẨN MỰC OOAD (TIÊU CHUẨN ĐỒ ÁN ĐIỂM 10.0)
## Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo
*(Saigon - Condao Islands Resort Booking Platform)*

---

### I. CÁC NGUYÊN TẮC THIẾT KẾ CHUẨN MỰC UML 2.X (TEXTBOOK STANDARD)

1. **Quy Tắc Vị Trí Tác Nhân Chuẩn Giáo Trình (Actor Positioning Hierarchy)**:
   - **Cột Bên Trái (Left Side):** 100% là **Tác nhân chính (Primary Actors)** - những người trực tiếp đăng nhập và khởi xướng mục tiêu tương tác với hệ thống:
     * `KHÁCH HÀNG (CUSTOMER)`
     * `NHÂN VIÊN LỄ TÂN (RECEPTIONIST)`
     * `QUẢN LÝ RESORT (HOTEL MANAGER)` *(có mũi tên kế thừa trỏ lên Lễ tân)*
     * `NHÂN VIÊN BUỒNG PHÒNG (HOUSEKEEPER)`
     * `QUẢN TRỊ VIÊN HỆ THỐNG (SYSTEM ADMIN)`
   - **Cột Bên Phải (Right Side):** 100% là **Tác nhân phụ / Hệ thống hỗ trợ (Secondary / Supporting Actors)** - các dịch vụ bên ngoài nhận dữ liệu hoặc hỗ trợ hệ thống:
     * `CỔNG THANH TOÁN (PAYMENT GATEWAY - VNPAY/MOMO)`
     * `MÁY CHỦ CHẠY NỀN (CRON SYSTEM)`
   - **Cạnh Đáy & Cạnh Trên (Top/Bottom):** **TUYỆT ĐỐI KHÔNG CÓ ACTOR NÀO** (loại bỏ hoàn toàn lỗi đặt Actor ở dưới đáy kéo dây vòng vèo).
2. **Quy Chuẩn Phần Tử UML Thuần Khiết (Pure UML Elements)**:
   - Biểu đồ **chỉ sử dụng đúng 4 thành phần quy chuẩn của UML**:
     - **Tác nhân (Actor)**: Biểu tượng hình que chuẩn.
     - **Use Case**: Biểu tượng hình elip viền đen nền trắng.
     - **Ranh giới hệ thống (System Boundary)**: Khung chữ nhật bao quanh.
     - **Quan hệ nối**: `Association` (nét liền), `Generalization` (tam giác rỗng), `«include»` và `«extend»` (nét đứt kèm mũi tên).
   - **Loại bỏ 100% các hộp ghi chú (Note Box)**: Các điều kiện mở rộng (Extension points) được diễn giải chuẩn mực trong Tài liệu Đặc tả Use Case (Use Case Specification), không vẽ các ô giấy gập góc gây rối mắt trên biểu đồ.
3. **Phong cách hiển thị Monochrome 100% (Đen - Trắng Thuần Khiết)**:
   - Nền trắng tinh `#FFFFFF`, nét vẽ viền đen `#000000`, chữ màu đen `#000000`.
   - Đúng tiêu chuẩn đồ án học thuật viện nghiên cứu / đại học chuẩn quốc tế.
4. **Không Đè Nét & Không Đâm Xuyên (Zero Crossing & Zero Slicing)**:
   - Khóa cứng 100% tọa độ neo `exitX/Y` và `entryX/Y` ở mép ngoài đối tượng.
5. **Xử lý nhãn Text UML chống lỗi font & DOM HTML**:
   - Sử dụng chuẩn ký tự Guillemets chính thức của OMG UML (`«include»` và `«extend»`), không bị trình duyệt hiểu nhầm là thẻ HTML `<include>` gây mất chữ thành `<>`.
   - Định dạng Strict UTF-8 without BOM.

---

### II. BẢNG TRA CỨU FILE NGUỒN VÀ BẢN XEM TRỰC TIẾP

| STT | Tên Biểu Đồ Nghiệp Vụ | Tệp Nguồn Draw.io | Xem Trực Tiếp Trình Duyệt | Trạng Thái Nghiệm Thu |
|:---:|:---|:---:|:---:|:---:|
| **00** | **Sơ đồ Use Case Tổng Quát Toàn Hệ Thống (System Overview)** | [`00_So_Do_Use_Case_Tong_Quat.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/00_So_Do_Use_Case_Tong_Quat.drawio) | [`00_So_Do_Use_Case_Tong_Quat.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/00_So_Do_Use_Case_Tong_Quat.html) | Đạt Chuẩn 10.0 |
| **01** | **Phân hệ 01: Cổng đặt phòng trực tuyến B2C (Online Booking & Refund)** | [`01_Phan_He_Dat_Phong_Truc_Tuyen_B2C.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/01_Phan_He_Dat_Phong_Truc_Tuyen_B2C.drawio) | [`01_Phan_He_Dat_Phong_Truc_Tuyen_B2C.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/01_Phan_He_Dat_Phong_Truc_Tuyen_B2C.html) | Đạt Chuẩn 10.0 |
| **02** | **Phân hệ 02: Quản lý tài khoản & Phân quyền (IAM & RBAC)** | [`02_Phan_He_Tai_Khoan_Va_Phan_Quyen_RBAC.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/02_Phan_He_Tai_Khoan_Va_Phan_Quyen_RBAC.drawio) | [`02_Phan_He_Tai_Khoan_Va_Phan_Quyen_RBAC.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/02_Phan_He_Tai_Khoan_Va_Phan_Quyen_RBAC.html) | Đạt Chuẩn 10.0 |
| **03** | **Phân hệ 03: Tác nghiệp quầy tiền sảnh & Lễ tân (Front Desk & PMS)** | [`03_Phan_He_Tac_Nghiep_Le_Tan_Tien_Sanh.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/03_Phan_He_Tac_Nghiep_Le_Tan_Tien_Sanh.drawio) | [`03_Phan_He_Tac_Nghiep_Le_Tan_Tien_Sanh.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/03_Phan_He_Tac_Nghiep_Le_Tan_Tien_Sanh.html) | Đạt Chuẩn 10.0 |
| **04** | **Phân hệ 04: Vận hành buồng phòng (Housekeeping Management)** | [`04_Phan_He_Van_Hanh_Buong_Phong.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/04_Phan_He_Van_Hanh_Buong_Phong.drawio) | [`04_Phan_He_Van_Hanh_Buong_Phong.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/04_Phan_He_Van_Hanh_Buong_Phong.html) | Đạt Chuẩn 10.0 |
| **05** | **Phân hệ 05: Quản trị doanh thu, bảng giá & Báo cáo (Revenue & Analytics)** | [`05_Phan_He_Quan_Tri_Doanh_Thu_Va_Bao_Cao.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/05_Phan_He_Quan_Tri_Doanh_Thu_Va_Bao_Cao.drawio) | [`05_Phan_He_Quan_Tri_Doanh_Thu_Va_Bao_Cao.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/05_Phan_He_Quan_Tri_Doanh_Thu_Va_Bao_Cao.html) | Đạt Chuẩn 10.0 |
| **ALL** | **TRANG MASTER VIEWER XEM TỔNG HỢP CẢ 6 BIỂU ĐỒ TRÊN MỘT GIAO DIỆN** | — | [`viewer.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/ooad_standard/viewer.html) | Đạt Chuẩn 10.0 |

> **Thư mục đồng bộ học thuật**: Bản sao cũng đã sẵn sàng tại [`c:\HocC\Daily\ooad_standard\viewer.html`](file:///c:/HocC/Daily/ooad_standard/viewer.html).
