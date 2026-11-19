# KỊCH BẢN THUYẾT TRÌNH TỐI ƯU TỪNG SLIDE (PHIÊN BẢN BẮN TỈA TRỌNG TÂM - 08 PHÚT)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO RESORT
> **Tài liệu trình chiếu**: Tệp [slide_N7.pdf](file:///C:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/slide_N7.pdf) (khớp 100% từ Slide 1 đến Slide 52)  
> **Phong cách trình bày**: **Vào thẳng vấn đề - Không đọc chữ trên slide - 15 giây/slide biểu đồ - Dập tắt bẫy vặn vẹo**.  
> **Tổng thời lượng toàn bài**: Đúng **08 - 09 phút** (vừa khít trước khi chuông Hội đồng reo).

---

## ⚡ HƯỚNG DẪN DÀNH CHO NGƯỜI THUYẾT TRÌNH:
1. **Tay cầm clicker chuyển slide theo đúng nhịp**: Mỗi slide biểu đồ chỉ dừng **15 - 20 giây**.
2. **Không đọc lại chữ đã có trên slide**: Thầy cô tự nhìn thấy chữ, bạn chỉ nói **bản chất nghiệp vụ & đột phá kỹ thuật**.
3. **Mục 💡 Chốt chặn**: Là vũ khí phản xạ nhanh nếu Thầy ngắt lời hỏi vặn. Không hỏi thì không cần đọc.

---

# PHẦN I: MỞ ĐẦU & YÊU CẦU HỆ THỐNG (SLIDE 01 - 16)
*(Lướt nhanh trong 1.5 phút)*

### [Slide 01] Bìa Đề Tài (10s)
- 🎙️ **Nói nhanh**: *"Kính thưa Quý Thầy/Cô, em xin đại diện Nhóm 7 báo cáo đồ án OOAD: **Hệ thống Quản lý và Đặt phòng ở Saigon - Condao Resort**."*

### [Slide 02] Mục Lục Báo Cáo (10s)
- 🎙️ **Nói nhanh**: *"Báo cáo gồm 5 phần, trong đó Nhóm tập trung sâu nhất vào Phần 4 - Mô hình hóa hệ thống với trọn bộ 28 biểu đồ thiết kế chuẩn RUP."*

### [Slide 03 - 05] Bối Cảnh & 3 Thách Thức Sống Còn (30s)
- 🎙️ **Nói nhanh**: *"Khách sạn Sài Gòn - Côn Đảo là resort 4-5 sao tại hải đảo biệt lập. Nghiệp vụ tại đây có **3 bài toán đặc thù**:*
  1. *Khách dồn dập đặt theo chuyến bay/tàu cao tốc, dễ gây bán trùng phòng (**Overbooking**).*
  2. *Sự tách biệt giữa **Hạng phòng kinh doanh B2C** và **Phòng vật lý thực tế**.*
  3. *Nhu cầu theo dõi **Sổ cái chi tiêu Folio tập trung** và cơ chế hoàn tiền khi bão gió cấm tàu."*

### [Slide 06 - 10] Mục Tiêu & Khảo Sát Hiện Trạng (20s)
- 🎙️ **Nói nhanh**: *"Hiện trạng resort đang tiếp nhận phòng phân tán qua Website, Hotline và Fanpage. Mục tiêu của đề tài là xây dựng hệ thống tự động hóa khép kín từ đặt phòng, lễ tân đến buồng phòng thời gian thực."*

### [Slide 11 - 16] Đặc Tả Yêu Cầu Chức Năng, Phi Chức Năng & BR (20s)
- 🎙️ **Nói nhanh**: *"Hệ thống được đặc tả chặt chẽ qua 5 nhóm tác nhân, 12 yêu cầu chức năng FR, 25 yêu cầu phi chức năng NFR, và 16 quy tắc nghiệp vụ BR (như Check-in 14:00, Check-out 12:00, Khóa giữ chỗ 15 phút, Chính sách hoàn cọc). Toàn bộ được cụ thể hóa thành 28 biểu đồ kiến trúc ngay sau đây."*

---

# PHẦN II: THUYẾT TRÌNH TRỌNG TÂM TỪNG BIỂU ĐỒ (SLIDE 17 - 45)
*(Mỗi slide nói đúng 15 - 20 giây - Điểm huyệt kiến trúc)*

---

### [Slide 17] Biểu Đồ Use Case Tổng Quát (20s)
- 🎙️ **Nói nhanh**: *"Slide 17 là Use Case tổng quát: Hệ thống phân định 5 tác nhân người dùng và 2 tác nhân ngoại vi là **Cổng thanh toán VNPay** và **Máy chủ chạy nền Cron System**. Toàn bộ 15 Use Case cốt lõi được đóng khung trọn vẹn trong ranh giới hệ thống."*
- 👉 **Chỉ hình**: Rê chuột vòng quanh ranh giới hệ thống và chỉ vào Cron, VNPay ở ngoài.
- 💡 **Chốt chặn (Nếu Thầy vặn Cron/VNPay là Actor?)**: *"Theo UML 2.5, bất kỳ thực thể bên ngoài nào tương tác gửi/nhận dữ liệu với hệ thống đều là Actor hợp lệ."*

---

### [Slide 18] Use Case Phân Rã: Cổng Đặt Phòng B2C (15s)
- 🎙️ **Nói nhanh**: *"Tại phân hệ Đặt phòng B2C: Use Case 'Đặt phòng trực tuyến' bắt buộc **`<<include>>`** 'Khóa phòng chống trùng 15 phút' và 'Xác thực cổng thanh toán'; đồng thời liên kết **`<<extend>>`** với 'Áp dụng Voucher' khi khách có mã ưu đãi."*
- 👉 **Chỉ hình**: Chỉ vào đường `<<include>>` trỏ thuận và `<<extend>>` trỏ ngược.
- 💡 **Chốt chặn (Nếu Thầy vặn chiều mũi tên?)**: *"Include là gọi bắt buộc nên trỏ thuận; Extend là chèn hành vi mở rộng nên trỏ ngược về Use Case cơ sở."*

---

### [Slide 19] Use Case Phân Rã: Quản Lý Tài Khoản & Phân Quyền (15s)
- 🎙️ **Nói nhanh**: *"Phân hệ Tài khoản hỗ trợ đăng ký hội viên VIP, phân quyền vai trò RBAC cho nhân sự, ghi nhận Audit Log an ninh, và cơ chế **`<<extend>>` tự động khóa tài khoản sau 5 lần đăng nhập sai** để chống Brute-force."*
- 👉 **Chỉ hình**: Chỉ vào nhánh mở rộng Khóa tài khoản và Audit Log.

---

### [Slide 20] Use Case Phân Rã: Tác Nghiệp Quầy Tiền Sảnh & Lễ Tân (15s)
- 🎙️ **Nói nhanh**: *"Tại quầy tiền sảnh, hệ thống hỗ trợ cả khách đặt trước lẫn **khách Walk-in vãng lai**, quản lý gán phòng trên sơ đồ Gantt thời gian thực, xử lý Check-out quyết toán Folio VAT, và xử lý hủy đơn khách vắng mặt (No-Show) sau 23:59."*
- 👉 **Chỉ hình**: Chỉ vào Use Case Walk-in và Sơ đồ Gantt / No-Show.

---

### [Slide 21] Use Case Phân Rã: Vận Hành Buồng Phòng (15s)
- 🎙️ **Nói nhanh**: *"Phân hệ Buồng phòng giúp nhân viên nhận ca dọn buồng trên di động, cập nhật tiến độ sạch, kích hoạt **`<<extend>>` Báo cáo sự cố bảo trì** khi hỏng thiết bị, và quy trình Tổ trưởng nghiệm thu phòng sạch."*
- 👉 **Chỉ hình**: Chỉ vào nhánh mở rộng Báo cáo sự cố bảo trì.

---

### [Slide 22] Use Case Phân Rã: Quản Trị Doanh Thu & Báo Cáo (15s)
- 🎙️ **Nói nhanh**: *"Phân hệ Quản lý cung cấp công cụ thiết lập **Giá linh hoạt theo mùa (Dynamic Pricing)**, ban hành chính sách hoàn cọc bậc thang, và tự động tính toán các chỉ số KPI khách sạn như RevPAR và công suất phòng."*
- 👉 **Chỉ hình**: Chỉ vào Cài đặt giá linh hoạt và Báo cáo KPI.

---

### [Slide 23] Biểu Đồ Hoạt Động: Đặt Phòng Trực Tuyến (AD-01) (20s)
- 🎙️ **Nói nhanh**: *"Biểu đồ AD-01 mô hình hóa luồng chống Race Condition: Ngay khi khách chọn phòng, hệ thống **tạo khóa giữ phòng 15 phút**. Thanh phân nhánh **Fork** kích hoạt song song Timer 15:00 và luồng quét VietQR. Nếu thanh toán thành công trong 15 phút thì tạo Booking, nếu quá hạn thì tự động giải phóng phòng."*
- 👉 **Chỉ hình**: Rê chuột qua thanh Fork và đồng hồ Timer 15 phút.
- 💡 **Chốt chặn (Nếu Thầy vặn quá hạn mà Webhook mới tới?)**: *"Hệ thống có nhánh Reconciliation đối soát tự động để hoàn tiền hoặc đổi phòng, không bao giờ nuốt tiền khách."*

---

### [Slide 24] Biểu Đồ Hoạt Động: Check-In & Gán Phòng Vật Lý (AD-02) (15s)
- 🎙️ **Nói nhanh**: *"AD-02 xử lý cả khách đặt trước và khách Walk-in. Điểm chốt chặn là điều kiện lọc phòng: Hệ thống **chỉ cho phép gán phòng thỏa mãn 3 tiêu chuẩn**: Thuộc đúng hạng phòng, Trạng thái buồng phòng là CLEAN (đã dọn sạch), và Lịch phòng VACANT không trùng."*
- 👉 **Chỉ hình**: Chỉ vào hình thoi Decision kiểm tra phòng CLEAN và VACANT.

---

### [Slide 25] Biểu Đồ Hoạt Động: Dịch Vụ Phát Sinh & Folio (AD-03) (15s)
- 🎙️ **Nói nhanh**: *"AD-03 thể hiện kế toán Folio: Khi khách dùng minibar hay gọi món, hệ thống kiểm tra phòng đang `OCCUPIED` và Folio còn mở $\rightarrow$ thực thi giao dịch nguyên tử **cộng dồn khoản nợ vào số dư Folio** và in phiếu cho khách ký."*
- 👉 **Chỉ hình**: Chỉ vào bước 'Lưu Order và Folio Details trong cùng giao dịch'.

---

### [Slide 26] Biểu Đồ Hoạt Động: Check-Out & Quyết Toán (AD-04) (15s)
- 🎙️ **Nói nhanh**: *"AD-04 đối soát toàn bộ chi phí theo công thức: $\text{Số dư} = \text{Tiền phòng} + \text{Dịch vụ} - \text{Cọc}$. Nút rẽ nhánh kiểm soát điều kiện bảo vệ **`[Công nợ bằng 0?]`**: Chỉ khi số dư cân bằng, hệ thống mới xuất hóa đơn VAT Saigontourist và tự động đổi phòng sang `DIRTY`."*
- 👉 **Chỉ hình**: Chỉ vào điều kiện `[Công nợ bằng 0?]` và chuyển `DIRTY`.

---

### [Slide 27] Biểu Đồ Hoạt Động: Dọn Buồng & Bảo Trì (AD-05) (15s)
- 🎙️ **Nói nhanh**: *"AD-05 vận hành buồng phòng di động: Phòng bẩn chuyển `CLEANING`. Nếu hỏng hóc $\rightarrow$ chuyển `MAINTENANCE`. Nếu đạt chuẩn sạch $\rightarrow$ chuyển `CLEAN` và **bắn sự kiện WebSocket thời gian thực** để sơ đồ phòng lễ tân chuyển xanh ngay lập tức."*
- 👉 **Chỉ hình**: Chỉ vào 2 nhánh: Bắn WebSocket sang Lễ tân và nhánh khóa MAINTENANCE.

---

### [Slide 28] Biểu Đồ Tuần Tự: Giới Thiệu Mô Hình (10s)
- 🎙️ **Nói nhanh**: *"Slide 28 mở đầu cho Khối Sequence: Toàn bộ 6 biểu đồ tuần tự được thiết kế theo chuẩn **3 Tầng BCE (Boundary - Control - Entity)** với quy tắc **CẤM NHẢY CÓC**, Boundary không được gọi thẳng vào Entity để bảo vệ tính bao đóng."*

---

### [Slide 29] Biểu Đồ Tuần Tự: Đặt Phòng & Khóa 15m (SD-01) (20s)
- 🎙️ **Nói nhanh**: *"SD-01 thể hiện 17 thông điệp: `:BookingService` gọi `:RoomInventory` tạo khóa tạm `createHoldLock 15m`. Khách quét VietQR $\rightarrow$ VNPay gửi Webhook IPN $\rightarrow$ `:BookingService` tạo `:Booking` trạng thái `CONFIRMED`, sinh `:BookingNights`, và gọi `markLockAsSold` chuyển khóa sang ĐÃ BÁN."*
- 👉 **Chỉ hình**: Chỉ vào `createHoldLock`, khung Alt thành công và hàm `markLockAsSold`.
- 💡 **Chốt chặn (Nếu Thầy vặn Race Condition?)**: *"Áp dụng Pessimistic Hold with TTL bọc trong Transaction nguyên tử, ai chạm DB trước mili-giây sẽ giành được khóa."*

---

### [Slide 30] Biểu Đồ Tuần Tự: Làm Thủ Tục Nhận Phòng (SD-02) (15s)
- 🎙️ **Nói nhanh**: *"SD-02 gồm 16 thông điệp: Lễ tân tra cứu PNR, quét CCCD lưu vào `:GuestProfile`. Control gọi `:PhysicalRoom` kiểm tra phòng sạch `checkCleanRooms(status='CLEAN')` $\rightarrow$ gán số phòng cụ thể vào từng đêm và cập nhật phòng sang `OCCUPIED`."*
- 👉 **Chỉ hình**: Chỉ vào bước quét CCCD và hàm `assignPhysicalRoom`.

---

### [Slide 31] Biểu Đồ Tuần Tự: Ghi Nhận Tiêu Dùng Dịch Vụ (SD-03) (15s)
- 🎙️ **Nói nhanh**: *"SD-03 gồm 12 thông điệp: `:FolioBillingService` xác thực phòng đang lưu trú, lấy giá niêm yết có VAT từ `:PriceCatalog` $\rightarrow$ gọi `:FolioInvoice` lưu chi tiết tiêu dùng và gọi hàm `postChargeToFolio` cộng dồn số dư nợ của phòng."*
- 👉 **Chỉ hình**: Chỉ vào hàm `recordConsumption` và `postChargeToFolio`.

---

### [Slide 32] Biểu Đồ Tuần Tự: Trả Phòng & Quyết Toán (SD-04) (15s)
- 🎙️ **Nói nhanh**: *"SD-04 gồm 16 thông điệp: Lễ tân nạp phụ thu minibar $\rightarrow$ tính tổng nợ $\rightarrow$ thu tiền thiếu $\rightarrow$ hệ thống tự động sinh hóa đơn tài chính điện tử `:Invoice` thuế suất VAT 8%, mã số thuế Saigontourist `0312456789-001`, và gửi lệnh đổi phòng sang `DIRTY`."*
- 👉 **Chỉ hình**: Chỉ vào bước tạo Invoice VAT và thông điệp đổi phòng sang DIRTY.

---

### [Slide 33] Biểu Đồ Tuần Tự: Vận Hành Dọn Dẹp Buồng Phòng (SD-05) (15s)
- 🎙️ **Nói nhanh**: *"SD-05 gồm 21 thông điệp: Nhân viên buồng phòng nhận phòng đổi sang `CLEANING`, bấm giờ ca dọn `:CleaningLog`. Dọn xong đổi sang `CLEAN` và **bắn WebSocket Event `notifyRoomStatus('CLEAN')`** về quầy lễ tân. Nếu hỏng hóc thì tạo `:MaintenanceTicket`."*
- 👉 **Chỉ hình**: Chỉ vào hàm đóng CleaningLog và sự kiện WebSocket Event.

---

### [Slide 34] Biểu Đồ Tuần Tự: Hủy Đặt Phòng & Hoàn Cọc (SD-06) (20s)
- 🎙️ **Nói nhanh**: *"SD-06 gồm 27 thông điệp: `:BookingCancellationService` gọi `:RefundPolicy` tính số giờ trước check-in: Hoàn 100% trước 72h, 50% từ 24-72h, 0% dưới 24h. Hệ thống đổi đơn sang `Canceled`, ghi chứng từ hoàn tiền âm (`-refundAmount`), và gọi **`releaseBookedNights`** mở lại phòng trống ngay lập tức."*
- 👉 **Chỉ hình**: Chỉ vào hàm `getRefundPercentage`, chứng từ tiền âm, và `releaseBookedNights`.
- 💡 **Chốt chặn (Nếu Thầy vặn tại sao ghi tiền âm?)**: *"Kế toán kép: Khoản hoàn tiền ghi âm để câu lệnh `SUM(amount)` tự động đối soát chính xác doanh thu thực thu."*

---

### [Slide 35 - 36] Biểu Đồ Lớp – Domain Class Diagram (25s)
- 🎙️ **Nói nhanh**: *"Slide 35 và 36 là Biểu đồ Lớp Lĩnh vực thiết kế 3 ngăn theo nguyên lý **Information Expert**:*
  - *Mối quan hệ **Hợp thành (Composition $\blacklozenge$)** ràng buộc sinh tử giữa `BookingMaster` và `BookingNight`, giữa `ServiceFolio` và `FolioItem`.*
  - *Mối quan hệ **Thu nạp (Aggregation $\diamondsuit$)** độc lập vòng đời giữa `Hotel` $\rightarrow$ `RoomType` $\rightarrow$ `PhysicalRoom`.*
  - *Mối quan hệ **Kế thừa** từ `Account` sang `CustomerAccount` và `StaffAccount`."*
- 👉 **Chỉ hình**: Chỉ vào kim cương đen Composition và kim cương trắng Aggregation.
- 💡 **Chốt chặn (Nếu Thầy vặn tại sao không vẽ khóa ngoại ID?)**: *"Domain Model mô hình hóa quan hệ bằng tham chiếu đối tượng (Association), không dùng khóa ngoại dạng cột ID như CSDL vật lý."*

---

### [Slide 37] Biểu Đồ Gói – Package Diagram (15s)
- 🎙️ **Nói nhanh**: *"Slide 37 là Biểu đồ Gói tổ chức mã nguồn thành 5 tầng kiến trúc: `<<user interface>>` $\rightarrow$ `<<application>>` $\rightarrow$ `<<domain>>` (5 gói nghiệp vụ) $\rightarrow$ `<<infrastructure>>` $\rightarrow$ `<<database>>`. Phụ thuộc một chiều từ trên xuống, không có phụ thuộc vòng."*
- 👉 **Chỉ hình**: Chỉ vào chiều mũi tên nét đứt phụ thuộc một chiều.

---

### [Slide 38] Biểu Đồ Triển Khai – Deployment Diagram (20s)
- 🎙️ **Nói nhanh**: *"Slide 38 là Biểu đồ Triển khai 3-Tier Enterprise:*
  - *Máy trạm Lễ tân kết nối máy in nhiệt POS qua cáp `USB 2.0 / TCP Port 9100` để in hóa đơn tức thì < 0.5s kể cả khi mất Internet.*
  - *Máy chủ trung tâm chạy **Nginx Reverse Proxy** (TLS 1.3, mạng nội bộ `VLAN 20`, WebSocket WSS), môi trường **Python WSGI**, và **Cron Daemon** ngầm dọn phòng quá hạn 15 phút.*
  - *CSDL nằm trong phân vùng an toàn `Dedicated DB Subnet`."*
- 👉 **Chỉ hình**: Chỉ vào cáp USB máy in, Nginx, Cron daemon và Database Subnet.

---

### [Slide 39 - 44] Khối 6 Biểu Đồ Thành Phần – Component Diagrams (30s)
- 🎙️ **Nói nhanh**: *"Từ Slide 39 đến 44 là Khối Biểu đồ Thành phần chứng minh kiến trúc mô-đun hóa độc lập có thể thay thế được (`<<executable>>`, `<<component>>`, `<<library>>`, `<<database>>`):*
  - *Slide 39 là kiến trúc tổng quát phân tách giao diện và nghiệp vụ.*
  - *Slide 40 đến 44 là 5 quy trình độc lập: Đặt phòng giữ tồn 15m, Nhận phòng gán phòng sạch, Ghi nhận dịch vụ và tính lại hóa đơn, Trả phòng quyết toán, và Vệ sinh buồng phòng di động."*
- 👉 **Chỉ hình**: Bấm clicker lướt nhịp nhàng qua từng slide từ 39 đến 44.

---

### [Slide 45] Thiết Kế Dữ Liệu – 15 Bảng Chuẩn Hóa 3NF (25s)
- 🎙️ **Nói nhanh**: *"Slide 45 là mô hình CSDL quan hệ 15 bảng đạt chuẩn **3NF thuần khiết**, xóa bỏ hoàn toàn God-table `New_Bookings`:*
  - *Tách biệt `T_RoomType` và `T_PhysicalRoom` để quản lý chính xác 14 phòng vật lý.*
  - *Tách biệt `T_Booking` và `T_BookingNight` giúp quản lý giá phòng linh hoạt từng đêm, hỗ trợ đổi phòng giữa chừng (Split Stay) và tối ưu đếm phòng trống bằng phép `COUNT(*)` cực nhanh.*
  - *Bảng `T_RoomHoldLock` lưu phiên giữ chỗ 15m chống Race Condition; và sổ nợ `T_FolioInvoice` độc lập.*
  - *Hệ thống đã vượt qua trọn vẹn **43/43 tests tự động đạt 100%**."*
- 👉 **Chỉ hình**: Chỉ vào cặp bảng RoomType vs PhysicalRoom, Booking vs BookingNight, và FolioInvoice.
- 💡 **Chốt chặn (Nếu Thầy vặn chứng minh 3NF?)**: *"1NF: Không có thuộc tính đa trị; 2NF: Khóa đơn nightId phụ thuộc hàm toàn phần; 3NF: Không phụ thuộc bắc cầu qua thuộc tính không khóa."*

---

# PHẦN III: GIAO DIỆN THỰC TẾ & KẾT LUẬN (SLIDE 46 - 52)
*(Lướt nhanh trong 1.0 phút)*

### [Slide 46 - 51] Minh Chứng Giao Diện Thực Tế (40s)
- 🎙️ **Nói nhanh**: *"Từ Slide 46 đến 51 là minh chứng giao diện thực tế phong cách Coastal Luxury 5 sao tương ứng với các biểu đồ:*
  - *Slide 46: Trang chủ tìm kiếm phòng.*
  - *Slide 47: Đăng ký, đăng nhập RBAC.*
  - *Slide 48: Tra cứu phòng trống thời gian thực.*
  - *Slide 49: Màn hình giữ phòng đếm ngược 15:00 và mã VietQR (hiện thực hóa SD-01).*
  - *Slide 50: Lịch sử đơn và thẻ hội viên VIP Gold.*
  - *Slide 51: Modal tính toán hoàn cọc bậc thang tự động (hiện thực hóa SD-06)."*

### [Slide 52] Lời Cảm Ơn & Kết Thúc (15s)
- 🎙️ **Nói nhanh**:
  > *"Kính thưa Quý Thầy/Cô, toàn bộ 52 slide đã thể hiện sự nhất quán và chặt chẽ từ khảo sát nghiệp vụ Côn Đảo đến 28 biểu đồ kiến trúc và giao diện chạy thực tế.*
  >
  > *Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe và xin trân trọng kính mời Hội đồng đặt câu hỏi phản biện ạ!"*
