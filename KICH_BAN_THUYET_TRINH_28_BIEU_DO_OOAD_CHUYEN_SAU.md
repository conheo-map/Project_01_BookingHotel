# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN OOAD CHUYÊN SÂU: TOÀN BỘ 28 BIỂU ĐỒ HỆ THỐNG
## DỰ ÁN: HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO RESORT
> **Tài liệu tham chiếu chuẩn**: Tệp bản vẽ thiết kế `Tong_hop_bieu_do_(1).drawio` (gồm đúng 28 biểu đồ hoàn chỉnh)  
> **Quy chuẩn chuyên môn**: Phân tích Thiết kế Hệ thống Hướng đối tượng (OOAD) theo Rational Unified Process (RUP) & UML 2.5 Standard  
> **Bộ giáp phòng thủ học thuật**: Kiến thức cốt lõi giải thích tận gốc rễ lý thuyết, dập tắt mọi câu hỏi "vặn vẹo" của Hội đồng phản biện.

---

# MỤC LỤC 28 BIỂU ĐỒ THEO THỨ TỰ TRONG FILE DRAW.IO

| STT | Tên Biểu Đồ trong Draw.io | Thể Loại Biểu Đồ | Phân Hệ / Phạm Vi |
| :---: | :--- | :--- | :--- |
| **01** | `Biểu đồ UC tổng quát` | Use Case Diagram | Toàn bộ 5 vai trò & Ranh giới hệ thống |
| **02** | `Biểu đồ phân rã đạt phòng` | Use Case Detail | Phân hệ Đặt phòng B2C, Khóa phòng & Hủy phòng |
| **03** | `Biểu đồ phân rã quản lý tài khoản` | Use Case Detail | Phân hệ Tài khoản, Phân quyền RBAC & Audit Log |
| **04** | `Biểu đồ phân rã làm thủ tục` | Use Case Detail | Phân hệ Lễ tân: Walk-in, Check-in, Folio, Check-out, Gantt |
| **05** | `Biểu đồ phân rã vận hành buồng phòng` | Use Case Detail | Phân hệ Buồng phòng: Nhận việc, Nghiệm thu, Bảo trì |
| **06** | `Biểu đồ phân rã quản trị doanh thu` | Use Case Detail | Phân hệ Quản lý: Giá linh hoạt, Voucher, Báo cáo KPI |
| **07** | `Biểu đồ hoạt động đặt phòng trực tuyến` | Activity Diagram (AD-01) | Đặt phòng B2C & Khóa giữ phòng 15 phút (Fork/Join, Timer) |
| **08** | `Biểu đồ hoạt động Check-in và gán phòng vật lý động` | Activity Diagram (AD-02) | Check-in khách đặt trước & Walk-in, Gán phòng CLEAN |
| **09** | `Biểu đồ hoạt động sử dụng dịch vụ và ghi chi tiêu vào Folio` | Activity Diagram (AD-03) | Tiêu dùng minibar/dịch vụ & Hạch toán nợ Folio phòng |
| **10** | `Biểu đồ hoạt động trả phòng, kiểm kê và quyết toán Folio` | Activity Diagram (AD-04) | Trả phòng, đối chiếu kiểm kê, tất toán nợ & Đổi DIRTY |
| **11** | `Biểu đồ hoạt động dọn buồng phòng và xử lý bảo trì` | Activity Diagram (AD-05) | Quy trình dọn buồng qua Mobile PWA, Sự cố kỹ thuật |
| **12** | `Biểu đồ hoạt động hủy phòng` | Activity Diagram (AD-06) | Hủy đơn trực tuyến, Tính hoàn tiền bậc thang, Rollback |
| **13** | `Biểu đồ trình tự đặt phòng` | Sequence BCE (SD-01) | Đặt phòng B2C, Hold Lock 15m, VietQR, IPN Webhook |
| **14** | `Biểu đồ trình tự check-in` | Sequence BCE (SD-02) | Check-in, Quét CCCD, Lọc phòng sạch, Gán phòng OCCUPIED |
| **15** | `Biểu đồ trình tự dịch vụ phát sinh` | Sequence BCE (SD-03) | Ghi nhận tiêu dùng dịch vụ buồng phòng vào Folio |
| **16** | `Biểu đồ trình tự check-out` | Sequence BCE (SD-04) | Check-out, Tính nợ, Xuất hóa đơn VAT Saigontourist, DIRTY |
| **17** | `Biểu đồ trình tự dọn dẹp` | Sequence BCE (SD-05) | Vận hành dọn dẹp, Bấm giờ ca dọn, Bắn WebSocket CLEAN |
| **18** | `Biểu đồ trình tự hủy phòng` | Sequence BCE (SD-06) | Hủy phòng, Tính phạt cọc trước 14:00, Giải phóng Nights |
| **19** | `Biểu đồ lớp lĩnh vực` | Domain Class Diagram | 3 ngăn, Nguyên lý Information Expert, Composition, Multiplicity |
| **20** | `Biểu đồ gói` | Package Diagram | 5 Tầng: UI, Application, Domain, Infrastructure, Database |
| **21** | `Biểu đồ triển khai` | Deployment Diagram | 3-Tier Enterprise: Client, App Server (Nginx/WSGI/Cron), DB |
| **22** | `Biểu đồ thành phần tổng quát` | Component Diagram | Tổng thể kiến trúc Module giao tiếp, Nghiệp vụ & Data Access |
| **23** | `Biểu đồ thành phần đặt phòng trực tuyến` | Component Diagram | Module Đặt phòng, Giữ tồn phòng 15m, Xác nhận thanh toán |
| **24** | `Biểu đồ thành phần nhận phòng và gán phòng vật lý` | Component Diagram | Module Tiếp nhận, Gán phòng sạch, Cập nhật trạng thái |
| **25** | `Biểu đồ thành phần dịch vụ phát sinh` | Component Diagram | Module Ghi phát sinh tại quầy, Tính lại số dư hóa đơn |
| **26** | `Biểu đồ thành phần check out` | Component Diagram | Module Màn hình quyết toán, Chốt đặt phòng, Đổi phòng chờ dọn |
| **27** | `Biểu đồ thành phần vệ sinh buồng phòng` | Component Diagram | Module Màn hình buồng phòng, Nhận việc, Xác nhận phòng sạch |
| **28** | `Thiết kế dữ liệu` | UML Database Design | 15 Bảng chuẩn hóa 3NF, Khóa PK/FK, Ràng buộc Unique/Index |

---

# CHI TIẾT KỊCH BẢN THUYẾT TRÌNH TỪNG BIỂU ĐỒ (TỪ DIAGRAM 1 ĐẾN 28)

---

## DIAGRAM 1: BIỂU ĐỒ UC TỔNG QUÁT
- **Tên Tab trong Draw.io**: `Biểu đồ UC tổng quát`
- **Mục tiêu**: Định nghĩa phạm vi ranh giới hệ thống (System Boundary) và phân định trách nhiệm của 5 Tác nhân người dùng và 2 Tác nhân hệ thống.

### 🎙️ Lời thoại thuyết trình:
> *"Kính thưa Thầy/Cô, mở đầu hồ sơ thiết kế là **Biểu đồ Use Case Tổng quát** của Hệ thống Quản lý và Đặt phòng Sài Gòn - Côn Đảo Resort.*
>
> 👉 *[Chỉ vào các Actor phía ngoài ranh giới]*:
> *Về mặt tác nhân, hệ thống xác định 5 tác nhân người dùng và 2 tác nhân hỗ trợ:*
> 1. **Khách hàng (Customer)**: Đặt phòng trực tuyến, quản lý giỏ hàng đa phòng, hủy phòng hoàn cọc, đăng ký hội viên VIP.
> 2. **Nhân viên Lễ tân (Receptionist)**: Tiếp nhận khách Walk-in tại quầy, làm thủ tục Check-in/Check-out, điều chuyển phòng, ghi nhận dịch vụ phát sinh, quản trị sơ đồ Gantt và xử lý khách vắng mặt (No-Show).
> 3. **Nhân viên Buồng phòng (Housekeeper)**: Tiếp nhận danh sách phòng bẩn, cập nhật tiến độ dọn buồng và báo cáo sự cố hư hỏng vật tư.
> 4. **Quản lý Resort (Manager)**: Thiết lập giá phòng linh hoạt theo mùa, quản lý Voucher khuyến mãi, theo dõi báo cáo doanh thu và phân tích chỉ số KPI (RevPAR, ADR).
> 5. **Quản trị viên Hệ thống (Admin)**: Phân quyền vai trò RBAC, quản lý danh mục phòng và cấu hình an ninh hệ thống.
> 6. *Hai tác nhân hệ thống bên ngoài: **Cổng thanh toán VNPay** (xác thực giao dịch tài chính) và **Máy chủ chạy nền Cron System** (tự động quét dọn các phiên giữ phòng quá hạn).*
>
> 👉 *[Chỉ vào Ranh giới hệ thống]*:
> *Ranh giới hệ thống (System Boundary) bao bọc trọn vẹn 15 Use Case nghiệp vụ cốt lõi, đảm bảo nguyên tắc: Không để tác nhân nằm trong ranh giới, và các Use Case phải mang lại giá trị trọn vẹn (Business Value) cho người dùng."*

### 🛡️ Kiến thức phòng thủ chống Thầy vặn:
- **Thầy hỏi**: *"Tại sao Cổng thanh toán và Máy chủ chạy nền (Cron) lại được vẽ là Actor hình que (Stick man)?"*
- **Đáp đanh thép**: *"Thưa Thầy, theo chuẩn UML 2.5 của OMG, Actor đại diện cho bất kỳ thực thể nào **nằm ngoài ranh giới hệ thống** tương tác trực tiếp với hệ thống để trao đổi thông tin. Cổng thanh toán là hệ thống bên thứ ba đóng vai trò Secondary Actor gửi tín hiệu Webhook IPN; còn Cron System là tác nhân ngoại vi kích hoạt tiến trình theo chu kỳ thời gian. UML cho phép dùng stereotype `<<system>>` hoặc vẽ hình que có nhãn tên rõ ràng."*

---

## DIAGRAM 2: BIỂU ĐỒ PHÂN RÃ ĐẶT PHÒNG
- **Tên Tab trong Draw.io**: `Biểu đồ phân rã đạt phòng`
- **Mục tiêu**: Bóc tách chi tiết nghiệp vụ Đặt phòng B2C, cơ chế khóa giữ phòng và hoàn tiền.

### 🎙️ Lời thoại thuyết trình:
> *"Tại phân hệ **Đặt phòng Trực tuyến B2C**:*
> - *Use Case trung tâm là **'Đặt phòng trực tuyến (B2C)'** do Khách hàng khởi phát.*
> - *Để hoàn tất việc đặt phòng, Use Case này bắt buộc phải **`<<include>>`** 3 Use Case con:*
>   1. **'Khóa phòng chống trùng (Hold Lock 15 phút)'**: Ngay khi khách chọn phòng, hệ thống lập tức tạm khóa để chống bán trùng phòng (Overbooking).*
>   2. **'Tính báo giá và phụ thu sức chứa'**: Tự động tính tiền phòng dựa trên số lượng người lớn, trẻ em và phụ thu nệm phụ.*
>   3. **'Xác thực cổng thanh toán'**: Kết nối sang VNPay để tạo giao dịch thanh toán trực tuyến.*
> - *Hai Use Case mở rộng theo điều kiện **`<<extend>>`**:*
>   1. **'Áp dụng mã giảm giá (Voucher)'**: Chỉ chạy khi khách hàng sở hữu mã ưu đãi hợp lệ.*
>   2. **'Gợi ý đặt phòng ghép phân đoạn (Split Stay)'**: Kích hoạt khi khách ở nhiều đêm nhưng không có một phòng đơn lẻ nào trống suốt toàn bộ kỳ nghỉ.*
> - *Song song đó, máy chủ Cron độc lập kích hoạt Use Case **'Quét dọn phiên giữ phòng quá hạn'** để nhả kho phòng nếu khách không thanh toán sau 15 phút.*
> - *Nghiệp vụ **'Hủy đặt phòng & Hoàn tiền'** bao gồm việc tính toán hoàn cọc theo chính sách ngày hủy và cập nhật trạng thái đơn phòng."*

### 🛡️ Kiến thức phòng thủ chống Thầy vặn:
- **Thầy hỏi**: *"Tại sao mũi tên `<<include>>` trỏ từ 'Đặt phòng trực tuyến' sang 'Khóa phòng chống trùng', trong khi `<<extend>>` lại trỏ từ 'Áp dụng mã giảm giá' về 'Đặt phòng trực tuyến'?"*
- **Đáp đanh thép**: *"Thưa Thầy, đây là quy chuẩn ngữ nghĩa cốt lõi của UML:*
  * *`<<include>>` là phụ thuộc bắt buộc: Use Case nguồn **gọi** Use Case đích, nên mũi tên trỏ từ nguồn sang đích.*
  * *`<<extend>>` là sự mở rộng tùy chọn: Use Case mở rộng **chèn thêm hành vi** vào Use Case cơ sở tại Extension Point khi thỏa mãn điều kiện, nên mũi tên trỏ **ngược** từ Use Case mở rộng về Use Case cơ sở để chỉ rõ nó đang bổ sung tính năng cho ai."*

---

## DIAGRAM 3: BIỂU ĐỒ PHÂN RÃ QUẢN LÝ TÀI KHOẢN
- **Tên Tab trong Draw.io**: `Biểu đồ phân rã quản lý tài khoản`
- **Mục tiêu**: Mô hình hóa việc phân quyền truy cập Role-Based Access Control (RBAC), bảo mật đăng nhập và nhật ký an ninh.

### 🎙️ Lời thoại thuyết trình:
> *"Tại phân hệ **Quản lý Tài khoản & Phân quyền**:*
> - *Khách hàng thao tác trên **'Đăng ký hội viên mới'** (bao gồm `<<include>>` Xác thực Email/SĐT và Khởi tạo hồ sơ tích điểm Loyalty).*
> - *Use Case **'Đăng nhập & Xác thực bảo mật'** có 2 nhánh mở rộng `<<extend>>`:*
>   1. **'Xác thực 2 yếu tố (2FA)'**: Dành cho tài khoản nội bộ và giao dịch giá trị cao.*
>   2. **'Khóa tài khoản khi đăng nhập sai 5 lần'**: Cơ chế phòng thủ chống tấn công vét cạn (Brute-force attack).*
> - *Phía Quản trị viên quản lý: **Lập hồ sơ và cấp tài khoản nhân sự**, **Cấu hình phân quyền vai trò (RBAC)** quy định quyền truy cập trên từng phân hệ, và **Ghi nhận & tra cứu Audit Logs** để lưu vết mọi thao tác nhạy cảm (như sửa giá, hủy hóa đơn)."*

---

## DIAGRAM 4: BIỂU ĐỒ PHÂN RÃ LÀM THỦ TỤC
- **Tên Tab trong Draw.io**: `Biểu đồ phân rã làm thủ tục`
- **Mục tiêu**: Mô hình hóa toàn bộ tác nghiệp tại quầy tiền sảnh của Lễ tân.

### 🎙️ Lời thoại thuyết trình:
> *"Tại phân hệ **Tác nghiệp Tiền sảnh & Lễ tân**:*
> - *Lễ tân thực hiện 5 luồng nghiệp vụ lớn:*
>   1. **Tiếp nhận đặt phòng tại quầy (Walk-in)**: `<<include>>` Gán phòng vật lý tức thời, Thu tiền cọc trực tiếp, và Ghi nhận hồ sơ khách vãng lai.*
>   2. **Làm thủ tục nhận phòng (Check-in)**: `<<include>>` Lưu trữ thông tin CCCD/Hộ chiếu theo quy định lưu trú, Cập nhật trạng thái phòng sang OCCUPIED, và `<<extend>>` **Xử lý đổi phòng (Room Move)** khi khách có yêu cầu đặc biệt.*
>   3. **Ghi nhận tiêu dùng dịch vụ phát sinh**: Tra cứu danh mục và ghi nợ chi tiêu minibar/giặt ủi trực tiếp vào Folio phòng.*
>   4. **Làm thủ tục trả phòng (Check-out)**: `<<include>>` Quyết toán công nợ & In hóa đơn VAT điện tử, Tự động chuyển trạng thái phòng sang 'Chờ dọn' (DIRTY), và `<<extend>>` Thu tiền đền bù hỏng hóc tài sản.*
>   5. **Sơ đồ phòng Gantt & Xử lý No-Show**: Giám sát phòng theo trục thời gian thực và xử lý hủy đơn khách vắng mặt quá 23:59 để giải phóng phòng."*

---

## DIAGRAM 5: BIỂU ĐỒ PHÂN RÃ VẬN HÀNH BUỒNG PHÒNG
- **Tên Tab trong Draw.io**: `Biểu đồ phân rã vận hành buồng phòng`
- **Mục tiêu**: Quy trình khép kín kiểm soát vệ sinh phòng khách 5 sao.

### 🎙️ Lời thoại thuyết trình:
> *"Tại phân hệ **Vận hành Buồng phòng**:*
> - *Nhân viên buồng phòng thực hiện Use Case trung tâm **'Quản lý vệ sinh buồng phòng'**.*
> - *Bao hàm `<<include>>`: Xem danh sách phòng cần dọn (DIRTY), Tiếp nhận phân công ca dọn, và Cập nhật tiến độ dọn phòng (chuyển sang CLEANING $\rightarrow$ CLEAN).*
> - *Mở rộng `<<extend>>`:**'Báo cáo sự cố hư hỏng vật tư / Bảo trì phòng'** khi phát hiện thiết bị hỏng (như máy lạnh không lạnh, vỡ gương).*
> - *Quản lý buồng phòng thực hiện Use Case **'Nghiệm thu kiểm định phòng'** để chuyển phòng sang trạng thái INSPECTED trước khi bàn giao cho Lễ tân đón khách."*

---

## DIAGRAM 6: BIỂU ĐỒ PHÂN RÃ QUẢN TRỊ DOANH THU
- **Tên Tab trong Draw.io**: `Biểu đồ phân rã quản trị doanh thu`
- **Mục tiêu**: Công cụ dành cho Quản lý Resort tối ưu hóa doanh thu (Yield Management).

### 🎙️ Lời thoại thuyết trình:
> *"Tại phân hệ **Quản trị Doanh thu & Danh mục**:*
> - *Quản lý Resort thiết lập **'Quản lý danh mục hạng phòng & Phòng vật lý'** (cấu trúc 3NF phân tách giữa loại phòng và số phòng thực tế).*
> - *Thực hiện **'Thiết lập giá linh hoạt & Voucher'**: Bao gồm `<<include>>` Cài đặt giá biến đổi theo mùa/cuối tuần (Dynamic Pricing), Phát hành mã ưu đãi Voucher, và `<<extend>>` Ban hành quy chế hoàn tiền cọc bậc thang.*
> - *Thực hiện **'Báo cáo doanh thu & Phân tích KPI'**: Tự động kết xuất doanh thu thực thu (đã trừ hủy hoàn), tính toán tỷ lệ lấp đầy (Occupancy Rate), giá bình quân phòng (ADR) và doanh thu trên mỗi phòng sẵn có (RevPAR)."*

---

## DIAGRAM 7: BIỂU ĐỒ HOẠT ĐỘNG ĐẶT PHÒNG TRỰC TUYẾN (AD-01)
- **Tên Tab trong Draw.io**: `Biểu đồ hoạt động đặt phòng trực tuyến`
- **Mục tiêu**: Dòng chảy logic nghiệp vụ Đặt phòng B2C, xử lý đồng thời (Concurrency) và cơ chế khóa phòng 15 phút.

### 🎙️ Lời thoại thuyết trình:
> *"Kính thưa Thầy/Cô, đây là **Biểu đồ Hoạt động Đặt phòng Trực tuyến (AD-01)**:*
>
> 👉 *[Chỉ vào 3 làn bơi]*:
> *Biểu đồ gồm 3 làn bơi Swimlanes: **Khách hàng** | **Hệ thống Web Đặt phòng** | **Cổng thanh toán (VNPay / MoMo)**.*
>
> 👉 *[Đi theo dòng chảy từng nút]*:
> 1. *Khách hàng 'Chọn loại phòng và khoảng ngày lưu trú' $\rightarrow$ Web 'Kiểm tra tồn khả dụng cho từng đêm'.*
> 2. *Nút rẽ nhánh Decision `[Đủ phòng cho mọi đêm?]`:*
>    - *Nếu `[Sai]`: 'Thông báo hết phòng; đề nghị đổi lựa chọn' $\rightarrow$ Kết thúc.*
>    - *Nếu `[Đúng]`: Web thực thi 'Kiểm tra lại và tạo RoomHoldLocks 15 phút' để xác lập quyền giữ chỗ tạm thời.*
> 3. *Cổng thanh toán 'Tạo giao dịch và mã QR gắn với khóa giữ chỗ' $\rightarrow$ Khách hàng 'Xem mã QR và thời hạn thanh toán giữ chỗ' với đồng hồ đếm ngược 15:00.*
> 4. *Thanh đồng bộ **Fork** phân tách 2 luồng song song:*
>    - *Luồng 1: Bộ đếm thời gian Timer 'Chờ đến expiresAt hoặc tín hiệu hủy hẹn giờ'.*
>    - *Luồng 2: Khách 'Quét mã VietQR trên App Ngân hàng' $\rightarrow$ Cổng thanh toán 'Xác thực giao dịch & Trừ tiền' $\rightarrow$ 'Gửi Webhook IPN thông báo kết quả'.*
> 5. *Tại thanh hợp nhất **Join**: Nếu Webhook thành công trong 15 phút $\rightarrow$ 'Xác thực Webhook, tạo Booking & Hủy hẹn giờ' $\rightarrow$ Khách nhận mã Booking PNR.*
> 6. *Nếu hết 15 phút mà không có thanh toán: Timer kích hoạt 'Giải phóng phòng giữ chỗ & Hủy phiên thanh toán' $\rightarrow$ Quỹ phòng tự động mở lại cho khách khác."*

### 🛡️ Kiến thức phòng thủ chống Thầy vặn:
- **Thầy hỏi**: *"Nếu khách thanh toán ở phút thứ 14 giây 59 nhưng Webhook đến trễ ở phút thứ 16 thì hệ thống xử lý thế nào?"*
- **Đáp đanh thép**: *"Thưa Thầy, hệ thống áp dụng cơ chế **Idempotent Reconciliation (Đối soát tự động)** được vẽ rõ ở nhánh `[Giữ tồn đã nhả; đối soát hoàn khoản đến muộn]`: Khi Webhook đến sau khi Lock đã hết hạn và phòng đã bị bán cho người khác, hệ thống ghi nhận giao dịch thành công nhưng chuyển sang trạng thái ngoại lệ cần hoàn tiền tự động (Auto-refund) hoặc thông báo Lễ tân hỗ trợ nâng hạng phòng miễn phí cho khách, tuyệt đối không nuốt tiền của khách."*

---

## DIAGRAM 8: BIỂU ĐỒ HOẠT ĐỘNG CHECK-IN VÀ GÁN PHÒNG VẬT LÝ ĐỘNG (AD-02)
- **Tên Tab trong Draw.io**: `Biểu đồ hoạt động Check-in và gán phòng vật lý động`
- **Mục tiêu**: Xử lý 2 luồng Check-in khách đặt trước và khách Walk-in tại quầy, nguyên tắc gán phòng sạch.

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Hoạt động AD-02**:*
> - *Làn bơi phân định: **Khách hàng** | **Lễ tân** | **Hệ thống PMS**.*
> - *Khách đến quầy $\rightarrow$ Nút Decision `[Đã đặt trước?]`:*
>   - *Nếu `[Đúng]`: Khách cung cấp mã Booking/SĐT $\rightarrow$ Lễ tân tra cứu $\rightarrow$ Kiểm tra Booking hợp lệ.*
>   - *Nếu `[Sai]`: Lễ tân tiếp nhận nhu cầu Walk-in $\rightarrow$ kiểm tra tồn phòng $\rightarrow$ Tạo hồ sơ khách và Booking tại quầy.*
> - *Khách xuất trình CCCD $\rightarrow$ Lễ tân quét và đối chiếu giấy tờ.*
> - *Hệ thống PMS tự động **'Lọc phòng khả dụng: CLEAN, VACANT & Không trùng lịch'**.*
> - *Nút Decision `[Có phòng sẵn sàng?]`:*
>   - *Nếu `[Sai]`: Thông báo khách chờ buồng phòng dọn gấp hoặc đề xuất đổi phòng.*
>   - *Nếu `[Đúng]`: Lễ tân chọn phòng vật lý $\rightarrow$ Hệ thống 'Kiểm tra lại và gán phòng vào các BookingNights' $\rightarrow$ 'Lưu giờ nhận và khách; chuyển phòng OCCUPIED' $\rightarrow$ Bàn giao chìa khóa cho khách."*

---

## DIAGRAM 9: BIỂU ĐỒ HOẠT ĐỘNG SỬ DỤNG DỊCH VỤ VÀ GHI CHI TIÊU VÀO FOLIO (AD-03)
- **Tên Tab trong Draw.io**: `Biểu đồ hoạt động sử dụng dịch vụ và ghi chi tiêu vào Folio`
- **Mục tiêu**: Minh bạch hóa tài khoản công nợ phòng (Folio) trong suốt kỳ nghỉ.

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Hoạt động AD-03**:*
> - *Khách sử dụng dịch vụ tại Nhà hàng/Minibar $\rightarrow$ Nút Decision `[Thanh toán ngay?]`:*
>   - *Nếu trả tiền mặt/quẹt thẻ ngay: Nhân viên thu tiền $\rightarrow$ Hệ thống lưu Order và đánh dấu đã thanh toán.*
>   - *Nếu ghi nợ phòng: Khách cung cấp số phòng $\rightarrow$ Nhân viên lập Order và gửi yêu cầu ghi nợ.*
> - *Hệ thống PMS kiểm tra 2 điều kiện bắt buộc: `[Đúng khách, phòng OCCUPIED?]` và `[Folio còn mở để ghi nợ?]`.*
> - *Hệ thống thực thi giao dịch nguyên tử: Lưu chi tiết tiêu dùng (Folio Details) và **Cộng khoản chưa thanh toán vào số dư Folio** $\rightarrow$ Khách ký xác nhận phiếu thu."*

---

## DIAGRAM 10: BIỂU ĐỒ HOẠT ĐỘNG TRẢ PHÒNG, KIỂM KÊ VÀ QUYẾT TOÁN FOLIO (AD-04)
- **Tên Tab trong Draw.io**: `Biểu đồ hoạt động trả phòng, kiểm kê và quyết toán Folio`
- **Mục tiêu**: Quy trình tất toán tài chính, xuất hóa đơn VAT và đổi trạng thái phòng sang DIRTY.

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Hoạt động AD-04**:*
> - *Khách báo trả phòng $\rightarrow$ Lễ tân phát lệnh kiểm phòng sang Buồng phòng.*
> - *Buồng phòng kiểm kê minibar và hiện trạng tài sản $\rightarrow$ gửi báo cáo phát sinh $\rightarrow$ Lễ tân nạp phụ thu vào Folio.*
> - *Hệ thống PMS tự động tổng hợp: `Số dư = Tiền phòng + Dịch vụ phát sinh + Hư hao - Tiền cọc` $\rightarrow$ Trình bảng quyết toán.*
> - *Xử lý số dư tại nút Decision:*
>   - *`[Số dư dương]`: Khách thanh toán phần còn thiếu.*
>   - *`[Số dư âm]`: Lễ tân thực hiện hoàn tiền thừa cho khách.*
> - *Chốt điều kiện bảo vệ: **`[Công nợ bằng 0?]`** $\rightarrow$ Hệ thống mới cho phép 'Chốt Folio, xuất hóa đơn GTGT Saigontourist Group' $\rightarrow$ 'Đóng lưu trú, giải phóng phân phòng, chuyển sang DIRTY' $\rightarrow$ Tự động đẩy phòng vào danh sách dọn."*

---

## DIAGRAM 11: BIỂU ĐỒ HOẠT ĐỘNG DỌN BUỒNG PHÒNG VÀ XỬ LÝ BẢO TRÌ (AD-05)
- **Tên Tab trong Draw.io**: `Biểu đồ hoạt động dọn buồng phòng và xử lý bảo trì`
- **Mục tiêu**: Vận hành buồng phòng di động và cơ chế cô lập phòng bảo trì.

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Hoạt động AD-05**:*
> - *Nhân viên buồng phòng mở ứng dụng di động Web PWA $\rightarrow$ xem danh sách phòng 'DIRTY' $\rightarrow$ chọn phòng $\rightarrow$ hệ thống chuyển sang 'CLEANING'.*
> - *Trong quá trình dọn, nếu phát hiện sự cố:*
>   - *Nhân viên chụp ảnh lỗi, nhập mô tả $\rightarrow$ Hệ thống tạo `MaintenanceTicket` và khóa phòng sang 'MAINTENANCE'.*
>   - *Tổ kỹ thuật nhận phiếu, sửa chữa $\rightarrow$ hoàn tất sửa chuyển về 'DIRTY' để buồng phòng dọn lại.*
> - *Nếu dọn đạt chuẩn sạch: Nhân viên bấm xác nhận đạt chuẩn $\rightarrow$ Server cập nhật trạng thái 'CLEAN' và **phát sự kiện WebSocket** $\rightarrow$ Màn hình quầy lễ tân lập tức chuyển sang màu xanh, sẵn sàng đón khách mới."*

---

## DIAGRAM 12: BIỂU ĐỒ HOẠT ĐỘNG HỦY PHÒNG (AD-06)
- **Tên Tab trong Draw.io**: `Biểu đồ hoạt động hủy phòng`
- **Mục tiêu**: Quy trình hủy phòng tự động B2C, áp dụng chính sách hoàn cọc bậc thang và an toàn giao dịch (Rollback).

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Hoạt động Hủy phòng (AD-06)**:*
> - *Khách chọn đơn và yêu cầu hủy $\rightarrow$ Ứng dụng gửi yêu cầu xem trước khoản hoàn.*
> - *Hệ thống PMS tra cứu đơn $\rightarrow$ Kiểm tra điều kiện `[Đủ điều kiện hủy?]` (đơn phải là CONFIRMED và chưa Check-in).*
> - *Hệ thống tra tỷ lệ hoàn trước 14:00 ngày nhận phòng: **Hoàn 100%** (trước 72h), **Hoàn 50%** (từ 24-72h), **Hoàn 0%** (dưới 24h).*
> - *Ứng dụng hiển thị tiền hoàn và phí hủy dự kiến $\rightarrow$ Khách nhập lý do và bấm xác nhận hủy.*
> - *PMS kiểm tra lại tính hợp lệ của đơn $\rightarrow$ Chuyển trạng thái đơn sang `'Canceled'` $\rightarrow$ Lưu biên bản hủy.*
> - *Nếu `[Tiền hoàn > 0]`: Ghi nhận giao dịch hoàn cọc $\rightarrow$ Lập tức **giải phóng các đêm đặt (BookingNights)**.*
> - *Nếu giao dịch hoàn cọc thành công: Chốt giao dịch và báo khách thành công. Nếu thất bại: Hệ thống tự động **Hoàn tác giao dịch (Rollback)** để bảo toàn dữ liệu."*

---

## DIAGRAM 13 ĐẾN 18: BỘ 06 BIỂU ĐỒ TRÌNH TỰ BCE (SEQUENCE DIAGRAMS SD-01 ĐẾN SD-06)

### 🎙️ Lời thoại mở đầu khối Sequence:
> *"Kính thưa Thầy/Cô, toàn bộ 6 biểu đồ trình tự được xây dựng theo chuẩn **BCE (Boundary - Control - Entity)** với nguyên tắc phân lớp nghiêm ngặt:*
> - **Boundary ($\vdash\bigcirc$)**: Tiếp nhận tương tác người dùng (`SearchBookingUI`, `FrontDeskGanttUI`, `ServicePostingUI`, `CheckoutFolioUI`, `HousekeepingMobileUI`, `BookingHistoryUI`).*
> - **Control ($\circlearrowleft$)**: Điều phối nghiệp vụ giao dịch (`BookingService`, `CheckInController`, `FolioBillingService`, `CheckoutController`, `HousekeepingService`, `BookingCancellationService`).*
> - **Entity ($\ominus$)**: Lưu trữ trạng thái thực thể (`RoomInventory`, `RoomLock`, `Booking`, `BookingNight`, `GuestProfile`, `PhysicalRoom`, `FolioInvoice`, `FolioItem`, `PaymentTransaction`, `CleaningLog`, `RefundPolicy`, `CancellationRecord`).*
> - *Mọi lời gọi đồng bộ (Sync Call) đều có vạch kích hoạt (Activation Bar) đối xứng với thông điệp trả về (Return Message nét đứt). Khung kết hợp `Alt` và `Opt` phân nhánh tường minh."*

---

### DIAGRAM 13: BIỂU ĐỒ TRÌNH TỰ ĐẶT PHÒNG (SD-01)
- **Tên Tab**: `Biểu đồ trình tự đặt phòng`
- **Các bước chi tiết**:
  1. *Khách chọn loại phòng & ngày trên `:SearchBookingUI`.*
  2. *Boundary gọi `:BookingService` hàm `yeuCauGiuChoTamThoi(roomTypeId, dates, qty)`.*
  3. *`:BookingService` gọi `:RoomInventory` hàm `checkAvailability(roomTypeId, dates)` $\rightarrow$ Trả về: Còn phòng.*
  4. *`:BookingService` gọi `:RoomInventory` hàm `createHoldLock(roomTypeId, expiresAt = now + 15m)` $\rightarrow$ Trả về `lockId`.*
  5. *Boundary hiển thị đồng hồ đếm ngược 15:00 và mở màn hình thanh toán.*
  6. *`:BookingService` gọi `:VNPayGateway` hàm `createOrder(orderId, amount, callbackUrl, ipnUrl)` $\rightarrow$ Trả về URL và mã VietQR.*
  7. *Khách quét VietQR trên App Ngân hàng $\rightarrow$ Xác nhận trừ tiền.*
  8. *Khung **Alt [Thành công, vnp_ResponseCode == '00']**:*
     - *VNPay gửi Webhook IPN sang `:VNPayGateway` $\rightarrow$ lưu chứng từ thanh toán `saveTransaction` sang `:PaymentTransaction`.*
     - *`:BookingService` gọi `confirmBookingFromLock` $\rightarrow$ sinh bản ghi `:Booking` trạng thái `CONFIRMED` $\rightarrow$ sinh các đêm lưu trú `:BookingNights` $\rightarrow$ gọi `markLockAsSold(lockId)` chuyển khóa tạm thành ĐÃ BÁN.*
     - *Client Polling/SSE nhận kết quả `PAID`, hiển thị Voucher PNR.*
  9. *Khung **Alt [else: Thất bại / Hủy]**:*
     - *Ghi nhận giao dịch `FAILED` $\rightarrow$ gọi `releaseHoldLock(lockId)` và `markLockAsExpired(lockId)` $\rightarrow$ Mở lại kho phòng ngay tức khắc.*

---

### DIAGRAM 14: BIỂU ĐỒ TRÌNH TỰ CHECK-IN (SD-02)
- **Tên Tab**: `Biểu đồ trình tự check-in`
- **Các bước chi tiết**:
  1. *Lễ tân nhập PNR trên `:FrontDeskGanttUI` $\rightarrow$ gọi `:CheckInController` hàm `getBookingDetails(pnrCode)`.*
  2. *Lễ tân quét thẻ CCCD khách $\rightarrow$ gọi `:GuestProfile` hàm `saveIdentityProfile(guestData)`.*
  3. *`:CheckInController` gọi `:PhysicalRoom` hàm `checkCleanRooms(roomTypeId, status='CLEAN')` để lọc phòng trống sạch.*
  4. *Khung **Alt [Có phòng CLEAN]**:*
     - *Đề xuất số phòng `cleanRoomId` (ví dụ: Villa 01).*
     - *Cập nhật trạng thái đơn `:Booking` sang `CHECKED_IN`.*
     - *Gọi `assignPhysicalRoom(cleanRoomId)` gán phòng vào `:BookingNight`.*
     - *Đổi trạng thái phòng vật lý `:PhysicalRoom` sang `OCCUPIED`.*
     - *In phiếu nhận phòng, giao chìa khóa và trên sơ đồ Gantt đổi màu phòng sang Đỏ (OCCUPIED).*
  5. *Khung **Alt [else: Chưa có phòng sạch]**: Phát cảnh báo phòng đang DIRTY, đề xuất dọn gấp hoặc đổi phòng.*

---

### DIAGRAM 15: BIỂU ĐỒ TRÌNH TỰ DỊCH VỤ PHÁT SINH (SD-03)
- **Tên Tab**: `Biểu đồ trình tự dịch vụ phát sinh`
- **Các bước chi tiết**:
  1. *Nhân viên nhập số phòng trên `:ServicePostingUI` $\rightarrow$ gọi `:FolioBillingService` hàm `findActiveBooking(roomNumber)`.*
  2. *Khung **Alt [Phòng đang lưu trú CHECKED_IN]**:*
     - *Hiển thị danh mục dịch vụ $\rightarrow$ Nhân viên chọn món minibar/dịch vụ.*
     - *Lấy đơn giá niêm yết từ `:PriceCatalog` $\rightarrow$ Tự động tính tổng tiền có VAT.*
     - *Gọi `:FolioInvoice` hàm `recordConsumption(bookingId, itemList, totalAmount)` lưu chi tiết tiêu dùng.*
     - *Gọi `postChargeToFolio(bookingId, totalAmount)` ghi nợ lũy kế vào số dư Folio.*
     - *In phiếu ký nhận dịch vụ (Voucher) cho khách ký.*
  3. *Khung **Alt [else: Phòng trống/Đã trả]**: Từ chối ghi nợ, báo lỗi phòng không có khách.*

---

### DIAGRAM 16: BIỂU ĐỒ TRÌNH TỰ CHECK-OUT (SD-04)
- **Tên Tab**: `Biểu đồ trình tự check-out`
- **Các bước chi tiết**:
  1. *Lễ tân nạp phụ thu kiểm phòng minibar $\rightarrow$ `:FolioBillingService` lưu chi tiết.*
  2. *Hệ thống tính toán công nợ: $\text{Số dư} = \text{Tiền phòng} + \text{Dịch vụ phát sinh} - \text{Tiền cọc}$.*
  3. *Lễ tân thu tiền thiếu (tiền mặt/quẹt thẻ) $\rightarrow$ ghi nhận chứng từ `:PaymentTransaction`.*
  4. *Khởi tạo hóa đơn điện tử `:Invoice` với thuế suất VAT 8%, mã số thuế Saigontourist Group `0312456789-001`.*
  5. *Đổi trạng thái đơn `:Booking` sang `CHECKED_OUT` và đóng Folio.*
  6. *Gửi thông điệp sang `:PhysicalRoom` cập nhật trạng thái phòng sang `DIRTY`.*
  7. *In hóa đơn VAT đưa khách và tự động đổi màu ô phòng trên Gantt sang Đỏ/Vàng (DIRTY).*

---

### DIAGRAM 17: BIỂU ĐỒ TRÌNH TỰ DỌN DẸP (SD-05)
- **Tên Tab**: `Biểu đồ trình tự dọn dẹp`
- **Các bước chi tiết**:
  1. *Nhân viên buồng phòng mở điện thoại xem danh sách phòng `DIRTY`.*
  2. *Bấm nhận dọn $\rightarrow$ phòng đổi sang `CLEANING` $\rightarrow$ tạo `:CleaningLog` bấm giờ ca dọn.*
  3. *Khung **Alt [Dọn đạt chuẩn sạch]**:*
     - *Dọn xong, kiểm tra minibar $\rightarrow$ bấm hoàn thành.*
     - *Hệ thống đổi trạng thái phòng sang `CLEAN`.*
     - *Đóng ca dọn trong `:CleaningLog` với kết quả `PASSED`.*
     - *Bắn **WebSocket Event `notifyRoomStatus(roomId, 'CLEAN')`** $\rightarrow$ Sơ đồ lễ tân lập tức đổi sang màu xanh, sẵn sàng đón khách.*
  4. *Khung **Alt [else: Phát hiện sự cố hỏng hóc]**:*
     - *Chụp ảnh lỗi, gửi báo cáo $\rightarrow$ đổi trạng thái phòng sang `MAINTENANCE`.*
     - *Sinh phiếu sửa chữa `:MaintenanceTicket` $\rightarrow$ Bắn WebSocket báo sự cố sang tổ kỹ thuật và lễ tân.*

---

### DIAGRAM 18: BIỂU ĐỒ TRÌNH TỰ HỦY PHÒNG (SD-06)
- **Tên Tab**: `Biểu đồ trình tự hủy phòng`
- **Các bước chi tiết**:
  1. *Khách bấm Yêu cầu hủy trên `:BookingHistoryUI` $\rightarrow$ gọi `:BookingCancellationService`.*
  2. *Kiểm tra đơn ở trạng thái `CONFIRMED` $\rightarrow$ gọi `:RefundPolicy` với tham số `hoursRemaining` (tính đến 14:00 ngày nhận phòng).*
  3. *Trả về tỷ lệ hoàn cọc: **100%**, **50%** hoặc **0%** $\rightarrow$ Hiển thị bảng xem trước (Preview Modal).*
  4. *Khách nhập lý do và bấm Xác nhận hủy.*
  5. *Đổi trạng thái đơn `:Booking` sang `Canceled` $\rightarrow$ Lưu biên bản hủy `:CancellationRecord`.*
  6. *Khung **Opt [refundAmount > 0]**: Ghi nhận chứng từ hoàn tiền với **số tiền âm** (`-refundAmount`) vào `:PaymentTransaction`.*
  7. *Thao tác then chốt: **`releaseBookedNights(bookingId)`** $\rightarrow$ Giải phóng toàn bộ các đêm lưu trú trong `:BookingNight` để quỹ phòng trống lập tức mở lại trên website.*

---

## DIAGRAM 19: BIỂU ĐỒ LỚP LĨNH VỰC (DOMAIN CLASS DIAGRAM)
- **Tên Tab trong Draw.io**: `Biểu đồ lớp lĩnh vực`
- **Mục tiêu**: Mô hình cấu trúc tĩnh của toàn bộ thực thể bài toán theo nguyên lý Information Expert.

### 🎙️ Lời thoại thuyết trình:
> *"Kính thưa Thầy/Cô, Biểu đồ Lớp Lĩnh vực thể hiện cấu trúc tĩnh của hệ thống:*
> - *Mỗi lớp được cấu tạo gồm 3 ngăn: Tên lớp, Thuộc tính nghiệp vụ, và Phương thức hành vi.*
> - *Nguyên lý **Information Expert**: Trách nhiệm tính toán được giao cho lớp nắm giữ đầy đủ thông tin nhất. Ví dụ: `BookingMaster` nắm thông tin ngày đến/đi nên chứa hàm `tinhTongTien()` và `tinhTienPhatHuy()`; `ServiceFolio` chứa hàm `ghiNoDichVu()` và `tinhSoDuCongNo()`.*
> - *Các mối quan hệ sống còn:*
>   1. **Hợp thành (Composition - Kim cương đen)**: Giữa `BookingMaster` và `BookingNight`, giữa `ServiceFolio` và `FolioItem`. Vòng đời của bộ phận phụ thuộc sinh tử vào toàn thể.*
>   2. **Thu nạp (Aggregation - Kim cương trắng)**: Giữa `Hotel` và `RoomType`, giữa `RoomType` và `PhysicalRoom`. Tách biệt giữa hạng phòng kinh doanh và phòng vật lý.*
>   3. **Kế thừa (Generalization)**: Lớp cha `Account` được kế thừa bởi `CustomerAccount` và `StaffAccount`.*
>   4. **Bản số (Multiplicity)**: Được định danh chính xác hai đầu liên kết (`1..1`, `0..*`, `1..*`)."*

---

## DIAGRAM 20: BIỂU ĐỒ GÓI (PACKAGE DIAGRAM)
- **Tên Tab trong Draw.io**: `Biểu đồ gói`
- **Mục tiêu**: Tổ chức kiến trúc mã nguồn thành các gói phân tầng theo chuẩn n-Tier Architectural Pattern.

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Gói (Package Diagram)**, hệ thống được phân rã thành 5 tầng kiến trúc độc lập:*
> 1. **Gói `<<user interface>>` (Giao diện người dùng)**: Chứa các màn hình của Khách hàng, Lễ tân, Buồng phòng, Quản lý và Quản trị viên.*
> 2. **Gói `<<application>>` (Điều phối yêu cầu)**: Tiếp nhận Request từ giao diện, kiểm tra quyền hạn (Authorization Middleware) và định tuyến đến các bộ phận nghiệp vụ.*
> 3. **Gói `<<domain>>` (Nghiệp vụ khách sạn cốt lõi)**: Chia thành 5 gói con nghiệp vụ:*
>    - `Đặt phòng trực tuyến`: Tìm phòng, giữ phòng 15 phút, xác nhận thanh toán.*
>    - `Nhận phòng`: Kiểm tra đặt phòng, gán phòng vật lý sạch.*
>    - `Dịch vụ phát sinh`: Tra cứu danh mục, ghi nợ, tính lại số dư.*
>    - `Trả phòng`: Quyết toán công nợ, chốt hóa đơn VAT, đổi phòng chờ dọn.*
>    - `Buồng phòng`: Xem phòng bẩn, nhận ca dọn, xác nhận phòng sạch.*
> 4. **Gói `<<infrastructure>>` (Truy cập dữ liệu)**: Quản lý Connection Pooling, xử lý ORM/SQL, và kiểm soát Transaction nguyên tử.*
> 5. **Gói `<<database>>` (Cơ sở dữ liệu)**: Lưu trữ bảng dữ liệu thực thể.*
> - *Quan hệ phụ thuộc (Dependency nét đứt `<<use>>`) tuân thủ nghiêm ngặt theo một chiều từ trên xuống dưới, tuyệt đối không có quan hệ phụ thuộc vòng (Circular Dependency)."*

---

## DIAGRAM 21: BIỂU ĐỒ TRIỂN KHAI (DEPLOYMENT DIAGRAM)
- **Tên Tab trong Draw.io**: `Biểu đồ triển khai`
- **Mục tiêu**: Mô hình hóa hạ tầng phần cứng, mạng và môi trường thực thi 3-Tier Enterprise.

### 🎙️ Lời thoại thuyết trình:
> *"Tại **Biểu đồ Triển khai (Deployment Diagram)**:*
> - **Tầng 1 (Client Tier)**: Thiết bị khách hàng B2C, Thiết bị buồng phòng di động (Mobile Web PWA), và Máy trạm Lễ tân (kết nối máy in hóa đơn nhiệt POS qua cổng `USB 2.0 / Raw TCP Port 9100`).*
> - **Tầng 2 (Application Server Tier)**: Máy chủ Ubuntu Linux 22.04 LTS gồm:*
>   - **Nginx Web Server**: Reverse Proxy, mã hóa `TLS 1.3 / HTTPS Port 443`, phân chia phân đoạn mạng nội bộ `VLAN 20`, hỗ trợ `WebSocket (WSS)` thời gian thực.*
>   - **Python WSGI Container**: Chạy các ứng dụng dịch vụ (`BookingService`, `FolioSettlementService`, `CancellationService`, `HousekeepingService`).*
>   - **Cron Background Daemon**: Chạy tiến trình ngầm `cron_worker.py` liên tục quét dọn các bản ghi giữ phòng quá hạn 15 phút.*
> - **Tầng 3 (Data & External Services Tier)**: Máy chủ CSDL trong phân vùng an toàn (`Dedicated DB Subnet`), kết nối Cổng thanh toán VNPay (REST API/Webhook IPN) và Cổng Mail giao dịch SendGrid/Google Cloud (SMTP Port 587)."*

---

## DIAGRAM 22 ĐẾN 27: KHỐI 06 BIỂU ĐỒ THÀNH PHẦN (COMPONENT DIAGRAMS)

### 🎙️ Lời thoại mở đầu khối Component:
> *"Kính thưa Thầy/Cô, Biểu đồ Thành phần (Component Diagram) thể hiện kiến trúc phần mềm ở mức mô-đun hóa có thể tái sử dụng và thay thế được (Replaceable Units), liên kết với nhau qua các cổng giao tiếp và giao diện cung cấp (Provided Interface) / giao diện yêu cầu (Required Interface):*
> - **Diagram 22 (Tổng quát)**: Thể hiện sự phân tách giữa Ứng dụng giao diện (`<<executable>>`), Mô-đun giao tiếp, Ứng dụng nghiệp vụ, Thư viện kết nối dữ liệu (`<<library>>`) và Cơ sở dữ liệu.*
> - **Diagram 23 (Đặt phòng trực tuyến)**: Mô tả liên kết giữa Mô-đun tiếp nhận yêu cầu đặt phòng $\leftrightarrow$ Mô-đun giữ tồn phòng 15 phút $\leftrightarrow$ Mô-đun xác nhận đặt phòng $\leftrightarrow$ Tầng Data Access.*
> - **Diagram 24 (Nhận phòng & Gán phòng)**: Mô tả luồng liên kết giữa Màn hình Lễ tân $\leftrightarrow$ Mô-đun tiếp nhận Check-in $\leftrightarrow$ Mô-đun gán phòng vật lý đủ điều kiện sạch $\leftrightarrow$ CSDL.*
> - **Diagram 25 (Dịch vụ phát sinh)**: Mô-đun ghi phát sinh tại quầy $\leftrightarrow$ Mô-đun tính lại số dư hóa đơn $\leftrightarrow$ CSDL Dịch vụ & Hóa đơn.*
> - **Diagram 26 (Check-out)**: Màn hình quyết toán $\leftrightarrow$ Mô-đun quyết toán trả phòng $\leftrightarrow$ Chốt hóa đơn và kích hoạt chuyển phòng sang trạng thái chờ dọn.*
> - **Diagram 27 (Vệ sinh buồng phòng)**: Màn hình buồng phòng di động $\leftrightarrow$ Mô-đun tiếp nhận buồng phòng $\leftrightarrow$ Cập nhật trạng thái phòng sang sạch (CLEAN)."*

---

## DIAGRAM 28: THIẾT KẾ DỮ LIỆU (UML DATABASE DESIGN - 15 BẢNG 3NF)
- **Tên Tab trong Draw.io**: `Thiết kế dữ liệu`
- **Mục tiêu**: Chuẩn hóa toàn bộ cấu trúc dữ liệu quan hệ đạt chuẩn 3NF, loại bỏ hoàn toàn dư thừa và dị thường cập nhật.

### 🎙️ Lời thoại thuyết trình:
> *"Kính thưa Thầy/Cô, sản phẩm cuối cùng trong file là **Biểu đồ Thiết kế Dữ liệu gồm 15 bảng đạt chuẩn 3NF**:*
>
> 👉 *[Chỉ vào 5 cụm bảng nghiệp vụ]*:
> 1. ***Cụm Tài khoản & Phân quyền**: `T_Role` (quyền hạn), `T_Account` (thông tin đăng nhập có băm mật khẩu `passwordHash`), `T_StaffProfile` (hồ sơ nhân sự), `T_CustomerProfile` (hồ sơ khách hàng, mã định danh CCCD và điểm tích lũy Loyalty).*
> 2. ***Cụm Giữ chỗ chống Race Condition**: Bảng `T_RoomHoldLock` lưu trữ `holdId`, `idRoomType`, `sessionId`, `quantity`, thời điểm khóa `lockedAt`, thời điểm hết hạn `expiresAt` (đúng 15 phút), và `status`.*
> 3. ***Cụm Khách sạn & Phòng 3NF**: Phân tách triệt để:*
>    - `T_RoomType`: Lưu mã loại phòng, tên loại, giá cơ bản `basePrice`, số khách tối đa `maxAdults`, và tổng tồn kho phòng kinh doanh `totalInventory`.*
>    - `T_PhysicalRoom`: Lưu 14 phòng vật lý thực tế với số phòng `roomNumber`, số tầng `floorNumber`, trạng thái buồng phòng `housekeepingStatus` (DIRTY/CLEAN/MAINTENANCE) và trạng thái lưu trú `occupancyStatus` (VACANT/OCCUPIED).*
> 4. ***Cụm Vận hành Buồng phòng**: `T_HousekeepingLog` (lưu ca dọn, thời gian bắt đầu và kết quả nghiệm thu) và `T_MaintenanceTicket` (phiếu báo cáo sự cố thiết bị hư hỏng kèm mức ưu tiên).*
> 5. ***Cụm Đặt phòng & Kế toán Folio 3NF**:*
>    - `T_Booking`: Bảng Master lưu mã PNR duy nhất (`pnrCode [Unique]`), ngày đến `arrivalDate`, ngày đi `departureDate`, tổng số đêm `totalNights`, tổng tiền phòng và tiền cọc.*
>    - `T_BookingNight`: Lưu chi tiết từng đêm lưu trú (`stayDate`), giá tiền từng đêm (`nightPrice`) và gán với `idPhysicalRoom` cụ thể.*
>    - `T_ServiceItem` & `T_ServiceConsumption`: Danh mục dịch vụ và bảng lưu chi tiết tiêu dùng minibar/giặt ủi.*
>    - `T_FolioInvoice`: Hóa đơn quyết toán lưu tổng tiền phòng `roomSubtotal`, tiền dịch vụ `serviceSubtotal`, tiền thuế VAT `taxVatAmount`, trừ tiền cọc `depositDeducted` và số tiền thanh toán cuối cùng `finalAmount`.*
>    - `T_PaymentTransaction`: Lưu vết mọi giao dịch tài chính VNPay/Tiền mặt với mã tham chiếu `transactionCode` phục vụ đối soát kiểm toán.*
> - *Toàn bộ cấu trúc khóa chính (PK) gạch chân đỏ và khóa ngoại (FK) in nghiêng xanh dương đảm bảo toàn vẹn tham chiếu 100%."*

---

# BỘ BÍ KÍP 20 CÂU HỎI "VẶN VẸO" KINH ĐIỂN CỦA HỘI ĐỒNG VÀ CÂU TRẢ LỜI "ĂN ĐIỂM TUYỆT ĐỐI"

### ❓ Câu 1: "Tại sao trong Biểu đồ Use Case tổng quát (Diagram 1), Cron System và Cổng thanh toán lại được vẽ là Actor?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, theo giáo trình UML 2.5 của OMG, Actor là bất kỳ thực thể bên ngoài nào tương tác để trao đổi dữ liệu với hệ thống. Cron System là một Agent ngoại vi kích hoạt tiến trình theo sự kiện thời gian (Temporal Event); Cổng thanh toán VNPay là hệ thống thứ ba tương tác qua giao thức Webhook. Cả hai đều nằm ngoài ranh giới hệ thống nên được mô hình hóa là Actor hợp lệ."*

### ❓ Câu 2: "Tại sao trong Diagram 2, quan hệ giữa 'Đặt phòng trực tuyến' và 'Khóa phòng chống trùng 15 phút' lại là `<<include>>` mà không phải `<<extend>>`?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, vì nghiệp vụ đặt phòng khách sạn không bao giờ cho phép đặt phòng thành công mà không trừ kho giữ chỗ. Luồng xử lý bắt buộc phải đi qua bước khóa phòng tạm thời để chống bán trùng. Do đó đây là quan hệ bắt buộc (`<<include>>`), không phải tùy chọn theo điều kiện (`<<extend>>`)."*

### ❓ Câu 3: "Trong Biểu đồ Hoạt động AD-01 (Diagram 7), thanh đậm Fork/Join thể hiện điều gì? Nếu Timer 15 phút kết thúc trước thì luồng Webhook bị xử lý ra sao?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, thanh Fork tạo ra 2 luồng xử lý song song độc lập: một luồng đếm giờ Timer 15 phút và một luồng chờ khách quét mã thanh toán. Tại thanh Join, nếu Timer hết hạn trước mà chưa có tín hiệu thanh toán, hệ thống lập tức hủy phiên giữ chỗ và nhả phòng. Nếu Webhook thanh toán đến muộn sau khi phòng đã bị nhả, cơ chế đối soát ngoại lệ (Reconciliation) sẽ kích hoạt để hoàn tiền tự động hoặc đề xuất đổi phòng cho khách, không làm thất thoát tiền."*

### ❓ Câu 4: "Tại sao trong Biểu đồ Hoạt động AD-04 (Diagram 10), điều kiện tiên quyết để chốt Folio và xuất hóa đơn là `Công nợ bằng 0`?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, theo chế độ kế toán khách sạn quốc tế, Folio là sổ cái công nợ lưu trú. Nếu số dư Folio khác 0 (Balance $\ne$ 0), tức là khách còn nợ tiền hoặc khách còn tiền cọc thừa chưa lấy lại. Chỉ khi số dư cân bằng bằng 0 (sau khi thu thêm hoặc hoàn trả cọc thừa), hệ thống mới được phép đóng sổ (Close Folio) và xuất hóa đơn tài chính VAT hợp lệ."*

### ❓ Câu 5: "Trong Biểu đồ Hoạt động AD-06 (Diagram 12), tại sao lại có nhánh 'Hoàn tác giao dịch (Rollback)'?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, thao tác hủy phòng gồm nhiều bước: đổi trạng thái đơn, ghi chứng từ hoàn tiền và giải phóng các đêm lưu trú. Đây là một Database Transaction nguyên tử (ACID). Nếu bước ghi hoàn tiền hoặc mở lại phòng gặp sự cố mạng hoặc lỗi CSDL, hệ thống bắt buộc phải Rollback toàn bộ để tránh tình trạng đơn đã đánh dấu hủy nhưng tiền không được hoàn hoặc phòng bị khóa vĩnh viễn."*

### ❓ Câu 6: "Tại sao trong cả 6 biểu đồ Sequence (Diagram 13 - 18), nhóm lại tuân thủ mô hình BCE mà không cho Boundary gọi thẳng vào Entity?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, đây là nguyên lý phân tầng và giảm thiểu phụ thuộc (Low Coupling & High Cohesion):
> - Boundary đại diện cho giao diện, Entity đại diện cho dữ liệu lưu trữ. Nếu Boundary gọi thẳng vào Entity, giao diện sẽ bị phụ thuộc chặt vào cấu trúc bảng CSDL, làm lộ thông tin và phá vỡ tính bao đóng (Information Hiding).
> - Tầng Control đóng vai trò nhạc trưởng điều phối các luật nghiệp vụ (Business Rules), kiểm tra quyền hạn và quản lý Transaction. Nhờ có Control, khi ta thay đổi giao diện từ Web sang Mobile App, toàn bộ tầng nghiệp vụ và dữ liệu Entity được giữ nguyên 100%."*

### ❓ Câu 7: "Trong Sequence SD-01 (Diagram 13), cơ chế Polling hoặc SSE ở bước 15 nhằm mục đích gì?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, khi khách quét mã VietQR trên điện thoại, giao dịch được xác thực giữa Ngân hàng và Cổng VNPay, sau đó VNPay gửi Webhook ngầm (Back-channel IPN) về máy chủ hệ thống. Trình duyệt của khách (Front-channel) không tự biết được kết quả này nếu không có cơ chế Server-Sent Events (SSE) hoặc Polling định kỳ 2 giây/lần để hỏi máy chủ xem đơn hàng đã được cập nhật sang 'PAID' hay chưa, từ đó tự động chuyển hướng màn hình sang Voucher thành công."*

### ❓ Câu 8: "Tại sao trong Sequence SD-02 (Diagram 14), chỉ có phòng ở trạng thái 'CLEAN' mới được gán cho khách?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, đây là tiêu chuẩn nghiệp vụ bắt buộc của khách sạn 5 sao. Một phòng dù trống về mặt lịch đặt (Vacant) nhưng nếu chưa được dọn dẹp (Dirty) hoặc đang bảo trì (Maintenance) thì không thể giao chìa khóa cho khách. Hệ thống bảo vệ chất lượng dịch vụ bằng cách lọc qua điều kiện `housekeepingStatus == 'CLEAN'`."*

### ❓ Câu 9: "Trong Sequence SD-04 (Diagram 16), tại sao ngay sau khi Check-out xong, hệ thống lập tức đổi trạng thái phòng sang 'DIRTY'?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, ngay khi khách vừa trả phòng, căn phòng đó đã qua sử dụng và cần được thay ga trải giường, dọn dẹp và bổ sung minibar mới. Việc tự động chuyển sang 'DIRTY' giúp kích hoạt tức thời danh sách công việc trên ứng dụng di động của đội buồng phòng mà Lễ tân không cần phải gọi điện thoại hay ghi sổ giấy thủ công."*

### ❓ Câu 10: "Trong Sequence SD-06 (Diagram 18), tại sao chứng từ hoàn tiền cọc lại được ghi với số tiền âm (`-refundAmount`)?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, trong nguyên lý kế toán kép và đối soát tài chính khách sạn, mọi khoản tiền thu vào ghi dấu dương (+), và mọi khoản hoàn trả tiền cho khách (Refund/Payout) phải ghi dấu âm (-) trong bảng `payment_transactions`. Khi tính tổng doanh thu thực thu, câu lệnh chỉ cần thực hiện `SUM(amount)` sẽ tự động bù trừ tiền thu và tiền hoàn một cách hoàn hảo và chính xác tuyệt đối."*

### ❓ Câu 11: "Biểu đồ Gói (Diagram 20) giúp giải quyết vấn đề gì trong kiến trúc phần mềm?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, Biểu đồ Gói giúp tổ chức mã nguồn của một hệ sinh thái lớn thành các phân tầng rõ ràng (Layered Architecture). Nó chứng minh hệ thống tuân thủ nguyên lý Dependency Inversion: Gói giao diện phụ thuộc gói điều phối, gói điều phối phụ thuộc gói nghiệp vụ miền (Domain), và nghiệp vụ miền độc lập với hạ tầng cơ sở dữ liệu. Nhờ đó dự án dễ bảo trì, dễ mở rộng và kiểm thử độc lập."*

### ❓ Câu 12: "Sự khác biệt căn bản giữa Biểu đồ Gói (Diagram 20) và Biểu đồ Thành phần (Diagram 22) là gì?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy:
> - **Biểu đồ Gói (Package Diagram)** là mô hình tổ chức logic ở mức mã nguồn (Logical Grouping), gom nhóm các lớp có liên quan thành các Package/Namespace.
> - **Biểu đồ Thành phần (Component Diagram)** là mô hình kiến trúc ở mức đóng gói thực thi (Physical/Modular Architecture), thể hiện các khối mô-đun phần mềm độc lập (`<<executable>>`, `<<library>>`, `<<component>>`) giao tiếp với nhau qua các Interface và Port."*

### ❓ Câu 13: "Trong Biểu đồ Triển khai (Diagram 21), tại sao Nginx lại được đặt phía trước Python WSGI Container?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, Nginx đóng vai trò là một Reverse Proxy chuyên dụng cấp doanh nghiệp:
> 1. Nginx xử lý bắt tay mã hóa bảo mật SSL/TLS 1.3 nhanh gấp nhiều lần so với ứng dụng Python (SSL Termination).
> 2. Nginx phục vụ trực tiếp các tệp tin tĩnh (hình ảnh phòng, file CSS/JS) từ ổ cứng mà không cần đánh thức tiến trình Python WSGI, giúp tiết kiệm tối đa RAM và CPU.
> 3. Nginx đóng vai trò chống tấn công DDoS, giới hạn tần suất gọi API (Rate Limiting) và phân luồng kết nối WebSocket thời gian thực."*

### ❓ Câu 14: "Tại sao trong Diagram 21, quầy lễ tân lại kết nối máy in nhiệt POS qua cáp USB / Raw TCP Port 9100 nội bộ mà không in qua Cloud?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, ngoài Côn Đảo là môi trường hải đảo thường xuyên chịu ảnh hưởng thời tiết khiến mạng Internet có thể bị chập chờn. Việc kết nối máy in nhiệt nội bộ qua cổng USB 2.0 / TCP 9100 giúp Lễ tân in ngay phiếu nhận phòng và hóa đơn trong vòng 0.5 giây bằng lệnh trực tiếp ESC/POS, đảm bảo vận hành quầy tiền sảnh không bao giờ bị đình trệ kể cả khi mất kết nối Internet quốc tế."*

### ❓ Câu 15: "Trong Biểu đồ Thiết kế Dữ liệu (Diagram 28), tại sao phải tách riêng `T_Booking` và `T_BookingNight`? Đây có phải là chuẩn hóa 3NF không?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, đây chính là chuẩn hóa 3NF kinh điển:
> - Nếu gộp ngày đến và ngày đi trong `T_Booking`, ta không thể quản lý chi tiết giá phòng biến động theo từng đêm (ví dụ đêm thứ 7 giá cao hơn đêm ngày thường).
> - Đồng thời, khi khách ở nhiều đêm nhưng đêm 1 ở phòng này, đêm 2 đổi sang phòng khác (Split Stay), nếu không có `T_BookingNight` thì trường `idPhysicalRoom` trong Booking sẽ bị đa trị (Multi-valued attribute), vi phạm nghiêm trọng chuẩn 1NF.
> - Tách `T_BookingNight` giúp quản lý chính xác từng đêm lưu trú, tối ưu hóa câu truy vấn đếm phòng trống bằng phép `COUNT(*)` cực nhanh và đạt chuẩn 3NF thuần khiết."*

### ❓ Câu 16: "Bảng `T_RoomHoldLock` trong Diagram 28 có ý nghĩa gì trong việc chống Overbooking?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, `T_RoomHoldLock` là bảng hiện thực hóa cơ chế **Pessimistic Hold with Time-To-Live (TTL)**. Khi khách bấm đặt phòng, một bản ghi được tạo ra với `expiresAt = now + 15m`. Mọi câu truy vấn kiểm tra phòng trống đều áp dụng công thức: $\text{Số phòng khả dụng} = \text{Tổng kho} - \text{Đã bán} - \text{Khóa đang hoạt động}$. Nhờ đó, dù khách chưa thanh toán tiền, phòng vẫn được giữ chỗ an toàn, loại bỏ hoàn toàn khả năng 2 khách đặt trùng một căn phòng."*

### ❓ Câu 17: "Trong Diagram 28, tại sao có cả bảng `T_CustomerProfile` và `T_Account` riêng biệt?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, đây là bài toán tách biệt giữa Thông tin Định danh Đăng nhập (Authentication Identity) và Hồ sơ Nghiệp vụ Khách hàng (Business Profile):
> - Khách vãng lai đến quầy lễ tân đặt phòng (Walk-in) vẫn cần lưu họ tên, số điện thoại, CCCD trong `T_CustomerProfile` để khai báo tạm trú nhưng **không bắt buộc phải tạo tài khoản đăng nhập web** (trường `idAccount` được phép `NULL`).
> - Tách rời 2 bảng giúp hệ thống hỗ trợ cả khách vãng lai lẫn khách hội viên trực tuyến mà không bị ràng buộc dư thừa dữ liệu."*

### ❓ Câu 18: "Bảng `T_FolioInvoice` và `T_ServiceConsumption` liên kết với nhau như thế nào?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, `T_Booking` là gốc liên kết 1-N với `T_ServiceConsumption` (ghi nhận chi tiết từng lần uống bia minibar, giặt ủi). Khi làm thủ tục trả phòng, `T_FolioInvoice` được sinh ra làm tổng kết tài chính: tổng hợp toàn bộ các dòng tiêu dùng trong `T_ServiceConsumption` thành `serviceSubtotal`, cộng tiền phòng `roomSubtotal`, tính thuế `taxVatAmount`, trừ đi `depositDeducted` để ra số tiền cuối cùng `finalAmount`. Cấu trúc này phản ánh chuẩn xác quy trình kế toán khách sạn quốc tế."*

### ❓ Câu 19: "Hệ thống xử lý bài toán No-Show (khách không đến) như thế nào trên CSDL và sơ đồ buồng phòng?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, sau 23:59 ngày nhận phòng, nếu khách không đến, Lễ tân thực hiện Use Case No-Show trên giao diện Gantt:
> - Trạng thái `bookingStatus` trong `T_Booking` chuyển sang `'NO_SHOW'`.
> - Hệ thống thu phí phạt tương đương tiền cọc 1 đêm đầu tiên theo điều khoản hợp đồng lưu trú.
> - Toàn bộ các đêm lưu trú còn lại trong `T_BookingNight` được cập nhật trạng thái `'RELEASED'` để phòng vật lý được giải phóng ngay lập tức trên sơ đồ Gantt đón khách cho ngày hôm sau."*

### ❓ Câu 20: "Dự án đã được kiểm chứng bằng những bằng chứng kỹ thuật thực tế nào?"
> 🎙️ **Trả lời**: *"Dạ thưa Thầy, toàn bộ 28 biểu đồ thiết kế đã được hiện thực hóa đầy đủ trên nền tảng Backend Python Flask / SQLAlchemy và Frontend Jinja2 / JavaScript Coastal Luxury 5 sao, vượt qua bộ kiểm thử tự động gồm **43/43 tests passed (100%)**:
> - 5 Tests Domain Models (kiểm tra tính toàn vẹn thực thể và quan hệ CSDL).
> - 7 Tests Services Smoke (kiểm tra tính tiền, khóa phòng 15m, hoàn cọc).
> - 5 Tests API Endpoints (kiểm tra giao tiếp Controller và Boundary).
> - 6 Tests Frontend Views (kiểm tra toàn bộ 24 trang giao diện người dùng).
> - 4 Tests E2E Full Lifecycle (kiểm tra trọn vẹn vòng đời: Đặt phòng $\rightarrow$ Check-in $\rightarrow$ Tiêu dùng Minibar $\rightarrow$ Quyết toán $\rightarrow$ Hủy hoàn tiền)."*

---

# LỜI KẾT BÁO CÁO BẢO VỆ
🎙️ **Lời thoại kết thúc**:
> *"Kính thưa Quý Thầy/Cô trong Hội đồng,*
>
> *Hồ sơ 28 biểu đồ của nhóm chúng em là một công trình thiết kế hoàn chỉnh, nhất quán từ góc nhìn chức năng (Use Case), góc nhìn quy trình (Activity), góc nhìn tương tác đối tượng (Sequence BCE), góc nhìn kiến trúc phần mềm (Package & Component), góc nhìn hạ tầng vật lý (Deployment) cho đến thiết kế cơ sở dữ liệu quan hệ chuẩn hóa 3NF.*
>
> *Mọi quyết định thiết kế đều bắt nguồn từ nghiệp vụ thực tế của Khách sạn Sài Gòn - Côn Đảo Resort và được bảo vệ bởi những nguyên lý khoa học phần mềm vững chắc.*
>
> *Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe và xin trân trọng kính mời Hội đồng đặt câu hỏi phản biện ạ!"*
