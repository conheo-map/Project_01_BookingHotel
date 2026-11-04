# BỘ HỒ SƠ BIỂU ĐỒ TUẦN TỰ THEO MÔ HÌNH BCE (SEQUENCE DIAGRAMS - GRADE 10.0 STANDARD)
## Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo
*(Saigon - Condao Islands Resort Platform)*

---

### I. CÁC NGUYÊN TẮC HỌC THUẬT KIẾN TRÚC BCE & UML 2.X

1. **Kiến trúc 3 phân lớp BCE chuẩn mực (Boundary - Control - Entity)**:
   - **Boundary ($\vdash\bigcirc$)**: Lớp biên giao diện (`UI_...`) - Điểm chạm tương tác trực tiếp với Tác nhân (Actor).
   - **Control ($\circlearrowleft$)**: Lớp điều khiển nghiệp vụ (`CTL_...` / Service Layer) - Trọng tài điều phối quy trình, kiểm tra nghiệp vụ và xử lý logic.
   - **Entity ($\ominus$)**: Lớp thực thể dữ liệu (`En_...` / Table / Domain Model) - Đại diện cho các đối tượng lưu trữ trạng thái bền vững.

2. **Quy tắc cấm nhảy cóc (Strict Layering - Anti-Pattern AP-02 Audit)**:
   - `Actor` $\longleftrightarrow$ `Boundary` $\longleftrightarrow$ `Control` $\longleftrightarrow$ `Entity`.
   - **Cấm tuyệt đối**: Boundary gọi trực tiếp vào Entity; Entity trả dữ liệu thẳng về Boundary mà không qua Control.

3. **Vạch kích hoạt (Activation Bar) & Đối xứng Call-Stack (Anti-Pattern AP-01 Audit)**:
   - Vạch kích hoạt cố định bề rộng 12px viền đen nền trắng tại điểm tiếp nhận Message.
   - Gọi hàm đồng bộ (Synchronous Call): Mũi tên nét liền tam giác đặc (`endArrow=block;endFill=1;`).
   - Trả về (Return Message): Mũi tên nét đứt mở (`endArrow=open;dashed=1;`).

4. **Vòng đời đối tượng & Khung kết hợp Alt (Anti-Patterns AP-05 & AP-06 Audit)**:
   - Bản ghi mới sinh ra (Booking Master, Invoice, Receipt) dùng thông điệp `<<create>>` đâm thẳng vào đỉnh đầu Lifeline mới vẽ tụt xuống dưới.
   - Luôn có khung `Alt` phân nhánh rõ ràng: `[Thành công / Hợp lệ]` và `[Thất bại / Hết phòng / Lỗi thanh toán]`.

5. **Tiêu chuẩn đồ họa CAD/UML Monochrome 100%**:
   - Nền trắng tinh `#FFFFFF`, nét vẽ viền đen `#000000`, chữ màu đen `#000000`, phông chữ `Arial / Segoe UI`.

---

### II. BẢNG TRA CỨU 5 BIỂU ĐỒ TUẦN TỰ TRỌNG ĐIỂM (BCE)

| STT | Mã Biểu Đồ | Tên Quy Trình Nghiệp Vụ | Tệp Nguồn Draw.io | Xem Trực Tiếp Trình Duyệt | Trạng Thái Nghiệm Thu |
|:---:|:---|:---|:---:|:---:|:---:|
| **01** | `SD-01` | **Đặt phòng trực tuyến & Khóa phòng chống trùng 15 phút** *(B2C Booking & Hold Lock)* | [`SD_01_Dat_Phong_Truc_Tuyen_Va_Khoa_Phong_15P.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_01_Dat_Phong_Truc_Tuyen_Va_Khoa_Phong_15P.drawio) | [`SD_01_Dat_Phong_Truc_Tuyen_Va_Khoa_Phong_15P.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_01_Dat_Phong_Truc_Tuyen_Va_Khoa_Phong_15P.html) | Đạt Chuẩn 10.0 |
| **02** | `SD-02` | **Tiếp nhận & Làm thủ tục nhận phòng tại quầy** *(Front Desk Check-in & RFID Card)* | [`SD_02_Thu_Tuc_Nhan_Phong_Check_In.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_02_Thu_Tuc_Nhan_Phong_Check_In.drawio) | [`SD_02_Thu_Tuc_Nhan_Phong_Check_In.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_02_Thu_Tuc_Nhan_Phong_Check_In.html) | Đạt Chuẩn 10.0 |
| **03** | `SD-03` | **Ghi nhận tiêu dùng dịch vụ phát sinh** *(Extra Services, Minibar & Folio Billing)* | [`SD_03_Ghi_Nhan_Tieu_Dung_Dich_Vu_Phat_Sinh.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_03_Ghi_Nhan_Tieu_Dung_Dich_Vu_Phat_Sinh.drawio) | [`SD_03_Ghi_Nhan_Tieu_Dung_Dich_Vu_Phat_Sinh.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_03_Ghi_Nhan_Tieu_Dung_Dich_Vu_Phat_Sinh.html) | Đạt Chuẩn 10.0 |
| **04** | `SD-04` | **Làm thủ tục trả phòng & Quyết toán công nợ** *(Front Desk Check-out & Folio Settlement)* | [`SD_04_Thu_Tuc_Tra_Phong_Va_Quyet_Toan_Check_Out.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_04_Thu_Tuc_Tra_Phong_Va_Quyet_Toan_Check_Out.drawio) | [`SD_04_Thu_Tuc_Tra_Phong_Va_Quyet_Toan_Check_Out.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_04_Thu_Tuc_Tra_Phong_Va_Quyet_Toan_Check_Out.html) | Đạt Chuẩn 10.0 |
| **05** | `SD-05` | **Cập nhật tiến độ buồng phòng thời gian thực** *(Housekeeping Mobile Workflow)* | [`SD_05_Cap_Nhat_Tien_Do_Ve_Sinh_Buong_Phong.drawio`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_05_Cap_Nhat_Tien_Do_Ve_Sinh_Buong_Phong.drawio) | [`SD_05_Cap_Nhat_Tien_Do_Ve_Sinh_Buong_Phong.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/SD_05_Cap_Nhat_Tien_Do_Ve_Sinh_Buong_Phong.html) | Đạt Chuẩn 10.0 |
| **ALL** | **MASTER** | **TRANG MASTER VIEWER XEM CẢ 5 BIỂU ĐỒ TUẦN TỰ** | — | [`viewer_sequence.html`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/sequence_bce/viewer_sequence.html) | Đạt Chuẩn 10.0 |

> **Thư mục đồng bộ**: Bản sao sẵn sàng tại [`c:\HocC\Daily\sequence_bce\viewer_sequence.html`](file:///c:/HocC/Daily/sequence_bce/viewer_sequence.html).
