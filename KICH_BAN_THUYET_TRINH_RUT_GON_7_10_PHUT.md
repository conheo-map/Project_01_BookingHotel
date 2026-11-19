# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN OOAD (PHIÊN BẢN RÚT GỌN 08 - 10 PHÚT)
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO RESORT
> **Mục tiêu**: Báo cáo súc tích, đĩnh đạc, đúng giờ (chuông reo 10 phút), làm nổi bật các đột phá kiến trúc và triệt tiêu mọi rủi ro bị Hội đồng bắt bẻ.  
> **Tài liệu bản vẽ tham chiếu**: Tệp [Tong_hop_bieu_do_(1).drawio](file:///C:/HocC/Project_Booking%20-%20Sao%20ch%C3%A9p/Tong_hop_bieu_do_(1).drawio) (28 biểu đồ hoàn chỉnh).

---

## ⏱️ MA TRẬN PHÂN BỔ THỜI GIAN "VÀNG" (TỔNG: 09 PHÚT)

```
[00:00 - 01:00] (01 phút) : Mở đầu & 3 Thách thức đặc thù biển đảo Côn Đảo
[01:00 - 02:30] (1.5 phút): Cụm 1: Khối Use Case (Mô hình hóa chức năng & Phân rã) -> Tab 1 đến 6
[02:30 - 04:00] (1.5 phút): Cụm 2: Khối Hoạt động (Dòng chảy nghiệp vụ đa làn Swimlanes) -> Tab 7 đến 12
[04:00 - 06:30] (2.5 phút): Cụm 3: Khối Trình tự BCE (Trọng tâm tương tác đối tượng) -> Tab 13 đến 18
[06:30 - 07:45] (1.25 phút): Cụm 4: Cấu trúc Tĩnh, Gói & Triển khai 3-Tier -> Tab 19, 20, 21
[07:45 - 08:30] (0.75 phút): Cụm 5: Khối Thành phần (Component) & CSDL Chuẩn 3NF -> Tab 22 đến 28
[08:30 - 09:00] (0.5 phút) : Kết luận & Mời Hội đồng phản biện
```

---

## LỜI THOẠI THUYẾT TRÌNH CHI TIẾT (WORD-BY-WORD SCRIPT)

---

### PHẦN 1: MỞ ĐẦU & BỐI CẢNH BÀI TOÁN (01 PHÚT)
- ⏱️ **Thời gian**: `00:00 - 01:00`
- 👉 **Hành động**: Chào Hội đồng, đứng thẳng tự tin, bật Slide bìa và slide bài toán Côn Đảo.

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Quý Thầy/Cô trong Hội đồng và các bạn sinh viên,*
>
> *Em xin đại diện nhóm báo cáo đồ án Phân tích & Thiết kế Hệ thống Hướng đối tượng (OOAD) với đề tài: **Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo Resort**.*
>
> *Khách sạn Sài Gòn - Côn Đảo là resort 4-5 sao cao cấp của Saigontourist Group tại hải đảo biệt lập. Khác với khách sạn thông thường trong đất liền, nghiệp vụ tại đây đối mặt với **3 bài toán sống còn**:*
> 1. ***Tranh chấp phòng cùng thời điểm (Race Condition)**: Du khách thường dồn dập đặt phòng khi hãng mở bán vé máy bay/tàu cao tốc ra đảo, dễ gây bán vượt số phòng thực tế (**Overbooking**).*
> 2. ***Sự tách biệt giữa Loại phòng thương mại (Room Type) và Phòng vật lý thực tế (Physical Room)**: Khách trên mạng chỉ đặt loại phòng; việc gán số phòng cụ thể (như Villa 01, P.205) chỉ diễn ra khi check-in tại quầy theo tiến độ dọn phòng sạch thời gian thực.*
> 3. ***Quản trị Sổ cái Folio chi tiêu tập trung & Cơ chế hoàn cọc bậc thang**: Hạch toán toàn bộ minibar, tour đảo vào sổ nợ Folio thống nhất; và tự động hoàn tiền theo số giờ trước check-in khi biển động bão gió.*
>
> *Hệ thống đã được nhóm mô hình hóa hoàn chỉnh thành **28 biểu đồ chuẩn UML 2.5**, ứng dụng mẫu phân tích **3 Tầng BCE**, chuẩn hóa dữ liệu **3NF**, và kiểm thử thực tế với **43/43 tests tự động đạt 100%**."*

---

### PHẦN 2: CỤM USE CASE - MÔ HÌNH HÓA CHỨC NĂNG (1.5 PHÚT)
- ⏱️ **Thời gian**: `01:00 - 02:30`
- 👉 **Hành động**: Mở Tab 1 (`Biểu đồ UC tổng quát`) và lướt nhanh qua Tab 2 đến 6.

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Thầy/Cô, tại **Biểu đồ Use Case Tổng quát (Tab 1)**:*
> - *Hệ thống phân định rõ **5 Tác nhân người dùng**: Khách hàng B2C, Lễ tân tiền sảnh, Nhân viên buồng phòng, Quản lý Resort và Quản trị viên Admin; cùng **2 Tác nhân ngoại vi**: Cổng thanh toán VNPay và Máy chủ chạy nền Cron System.*
> - *Toàn bộ 15 Use Case cốt lõi được đóng khung trọn vẹn trong Ranh giới hệ thống (System Boundary).*
>
> 👉 *[Chỉ vào các quan hệ include/extend trên Tab 2 đến 6]*:
> *Về mặt học thuật, nhóm tuân thủ tuyệt đối quy chuẩn UML 2.5:*
> - ***Quan hệ `<<include>>` (Bắt buộc, mũi tên trỏ thuận)**: Use Case 'Đặt phòng trực tuyến' bắt buộc phải `<<include>>` 'Khóa phòng chống trùng 15 phút' và 'Xác thực cổng thanh toán'. Không thể có đơn đặt phòng thành công mà bỏ qua việc giữ chỗ và thanh toán.*
> - ***Quan hệ `<<extend>>` (Có điều kiện, mũi tên trỏ ngược)**: Use Case 'Áp dụng Voucher' mở rộng cho 'Đặt phòng' tại Extension Point `[Có mã ưu đãi]`; 'Hủy đặt phòng & Hoàn tiền' mở rộng cho 'Lịch sử đơn' khi đơn thỏa mãn điều kiện trước giờ check-in.*
> - *Tại phân hệ Quản lý và Tiền sảnh, hệ thống phân rã chi tiết quy trình tiếp nhận khách Walk-in tại quầy, quản trị sơ đồ Gantt thời gian thực và xử lý khách vắng mặt (No-Show)."*

---

### PHẦN 3: CỤM HOẠT ĐỘNG - DÒNG CHẢY NGHIỆP VỤ ĐA LÀN (1.5 PHÚT)
- ⏱️ **Thời gian**: `02:30 - 04:00`
- 👉 **Hành động**: Mở Tab 7 (`AD-01 Đặt phòng`), chuyển nhanh qua Tab 8 (`AD-02 Check-in`), Tab 10 (`AD-04 Check-out`) và Tab 12 (`AD-06 Hủy phòng`).

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Thầy/Cô, bộ 06 Biểu đồ Hoạt động (Activity Diagrams) mô hình hóa dòng chảy điều khiển qua các làn bơi **Swimlanes**:*
>
> 👉 *[Chỉ vào AD-01: Đặt phòng & Khóa giữ 15 phút - Tab 7]*:
> - *Khi khách chọn phòng $\rightarrow$ Hệ thống kiểm tra quỹ tồn. Nếu còn phòng, hệ thống lập tức thực thi **Tạo Hold Lock 15 phút** $\rightarrow$ điều hướng sang cổng VNPay.*
> - *Thanh phân nhánh **Fork** kích hoạt 2 luồng song song: Một luồng chờ Webhook IPN thanh toán, một luồng khởi động bộ đếm Timer 15 phút.*
> - *Tại thanh **Join**: Nếu thanh toán thành công trong 15 phút $\rightarrow$ Xác nhận Booking chính thức. Nếu quá 15 phút mà chưa thanh toán $\rightarrow$ Timer lập tức giải phóng phòng giữ chỗ về kho chung.*
>
> 👉 *[Chỉ vào AD-02, AD-04, AD-06]*:
> - *Tại **AD-02 (Check-in)**: Lễ tân chỉ được gán các phòng vật lý có trạng thái `CLEAN` (đã dọn sạch) và `VACANT` (trống lịch).*
> - *Tại **AD-04 (Check-out)**: Nút rẽ nhánh kiểm soát chặt chẽ điều kiện bảo vệ **`[Công nợ bằng 0?]`** $\rightarrow$ Hệ thống mới cho phép đóng Folio, xuất hóa đơn VAT Saigontourist và tự động chuyển phòng sang `DIRTY` (chờ dọn).*
> - *Tại **AD-06 (Hủy phòng)**: Tính toán tiền hoàn bậc thang (100% trước 72h, 50% từ 24-72h, 0% dưới 24h). Nếu giao dịch gặp sự cố, hệ thống có nhánh **Rollback hoàn tác** để bảo toàn tính toàn vẹn dữ liệu."*

---

### PHẦN 4: CỤM TRÌNH TỰ BCE - TRỌNG TÂM THIẾT KẾ ĐỘNG (2.5 PHÚT)
- ⏱️ **Thời gian**: `04:00 - 06:30`
- 👉 **Hành động**: Mở Tab 13 (`SD-01 Đặt phòng`), sau đó chuyển qua Tab 14 (`SD-02 Check-in`), Tab 15 (`SD-03 Folio`), Tab 16 (`SD-04 Check-out`), Tab 17 (`SD-05 Buồng phòng`), Tab 18 (`SD-06 Hủy phòng`).

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Thầy/Cô, đây là **trọng tâm kiến trúc hướng đối tượng** của đồ án. Toàn bộ 6 biểu đồ tuần tự được xây dựng theo chuẩn **BCE (Boundary - Control - Entity)** với quy tắc vàng: **CẤM NHẢY CÓC**. Boundary không được gọi thẳng vào Entity; mọi trao đổi đều phải qua tầng Control điều phối. Tất cả Sync Call đều có vạch kích hoạt đối xứng với Return Message nét đứt:*
>
> 1. ***SD-01 (Đặt phòng trực tuyến - Tab 13)**: Khách gửi yêu cầu qua Boundary `:SearchBookingUI` $\rightarrow$ Tầng điều khiển `:BookingService` gọi `:RoomInventory` tạo khóa tạm `createHoldLock(expiresAt = now + 15m)`. Khách quét mã VietQR $\rightarrow$ VNPay gửi Webhook IPN $\rightarrow$ `:BookingService` tạo `:Booking` trạng thái `CONFIRMED`, sinh các đêm `:BookingNight`, và gọi hàm `markLockAsSold` chuyển khóa tạm sang ĐÃ BÁN vĩnh viễn.*
> 2. ***SD-02 (Check-in tiền sảnh - Tab 14)**: Lễ tân tra cứu PNR $\rightarrow$ quét CCCD khách $\rightarrow$ `:CheckInController` gọi `:PhysicalRoom` kiểm tra phòng sạch `checkCleanRooms(status='CLEAN')` $\rightarrow$ Gán phòng vật lý `assignPhysicalRoom` vào từng đêm và đổi trạng thái phòng sang `OCCUPIED`.*
> 3. ***SD-03 (Dịch vụ phát sinh - Tab 15)**: Nhân viên nhập minibar $\rightarrow$ `:FolioBillingService` xác thực phòng đang lưu trú $\rightarrow$ tính thuế VAT $\rightarrow$ lưu chi tiết `:FolioItem` và gọi `postChargeToFolio` cộng dồn số dư nợ phòng.*
> 4. ***SD-04 (Check-out & Hóa đơn VAT - Tab 16)**: Hệ thống tính công nợ: $\text{Số dư} = \text{Tiền phòng} + \text{Dịch vụ} - \text{Cọc}$. Lễ tân thu tiền thiếu $\rightarrow$ xuất hóa đơn GTGT điện tử Saigontourist Group (MST `0312456789-001`), đóng Folio và ngay lập tức gửi lệnh đổi phòng `:PhysicalRoom` sang `DIRTY`.*
> 5. ***SD-05 (Vận hành buồng phòng - Tab 17)**: Nhân viên dùng Mobile Web PWA nhận phòng `DIRTY` $\rightarrow$ đổi sang `CLEANING` $\rightarrow$ dọn xong chuyển sang `CLEAN` $\rightarrow$ **Hệ thống bắn WebSocket Event `notifyRoomStatus`** giúp sơ đồ phòng tại quầy lễ tân tự động đổi màu xanh tức thì mà không cần gọi bộ đàm.*
> 6. ***SD-06 (Hủy phòng bậc thang - Tab 18)**: `:BookingCancellationService` gọi `:RefundPolicy` tính số giờ trước check-in $\rightarrow$ áp dụng tỷ lệ hoàn tiền $\rightarrow$ ghi chứng từ hoàn tiền âm (`-refundAmount`) và thực thi hàm then chốt **`releaseBookedNights`** để mở lại phòng trống ngay lập tức trên website."*

---

### PHẦN 5: CỤM CẤU TRÚC TĨNH, GÓI & TRIỂN KHAI 3-TIER (1.25 PHÚT)
- ⏱️ **Thời gian**: `06:30 - 07:45`
- 👉 **Hành động**: Mở Tab 19 (`Lớp lĩnh vực`), Tab 20 (`Biểu đồ gói`), và Tab 21 (`Biểu đồ triển khai`).

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Thầy/Cô:*
>
> 👉 *[Tab 19: Biểu đồ Lớp Lĩnh vực]*:
> *Mỗi lớp được thiết kế 3 ngăn chuẩn mực theo nguyên lý **Information Expert**: Chỉ chứa phương thức tính toán nghiệp vụ thuần túy (`tinhTongTien()`, `kiemTraConPhong()`), không rò rỉ mã hạ tầng SQL. Mối quan hệ **Hợp thành (Composition $\blacklozenge$)** sinh tử giữa `BookingMaster` và `BookingNight`, giữa `ServiceFolio` và `FolioItem`; quan hệ **Thu nạp (Aggregation $\diamondsuit$)** giữa `Hotel` $\rightarrow$ `RoomType` $\rightarrow$ `PhysicalRoom`; và quan hệ **Kế thừa** từ `Account` sang `CustomerAccount` / `StaffAccount`.*
>
> 👉 *[Tab 20: Biểu đồ Gói]*:
> *Tổ chức mã nguồn thành 5 tầng kiến trúc: `<<user interface>>` $\rightarrow$ `<<application>>` $\rightarrow$ `<<domain>>` (5 gói nghiệp vụ lõi) $\rightarrow$ `<<infrastructure>>` $\rightarrow$ `<<database>>`. Phụ thuộc một chiều từ trên xuống, không có phụ thuộc vòng.*
>
> 👉 *[Tab 21: Biểu đồ Triển khai 3-Tier Enterprise]*:
> - **Tầng 1 (Client Tier)**: Thiết bị khách hàng B2C, Mobile buồng phòng (Web PWA), và Máy trạm Lễ tân (nối máy in nhiệt POS qua cổng `USB 2.0 / TCP Port 9100` để in bill tức thì < 0.5s kể cả khi mất Internet hải đảo).*
> - **Tầng 2 (Application Server Tier)**: Máy chủ Ubuntu Linux với **Nginx Reverse Proxy** (mã hóa `TLS 1.3/HTTPS Port 443`, mạng nội bộ `VLAN 20`, kết nối WebSocket WSS thời gian thực), môi trường **Python WSGI Container**, và **Cron Daemon** ngầm (`cron_worker.py`) chuyên dọn dẹp các phiên giữ phòng quá hạn 15 phút.*
> - **Tầng 3 (Data & External Tier)**: Máy chủ CSDL trong phân vùng mạng an toàn (`Dedicated DB Subnet`), kết nối Cổng VNPay (REST/IPN) và Cổng Mail điện toán đám mây (SMTP Port 587)."*

---

### PHẦN 6: CỤM THÀNH PHẦN & CSDL CHUẨN 3NF (0.75 PHÚT)
- ⏱️ **Thời gian**: `07:45 - 08:30`
- 👉 **Hành động**: Lướt qua Tab 22 (`Component tổng quát`), dừng lại ở Tab 28 (`Thiết kế dữ liệu`).

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Thầy/Cô:*
> - *Tại **Khối Biểu đồ Thành phần (Tab 22 - 27)**: Hệ thống chứng minh kiến trúc mô-đun hóa cao, tách biệt Ứng dụng giao diện (`<<executable>>`), Mô-đun giao tiếp, Ứng dụng nghiệp vụ và Thư viện truy cập dữ liệu.*
> - *Tại **Biểu đồ Thiết kế Dữ liệu (Tab 28)**: Hệ thống chuẩn hóa quan hệ **15 bảng đạt chuẩn 3NF thuần khiết**, xóa bỏ hoàn toàn God-table `New_Bookings`:*
>   * *Tách biệt `T_RoomType` và `T_PhysicalRoom` để quản lý chính xác 14 phòng vật lý.*
>   * *Tách biệt `T_Booking` và `T_BookingNight` giúp quản lý giá phòng linh hoạt từng đêm, hỗ trợ đổi phòng giữa kỳ lưu trú (Split Stay) và tối ưu phép đếm phòng trống bằng `COUNT(*)`.*
>   * *Tài khoản `T_FolioInvoice` độc lập giúp hạch toán các dịch vụ minibar phát sinh minh bạch theo chuẩn kế toán khách sạn quốc tế.*
>   * *Bảng `T_RoomHoldLock` lưu vết phiên giữ phòng chống Race Condition.*
> - *Hệ thống đã vượt qua trọn vẹn **43/43 tests tự động (100% Passing)** từ Domain Models đến E2E Full Lifecycle."*

---

### PHẦN 7: LỜI KẾT & MỜI HỘI ĐỒNG PHẢN BIỆN (0.5 PHÚT)
- ⏱️ **Thời gian**: `08:30 - 09:00`
- 👉 **Hành động**: Chuyển slide Cảm ơn, nhìn thẳng Hội đồng, mỉm cười và cúi chào.

🎙️ **[LỜI THOẠI]**:
> *"Kính thưa Quý Thầy/Cô trong Hội đồng,*
>
> *Thông qua toàn bộ 28 biểu đồ kiến trúc, nhóm chúng em đã giải quyết trọn vẹn các thách thức đặc thù của Khách sạn Sài Gòn - Côn Đảo Resort từ góc độ chức năng, quy trình hoạt động, tương tác đối tượng đến cơ sở dữ liệu 3NF và hạ tầng triển khai thực tế.*
>
> *Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe bài báo cáo của nhóm.*
>
> *Em xin trân trọng kính mời Thầy/Cô đặt câu hỏi phản biện để chúng em được làm rõ thêm đề tài ạ!"*

---

## ⚡ BÍ KÍP PHẢN XẠ NHANH: TOP 5 CÂU HỎI "TỬ HUYỆT" HỘI ĐỒNG (TRẢ LỜI TRONG 30 GIÂY)

### 1. "Tại sao dùng BCE mà cấm Boundary gọi thẳng Entity?"
> 🎙️ **Đáp ngay**: *"Dạ thưa Thầy, để đảm bảo nguyên lý **Low Coupling & Information Hiding**. Boundary chỉ lo hiển thị, Entity chỉ lo dữ liệu. Mọi luật kiểm tra nghiệp vụ và quản lý giao dịch Transaction phải do tầng Control điều phối. Nhờ đó khi thay đổi giao diện từ Web sang Mobile App, toàn bộ tầng nghiệp vụ và dữ liệu Entity được tái sử dụng nguyên vẹn 100%."*

### 2. "Cơ chế khóa phòng 15 phút xử lý thế nào khi 2 người cùng bấm đặt 1 phòng trong cùng 1 tích tắc?"
> 🎙️ **Đáp ngay**: *"Dạ thưa Thầy, hệ thống áp dụng cơ chế **Pessimistic Hold with TTL (15 phút)** bọc trong một Database Transaction nguyên tử. Ai chạm CSDL trước mili-giây sẽ tạo được bản ghi trong bảng `T_RoomHoldLock` với `expiresAt = now + 15m`. Ai đến sau nhận kết quả phòng khả dụng bằng 0 và báo phòng đang được giữ chỗ. Daemon `cron_worker.py` sẽ tự động nhả phòng nếu quá hạn."*

### 3. "Tại sao phải tách `T_Booking` và `T_BookingNight`? Có phải chuẩn hóa 3NF không?"
> 🎙️ **Đáp ngay**: *"Dạ thưa Thầy, đúng ạ! Đây là chuẩn hóa 3NF kinh điển. Nếu lưu chung ngày đến/ngày đi, khi khách ở nhiều đêm và đổi phòng giữa chừng (Split Stay) thì thuộc tính `idPhysicalRoom` sẽ bị đa trị (vi phạm 1NF). Tách `T_BookingNight` giúp quản lý giá phòng linh hoạt từng đêm và chuyển câu truy vấn tìm phòng trống thành phép đếm `COUNT(*)` cực nhanh có Index hỗ trợ."*

### 4. "Tại sao máy in nhiệt POS lại nối cáp USB trực tiếp vào máy trạm lễ tân mà không in qua Cloud?"
> 🎙️ **Đáp ngay**: *"Dạ thưa Thầy, ngoài Côn Đảo mạng Internet thường bị chập chờn khi có bão gió. Kết nối trực tiếp cổng USB 2.0 / TCP 9100 nội bộ giúp máy trạm gửi lệnh in ESC/POS tức thì dưới 0.5 giây, đảm bảo quầy tiền sảnh luôn vận hành liên tục không bao giờ bị tê liệt."*

### 5. "Phân biệt `<<include>>` và `<<extend>>` trên biểu đồ Use Case?"
> 🎙️ **Đáp ngay**: *"Dạ thưa Thầy:
> - `<<include>>` là phụ thuộc bắt buộc: Use Case nguồn gọi Use Case đích, mũi tên nét đứt trỏ **thuận** (ví dụ: 'Đặt phòng' bắt buộc include 'Khóa phòng 15 phút').
> - `<<extend>>` là mở rộng tùy chọn tại Extension Point khi thỏa mãn điều kiện, mũi tên nét đứt trỏ **ngược** về Use Case cơ sở (ví dụ: 'Áp dụng Voucher' extend 'Đặt phòng' khi có mã ưu đãi)."*
