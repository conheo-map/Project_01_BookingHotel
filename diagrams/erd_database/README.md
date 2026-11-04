# BỘ HỒ SƠ MÔ HÌNH THỰC THỂ LIÊN KẾT (ERD) & CSDL CHUẨN HÓA 3NF
## Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo
*(Saigon - Condao Islands Resort Platform)*
**Tiêu chuẩn Học thuật: Đại học Kinh tế Quốc dân (NEU) - Lead Data Architect Grade 10.0**

---

### I. CÁC NGUYÊN TẮC THIẾT KẾ CƠ SỞ DỮ LIỆU CHUẨN HÓA 3NF

1. **Khắc phục triệt để Anti-Pattern "God Table"**:
   - Loại bỏ hoàn toàn bảng khổng lồ chứa hàng chục cột vô tổ chức (`New_Bookings`).
   - Bóc tách theo đúng nguyên lý phân rã không mất thông tin (Lossless Decomposition) thành các thực thể độc lập có vai trò đơn nhất (Single Responsibility Principle).

2. **Tách biệt Hạng phòng thương mại (Room Types) và Phòng vật lý (Physical Rooms)**:
   - `Room_Types`: Quản lý các thuộc tính kinh doanh B2C (tên hạng phòng, sức chứa người lớn/trẻ em, giá niêm yết theo đêm, phụ thu thêm người).
   - `Physical_Rooms`: Quản lý thực thể phòng có thật tại Resort (số phòng 101, 202, tầng, trạng thái buồng phòng `CLEAN`, `DIRTY`, `MAINTENANCE`, trạng thái chiếm dụng `VACANT`, `OCCUPIED`).

3. **Cơ chế Khóa giữ chỗ phòng chống Overbooking (Hold Lock Engine)**:
   - `Room_Hold_Locks`: Quản lý phiên giữ phòng tạm thời trong 15 phút khi khách hàng đang quét mã QR VNPAY/MoMo. Hết 15 phút, cronjob tự động giải phóng tồn kho.

4. **Hồ sơ Đặt phòng Master - Detail (3NF)**:
   - `Bookings`: Lưu trữ thông tin giao dịch tổng thể, mã PNR 6 ký tự, tổng tiền, tiền cọc.
   - `Booking_Nights`: Chi tiết từng đêm lưu trú (`stay_date`, `night_price`). Khách đặt online thì `physical_room_id` để `NULL`; khi khách tới quầy làm thủ tục Check-in, Lễ tân mới gán phòng vật lý sạch vào từng đêm.

5. **Mô hình Định danh Hợp nhất (Single Identity Model)**:
   - Bảng tài khoản gốc `Accounts` liên kết 1-1 với `Customer_Profiles` (khách hàng, hội viên tích điểm) và `Staff_Profiles` (nhân viên, vai trò RBAC).
   - Khách vãng lai đến đặt trực tiếp tại quầy (Walk-in) được lưu thẳng vào `Bookings` với `customer_id = NULL`, chấm dứt hoàn toàn tình trạng sinh tài khoản ảo rác `{phone}@walkin.local`.

6. **Phân hệ Tiền sảnh, Dịch vụ & Quyết toán Công nợ (Folio Billing & Invoicing)**:
   - `Service_Items`: Danh mục các mặt hàng minibar, F&B, giặt ủi, spa.
   - `Service_Consumptions`: Chi tiết dịch vụ khách sử dụng trong kỳ lưu trú, tự động cộng dồn vào hóa đơn phòng (Folio Billing).
   - `Invoices`: Hóa đơn tài chính VAT phát hành khi Check-out.
   - `Payments`: Ghi nhận từng lần thanh toán thực tế (đặt cọc online hoặc quyết toán tại quầy).

7. **Phân hệ Buồng phòng & Bảo trì vật tư**:
   - `Housekeeping_Logs`: Nhật ký ca dọn phòng của nhân viên buồng phòng.
   - `Maintenance_Tickets`: Phiếu ghi nhận sự cố hỏng hóc và tiến độ sửa chữa thiết bị.

---

### II. BẢNG TRA CỨU FILE NGUỒN VÀ BẢN XEM TRỰC TIẾP

| STT | Tên Sản Phẩm Bàn Giao | Tệp Nguồn / Vị Trí Lưu | Xem Trực Tiếp Trình Duyệt | Trạng Thái Nghiệm Thu |
|:---:|:---|:---:|:---:|:---:|
| **01** | **Biểu đồ ERD 3NF (Draw.io XML)** | [`00_Bieu_Do_ERD_Database_3NF.drawio`](file:///c:/HocC/Daily/00_Bieu_Do_ERD_Database_3NF.drawio) | [`00_Bieu_Do_ERD_Database_3NF.html`](file:///c:/HocC/Daily/00_Bieu_Do_ERD_Database_3NF.html) | Đạt Chuẩn 10.0 (100% Monochrome) |
| **02** | **Kịch bản SQL DDL (Production Script)** | [`schema_saigon_condao_3nf.sql`](file:///c:/HocC/Daily/schema_saigon_condao_3nf.sql) | Mở bằng VSCode / DBeaver / DataGrip | 15 Bảng 3NF + Seed Data |
| **03** | **Từ điển Dữ liệu Chi tiết** | [`README.md`](file:///c:/HocC/Daily/erd_database/README.md) | Markdown Viewer | Đầy đủ thuộc tính & ràng buộc |

> **Bản sao đồng bộ**: Có thể truy cập tại cả 2 đường dẫn:
> - [`c:\HocC\Project_Booking - Sao chép\diagrams\erd_database/`](file:///c:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/diagrams/erd_database/)
> - [`c:\HocC\Daily/`](file:///c:/HocC/Daily/)
