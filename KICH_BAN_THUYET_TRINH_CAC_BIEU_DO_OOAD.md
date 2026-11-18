# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN OOAD: HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO RESORT

> **Đề tài**: Phân tích & Thiết kế Hệ thống Hướng đối tượng (OOAD) - Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo  
> **Chuẩn mực học thuật**: Chuẩn giáo trình OOAD / Lead Software Architect  
> **Mô hình kiến trúc**: 3 Tầng BCE (Boundary - Control - Entity), CSDL Quan hệ 3NF, Kiến trúc Triển khai 3-Tier  
> **Thời lượng báo cáo tiêu chuẩn**: 15 - 20 phút (Thuyết trình) + 10 phút (Hội đồng phản biện & Vấn đáp)

---

## MỤC LỤC KỊCH BẢN
1. [PHẦN 0: MỞ ĐẦU & TỔNG QUAN BÀI TOÁN NGHIỆP VỤ (02 PHÚT)](#phần-0-mở-đầu--tổng-quan-bài-toán-nghiệp-vụ)
2. [PHẦN 1: MÔ HÌNH HÓA CHỨC NĂNG - HỆ THỐNG BIỂU ĐỒ USE CASE (03 PHÚT)](#phần-1-mô-hình-hóa-chức-năng---hệ-thống-biểu-đồ-use-case)
3. [PHẦN 2: DÒNG CHẢY NGHIỆP VỤ - BỘ BIỂU ĐỒ HOẠT ĐỘNG ACTIVITY DIAGRAMS (03 PHÚT)](#phần-2-dòng-chảy-nghiệp-vụ---bộ-biểu-đồ-hoạt-động-activity-diagrams)
4. [PHẦN 3: MÔ HÌNH DỮ LIỆU TĨNH - BIỂU ĐỒ LỚP LĨNH VỰC DOMAIN CLASS DIAGRAM (02 PHÚT)](#phần-3-mô-hình-dữ-liệu-tĩnh---biểu-đồ-lớp-lĩnh-vực-domain-class-diagram)
5. [PHẦN 4: TRỌNG TÂM THIẾT KẾ ĐỘNG - BỘ 06 BIỂU ĐỒ TRÌNH TỰ SEQUENCE BCE (06 PHÚT)](#phần-4-trọng-tâm-thiết-kế-động---bộ-06-biểu-đồ-trình-tự-sequence-bce)
   - [SD-01: Đặt phòng trực tuyến & Khóa giữ phòng 15 phút (B2C)](#sd-01-đặt-phòng-trực-tuyến--khóa-giữ-phòng-15-phút-b2c)
   - [SD-02: Thủ tục Nhận phòng (Check-in) & Gán phòng vật lý động](#sd-02-thủ-tục-nhận-phòng-check-in--gán-phòng-vật-lý-động)
   - [SD-03: Ghi nhận tiêu dùng dịch vụ phát sinh vào Folio](#sd-03-ghi-nhận-tiêu-dùng-dịch-vụ-phát-sinh-vào-folio)
   - [SD-04: Thủ tục Trả phòng (Check-out) & Quyết toán Folio VAT 5 sao](#sd-04-thủ-tục-trả-phòng-check-out--quyết-toán-folio-vat-5-sao)
   - [SD-05: Vận hành & Cập nhật tiến độ buồng phòng (Housekeeping)](#sd-05-vận-hành--cập-nhật-tiến-độ-buồng-phòng-housekeeping)
   - [SD-06: Hủy đặt phòng trực tuyến & Hoàn tiền cọc bậc thang](#sd-06-hủy-đặt-phòng-trực-tuyến--hoàn-tiền-cọc-bậc-thang)
6. [PHẦN 5: KIẾN TRÚC VẬT LÝ - BIỂU ĐỒ TRIỂN KHAI DEPLOYMENT DIAGRAM (02 PHÚT)](#phần-5-kiến-trúc-vật-lý---biểu-đồ-triển-khai-deployment-diagram)
7. [PHẦN 6: THIẾT KẾ CƠ SỞ DỮ LIỆU CHUẨN HÓA 3NF & UML DATABASE DESIGN (02 PHÚT)](#phần-6-thiết-kế-cơ-sở-dữ-liệu-chuẩn-hóa-3nf--uml-database-design)
8. [PHẦN 7: BỘ CÂU HỎI VẤN ĐÁP PHẢN BIỆN "SỐNG CÒN" (Q&A DEFENSE GUIDE)](#phần-7-bộ-câu-hỏi-vấn-đáp-phản-biện-sống-còn-qa-defense-guide)
9. [PHẦN 8: LỜI KẾT VÀ BÀN GIAO BẢO VỆ](#phần-8-lời-kết-và-bàn-giao-bảo-vệ)

---

## HƯỚNG DẪN KÝ HIỆU TRONG KỊCH BẢN
- 🎙️ **[LỜI THOẠI]**: Lời nói trực tiếp của sinh viên trước Hội đồng. Giọng điệu đĩnh đạc, tự tin, nhấn đúng từ khóa kỹ thuật.
- 👉 **[VISUAL CUE / HÀNH ĐỘNG]**: Hướng dẫn chỉ tay, rê chuột lazer vào thành phần cụ thể trên slide/biểu đồ để người nghe tập trung.
- ⏱️ **[TIMING]**: Thời gian phân bổ tối ưu cho từng phần, tránh bị quá giờ.
- 💡 **[INSIGHT KIẾN TRÚC]**: Điểm cốt lõi trả lời lý do tại sao thiết kế như vậy.

---

## PHẦN 0: MỞ ĐẦU & TỔNG QUAN BÀI TOÁN NGHIỆP VỤ
⏱️ **Thời lượng**: 02 phút  
👉 **Visual Cue**: Trình chiếu Slide Trang bìa & Sơ đồ Tổng thể Kiến trúc

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô trong Hội đồng và các bạn sinh viên,*
>
> *Em xin đại diện nhóm trình bày đồ án tốt nghiệp/bảo vệ học phần Phân tích & Thiết kế Hệ thống Hướng đối tượng với đề tài: **'Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo Resort'**.*
>
> *Khách sạn Sài Gòn - Côn Đảo là khu nghỉ dưỡng biển đảo quy mô cao cấp trực thuộc Saigontourist Group. Khác với các khách sạn thương mại trong đất liền, nghiệp vụ khách sạn biển đảo đối mặt với 3 thách thức thực tế vô cùng phức tạp:*
> 1. *Thứ nhất là bài toán **Tranh chấp phòng trong mùa cao điểm (Race Condition & Overbooking)**: Khách du lịch thường đặt phòng dồn dập vào cùng một thời điểm khi có chuyến bay/tàu cao tốc ra đảo.*
> 2. *Thứ hai là sự **Tách biệt giữa Hạng phòng thương mại (B2C Room Type) và Phòng vật lý thực tế (Physical Room)**: Khách đặt phòng trên mạng chỉ chọn hạng phòng (như Deluxe Hướng Biển, Biệt thự VIP), việc gán vào phòng cụ thể (như Villa 01 hay P.205) chỉ diễn ra khi check-in dựa trên tiến độ dọn dẹp buồng phòng thời gian thực.*
> 3. *Thứ ba là việc quản lý **Hồ sơ chi tiêu Folio tập trung** theo chuẩn quản trị khách sạn quốc tế, tích hợp cơ chế hoàn tiền bậc thang khi tàu bè bị cấm biển do bão gió.*
>
> *Để giải quyết triệt để các bài toán trên, nhóm chúng em đã áp dụng phương pháp luận OOAD tiêu chuẩn, bóc tách hệ thống theo mô hình 3 tầng **BCE (Boundary - Control - Entity)**, chuẩn hóa cơ sở dữ liệu đạt chuẩn **3NF**, và đảm bảo tính khả thi triển khai thực tế. Sau đây, em xin phép đi sâu vào từng biểu đồ thiết kế của hệ thống."*

---

## PHẦN 1: MÔ HÌNH HÓA CHỨC NĂNG - HỆ THỐNG BIỂU ĐỒ USE CASE
⏱️ **Thời lượng**: 03 phút  
👉 **Visual Cue**: Mở biểu đồ `00_So_Do_Use_Case_Tong_Quat.drawio` và các biểu đồ phân rã phân hệ.

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, màn hình trước mắt là **Biểu đồ Use Case Tổng quát** của toàn hệ thống.*
>
> 👉 *[Chỉ vào phía ngoài ranh giới hệ thống]*: *Về mặt tác nhân (Actor), hệ thống bóc tách thành 5 vai trò rõ ràng:*
> - *Phía B2C bên ngoài có **Khách hàng** (chia thành Khách vãng lai và Khách hàng thân thiết VIP có tài khoản).*
> - *Phía nội bộ có 4 vai trò vận hành phân quyền chặt chẽ (RBAC): **Lễ tân tiền sảnh**, **Nhân viên Buồng phòng**, **Quản lý khách sạn**, và **Quản trị hệ thống (Admin)**.*
>
> 👉 *[Chỉ vào System Boundary & 5 Phân hệ chính]*: *Ranh giới hệ thống bao bọc 5 phân hệ chức năng cốt lõi:*
> 1. ***Phân hệ Đặt phòng Trực tuyến B2C**: Cho phép tìm kiếm phòng trống theo thời gian thực, xem chi tiết tiện ích, đặt phòng và thanh toán trực tuyến qua cổng VNPay.*
> 2. ***Phân hệ Tác nghiệp Tiền sảnh (Front Desk)**: Quản lý sơ đồ buồng phòng Gantt Rack trực quan, tiếp nhận khách Check-in, gán số phòng vật lý động, phục vụ khách Walk-in tại quầy, và làm thủ tục Check-out quyết toán.*
> 3. ***Phân hệ Vận hành Buồng phòng (Housekeeping)**: Hỗ trợ nhân viên buồng phòng cập nhật trạng thái phòng qua thiết bị di động theo quy trình 4 bước chuẩn 5 sao (Dirty $\rightarrow$ Cleaning $\rightarrow$ Clean $\rightarrow$ Inspected).*
> 4. ***Phân hệ Quản trị Doanh thu & Thiết lập Danh mục**: Dành cho Quản lý cấu hình giá phòng linh hoạt theo mùa, áp dụng Voucher khuyến mãi, và ban hành chính sách hoàn tiền cọc.*
> 5. ***Phân hệ Quản trị Hệ thống**: Quản trị tài khoản người dùng, phân quyền vai trò và sao lưu nhật ký an ninh.*

👉 *[Chỉ vào các mối quan hệ `<<include>>` và `<<extend>>`]*:
> *"Điểm đặc biệt trong thiết kế Use Case của nhóm là tuân thủ tuyệt đối ngữ nghĩa học thuật:*
> - *Các quan hệ **`<<include>>`** được dùng khi một chức năng luôn luôn bắt buộc phải gọi chức năng con để hoàn tất giá trị. Ví dụ: Use Case 'Đặt phòng trực tuyến' bắt buộc phải `<<include>>` 'Kiểm tra phòng trống & Khóa giữ phòng tạm thời 15 phút' và `<<include>>` 'Thanh toán trực tuyến'. Không thể có một đơn đặt phòng thành công mà bỏ qua việc giữ chỗ và thanh toán.*
> - *Các quan hệ **`<<extend>>`** được dùng nghiêm ngặt tại các Điểm mở rộng (Extension Point) có điều kiện bảo vệ. Ví dụ: Use Case 'Áp dụng mã giảm giá / Voucher' mở rộng cho 'Đặt phòng' chỉ khi khách hàng có mã ưu đãi hợp lệ; hay 'Hủy đặt phòng & Hoàn tiền' mở rộng cho 'Quản lý lịch sử đặt phòng' khi đơn chưa đến ngày nhận phòng.*
> - *Nhóm tuyệt đối không biến các thao tác vụn vặt như bấm nút, gõ bàn phím thành Use Case, mà mỗi Use Case là một đơn vị công việc hoàn chỉnh mang lại giá trị trọn vẹn cho tác nhân."*

---

## PHẦN 2: DÒNG CHẢY NGHIỆP VỤ - BỘ BIỂU ĐỒ HOẠT ĐỘNG ACTIVITY DIAGRAMS
⏱️ **Thời lượng**: 03 phút  
👉 **Visual Cue**: Trình chiếu `bieu-do-hoat-dong-perfect.drawio` (các trang AD-01 đến AD-05)

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, để mô hình hóa khía cạnh động và phân định trách nhiệm xử lý giữa các chủ thể, nhóm đã xây dựng bộ 05 Biểu đồ Hoạt động (Activity Diagrams) tương ứng với 5 quy trình cốt lõi.*
>
> 👉 *[Chỉ vào cấu trúc Làn bơi Swimlane trên AD-01]*:
> *Mỗi biểu đồ hoạt động được chia thành 3 đến 4 làn bơi (Swimlanes) trực giao:*
> - *Làn 1: **Khách hàng / Nhân viên tác nghiệp** (Actor khởi phát thao tác).*
> - *Làn 2: **Hệ thống Web Portal / PMS Server** (Xử lý logic nghiệp vụ và kiểm tra ràng buộc).*
> - *Làn 3: **Cổng thanh toán điện tử VNPay** (Bên thứ ba xử lý giao dịch tài chính).*
> - *Làn 4: **Cơ sở Dữ liệu & Worker ngầm** (Đảm bảo lưu vết và dọn dẹp tài nguyên).*
>
> 👉 *[Chỉ vào AD-01: Quy trình Đặt phòng & Khóa giữ 15 phút]*:
> - *Tại điểm bắt đầu, Khách chọn loại phòng và ngày lưu trú $\rightarrow$ Hệ thống kiểm tra quỹ phòng khả dụng.*
> - *Tại nút rẽ nhánh Decision: Nếu còn phòng, hệ thống không chỉ kiểm tra mà ngay lập tức thực thi cơ chế **Tạo Lock giữ phòng tạm thời 15 phút** $\rightarrow$ Hệ thống điều hướng sang Cổng VNPay.*
> - *Một thanh đồng bộ **Fork** phân nhánh xử lý: Một nhánh khởi động bộ đếm đếm ngược Timer 15 phút, nhánh kia chờ kết quả Webhook IPN từ VNPay.*
> - *Nếu khách thanh toán thành công trong 15 phút: Hệ thống xác nhận đơn CONFIRMED và chuyển tiền cọc vào Folio.*
> - *Nếu hết 15 phút mà không thanh toán: Worker ngầm tự động kích hoạt tiến trình giải phóng Lock, trả lại quỹ phòng cho khách khác ngay tức khắc.*
>
> 👉 *[Chỉ vào AD-02 & AD-04]*:
> - *Tại quy trình Check-in (AD-02), hệ thống hỗ trợ lễ tân gán phòng vật lý theo thời gian thực dựa trên trạng thái buồng phòng sạch.*
> - *Tại quy trình Check-out (AD-04), hệ thống tích hợp điểm rẽ nhánh kiểm tra tài chính: Bắt buộc số dư Folio phải bằng 0 (Balance = 0) mới cho phép in hóa đơn VAT và đổi trạng thái phòng sang 'Dirty' để kích hoạt đội buồng phòng vào dọn."*

---

## PHẦN 3: MÔ HÌNH DỮ LIỆU TĨNH - BIỂU ĐỒ LỚP LĨNH VỰC DOMAIN CLASS DIAGRAM
⏱️ **Thời lượng**: 02 phút  
👉 **Visual Cue**: Mở `00_Bieu_Do_Lop_Linh_Vuc_Domain_Class.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, đây là **Biểu đồ Lớp Lĩnh vực (Domain Class Diagram)** - xương sống định hình cấu trúc dữ liệu hướng đối tượng của hệ thống.*
>
> 👉 *[Chỉ vào cấu trúc 3 ngăn của từng Lớp]*:
> *Mỗi lớp được thiết kế theo đúng chuẩn UML 3 ngăn: **Tên lớp**, **Thuộc tính nghiệp vụ**, và **Phương thức hành vi**. Điểm cốt lõi nhóm tuân thủ là nguyên lý **Information Expert** của mẫu GRASP: Chỉ đưa vào các phương thức tính toán nghiệp vụ thuần túy như `tinhTongTien()`, `kiemTraPhongTrong()`, `tinhTienPhatHuyPhong()`. Tuyệt đối không để rò rỉ các phương thức hạ tầng kỹ thuật như `connectDB()`, `saveSQL()` hay các hàm `get/set` vụn vặt.*
>
> 👉 *[Chỉ vào các mối quan hệ sống còn trên biểu đồ]*:
> 1. ***Quan hệ Hợp thành (Composition - Hình thoi đen đặc)** giữa `BookingMaster` và `BookingNight`: Một đơn đặt phòng được cấu thành từ các đêm phòng cụ thể. Đêm phòng không thể tồn tại độc lập nếu đơn đặt phòng bị xóa. Vòng đời của chúng gắn kết sinh tử.*
> 2. ***Quan hệ Hợp thành** giữa `ServiceFolio` và `FolioItem`: Hồ sơ quyết toán Folio sở hữu các dòng dịch vụ phát sinh (minibar, giặt ủi, ẩm thực). Toàn bộ chi tiêu đều được kiểm soát chặt chẽ trong Folio.*
> 3. ***Quan hệ Thu nạp (Aggregation - Hình thoi trắng rỗng)** giữa `Hotel` và `RoomType`, giữa `RoomType` và `PhysicalRoom`: Khách sạn quản lý nhiều hạng phòng, hạng phòng quản lý các phòng vật lý thực tế. Khi một phòng vật lý tạm khóa để bảo trì, hạng phòng và khách sạn vẫn tồn tại độc lập.*
> 4. ***Quan hệ Kế thừa (Generalization - Mũi tên tam giác trắng)**: Lớp cha `Account` bao quát các thuộc tính chung (mã định danh, thông tin đăng nhập, vai trò) và được kế thừa bởi `CustomerAccount` (bổ sung điểm tích lũy Loyalty, hạng thẻ Vàng/Bạc) và `StaffAccount` (bổ sung chức danh, mã nhân viên).*
> 5. ***Bản số (Multiplicity)**: Được xác định chính xác ở 2 đầu liên kết: Một khách hàng có thể có `0..*` đơn đặt phòng, một đơn đặt phòng bắt buộc thuộc về đúng `1` khách hàng; một đơn phòng có `1..*` đêm lưu trú."*

---

## PHẦN 4: TRỌNG TÂM THIẾT KẾ ĐỘNG - BỘ 06 BIỂU ĐỒ TRÌNH TỰ SEQUENCE BCE
⏱️ **Thời lượng**: 06 phút  
👉 **Visual Cue**: Trình chiếu từng biểu đồ trong bộ 6 biểu đồ Sequence: SD-01 đến SD-06.

🎙️ **[LỜI THOẠI MẪU - DẪN NHẬP BCE]**:
> *"Kính thưa Thầy/Cô, đây là phần cốt lõi và chi tiết nhất trong hồ sơ thiết kế OOAD của nhóm. Toàn bộ 06 biểu đồ trình tự được xây dựng theo chuẩn mực thiết kế hướng đối tượng **BCE Pattern (Boundary - Control - Entity)** với sự tham gia của 3 tầng đối tượng:*
> - **Boundary ($\vdash\bigcirc$)**: Đại diện cho giao diện người dùng, nơi thu nhận sự kiện và hiển thị dữ liệu.*
> - **Control ($\circlearrowleft$)**: Đại diện cho tầng điều khiển xử lý logic nghiệp vụ, điều phối nghiệp vụ giao dịch.*
> - **Entity ($\ominus$)**: Đại diện cho các đối tượng thực thể lưu trữ trạng thái và dữ liệu bài toán.*
>
> *Quy tắc bất di bất dịch nhóm áp dụng trên tất cả biểu đồ là: **CẤM NHẢY CÓC**. Boundary không được phép gọi trực tiếp vào Entity; Entity không được tự ý gửi trả dữ liệu trực tiếp về Boundary mà mọi tương tác đều phải qua tầng Control. Tất cả các lời gọi đồng bộ (Sync Call) đều có vạch kích hoạt (Activation Bar) đối xứng với mũi tên trả về (Return Message nét đứt)."*

---

### SD-01: Đặt phòng trực tuyến & Khóa giữ phòng 15 phút (B2C)
👉 **Visual Cue**: Mở `01_SD_DatPhong_KhoaPhong_B2C.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"Tại SD-01, biểu đồ mô tả kịch bản Khách hàng đặt phòng trực tuyến.*
>
> 👉 *[Chỉ vào bước tạo Lock]*:
> - *Khách hàng tìm kiếm phòng qua `:SearchBookingUI` $\rightarrow$ `:BookingService` tiếp nhận yêu cầu $\rightarrow$ gọi sang `:RoomInventory` để kiểm tra số lượng khả dụng.*
> - *Điểm đột phá kiến trúc: Ngay khi khách bấm 'Tiến hành đặt phòng', `:BookingService` không tạo ngay đơn hàng vĩnh viễn mà gọi hàm `createTemporaryHold(roomTypeId, dates, 15_minutes)` vào thực thể `:RoomLock`.*
> - *Khung **Alt** phân nhánh rõ ràng:*
>   - *[Nhánh 1 - Khóa thành công]: `:BookingService` khởi tạo bản ghi `:Booking` ở trạng thái `'HOLD'` và gọi `:VNPayGateway` tạo URL thanh toán. Boundary hiển thị đồng hồ đếm ngược 15 phút.*
>   - *Khi nhận được tín hiệu thanh toán thành công: `:BookingService` cập nhật trạng thái đơn sang `'CONFIRMED'`, xóa bản ghi tạm trong `:RoomLock`, và sinh chứng từ thanh toán `:PaymentTransaction`.*
>   - *[Nhánh 2 - Hết phòng hoặc Quá hạn]: `:BookingService` từ chối, giải phóng Lock và hiển thị thông báo lỗi thân thiện cho khách hàng."*

---

### SD-02: Thủ tục Nhận phòng (Check-in) & Gán phòng vật lý động
👉 **Visual Cue**: Mở `02_SD_NhanPhong_CheckIn_GanPhong.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, SD-02 giải quyết bài toán cốt lõi của khách sạn 5 sao: Gán phòng thực tế tại quầy lễ tân.*
>
> 👉 *[Chỉ vào tương tác giữa Lễ tân, Sơ đồ Gantt và Buồng phòng]*:
> - *Khi khách đến tiền sảnh, Lễ tân tra cứu mã đơn trên `:FrontDeskGanttUI` $\rightarrow$ `:CheckInController` kiểm tra trạng thái đơn hàng.*
> - *Hệ thống truy vấn thực thể `:PhysicalRoom` để lọc ra danh sách các phòng thực tế thỏa mãn 2 điều kiện:*
>   1. *Thuộc đúng hạng phòng mà khách đã đặt.*
>   2. *Trạng thái buồng phòng phải là `'Clean'` hoặc `'Inspected'` (đã dọn sạch và quản lý đã nghiệm thu).*
> - *Lễ tân chọn phòng vật lý (ví dụ: Villa 01) $\rightarrow$ `:CheckInController` cập nhật số phòng vào đơn, đổi trạng thái đơn sang `'CHECKED_IN'`, đồng thời đổi trạng thái phòng vật lý sang `'Occupied'` (Đang có khách).*
> - *Hệ thống tự động kích hoạt việc tạo hồ sơ `:ServiceFolio` sẵn sàng cho các chi tiêu minibar trong suốt kỳ lưu trú."*

---

### SD-03: Ghi nhận tiêu dùng dịch vụ phát sinh vào Folio
👉 **Visual Cue**: Mở `03_SD_GhiNhan_DichVu_PhatSinh.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"SD-03 thể hiện kiến trúc kế toán thu chi minh bạch qua tài khoản Folio.*
>
> 👉 *[Chỉ vào bước Post Charge]*:
> - *Khi khách sử dụng nước uống trong tủ lạnh Minibar hoặc dịch vụ Giặt ủi, Nhân viên nhập số phòng và danh mục dịch vụ trên `:ServicePostingUI`.*
> - *`:FolioService` nhận lệnh, tự động tra cứu xem phòng đó hiện tại tương ứng với mã đơn `:Booking` nào đang lưu trú.*
> - *Sau khi xác thực đơn đang 'CHECKED_IN', `:FolioService` thực thi thông điệp `<<create>>` sinh ra một bản ghi `:FolioItem` mới với đơn giá, số lượng, thời gian, và cập nhật tăng lũy kế trường `current_balance` trong `:ServiceFolio`.*
> - *Cơ chế này ngăn chặn tuyệt đối việc thất thoát doanh thu dịch vụ buồng phòng."*

---

### SD-04: Thủ tục Trả phòng (Check-out) & Quyết toán Folio VAT 5 sao
👉 **Visual Cue**: Mở `04_SD_TraPhong_QuyetToan_CheckOut.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"SD-04 là quy trình kết thúc kỳ lưu trú với yêu cầu tuân thủ chế độ tài chính khắt khe.*
>
> 👉 *[Chỉ vào bước Tất toán Folio và In Hóa đơn GTGT]*:
> - *Lễ tân khởi chạy thao tác check-out trên `:CheckoutFolioUI` $\rightarrow$ `:CheckoutController` gọi `:FolioService` tính toán tổng chi phí cuối cùng: `Tiền phòng + Tiền dịch vụ phát sinh - Tiền đặt cọc trước`.*
> - *Khung **Alt** xử lý thanh toán:*
>   - *Nếu khách còn nợ (Balance > 0): Lễ tân thu tiền (Tiền mặt/Quẹt thẻ POS) $\rightarrow$ ghi nhận chứng từ thanh toán `:PaymentTransaction` $\rightarrow$ Balance trở về 0.*
>   - *Nếu cọc thừa: Hệ thống xuất phiếu chi hoàn lại tiền mặt cho khách.*
> - *Sau khi số dư Folio cân bằng (`Balance == 0`), hệ thống thực hiện đồng thời 3 hành động:*
>   1. *Đổi trạng thái đơn `:Booking` sang `'CHECKED_OUT'`.*
>   2. *Tạo bản ghi hóa đơn điện tử `:Invoice` theo chuẩn Saigontourist Group (Mã số thuế `0312456789-001`, thuế suất VAT 8-10%) và gửi lệnh in ra máy in nhiệt `:POSPrinter`.*
>   3. *Ngay lập tức gửi thông điệp đổi trạng thái phòng vật lý `:PhysicalRoom` sang `'Dirty'` để thông báo cho đội buồng phòng tiến hành dọn dẹp."*

---

### SD-05: Vận hành & Cập nhật tiến độ buồng phòng (Housekeeping)
👉 **Visual Cue**: Mở `05_SD_VeSinh_BuongPhong_Housekeeping.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"SD-05 thể hiện sự khép kín trong chu trình vận hành giữa Tiền sảnh và Buồng phòng.*
>
> 👉 *[Chỉ vào luồng chuyển trạng thái phòng]*:
> - *Nhân viên buồng phòng sử dụng điện thoại/máy tính bảng đăng nhập `:HousekeepingMobileUI` $\rightarrow$ Hệ thống hiển thị danh sách phòng cần làm sạch (trạng thái `'Dirty'`).*
> - *Khi bắt đầu dọn, nhân viên bấm 'Bắt đầu dọn' $\rightarrow$ chuyển sang `'Cleaning'`.*
> - *Dọn xong, nhân viên kiểm tra minibar, bấm 'Hoàn thành' $\rightarrow$ hệ thống chuyển sang `'Clean'`.*
> - *Tổ trưởng buồng phòng kiểm tra chất lượng thực tế $\rightarrow$ bấm 'Nghiệm thu' $\rightarrow$ trạng thái phòng đổi thành `'Inspected'`.*
> - *Ngay lập tức, sơ đồ Gantt tại quầy lễ tân tự động nhận tín hiệu phòng sẵn sàng đón lượt khách mới mà không cần nhân viên phải gọi bộ đàm hay ghi chép sổ sách thủ công."*

---

### SD-06: Hủy đặt phòng trực tuyến & Hoàn tiền cọc bậc thang
👉 **Visual Cue**: Mở `06_SD_HuyPhong_HoanTien_B2C.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, đây là biểu đồ đặc thù vừa được nhóm hoàn thiện để giải quyết bài toán hoàn tiền minh bạch khi khách gặp sự cố không thể ra đảo.*
>
> 👉 *[Chỉ vào bước tính Refund Policy bậc thang]*:
> - *Khách hàng vào lịch sử đơn phòng trên `:BookingHistoryUI`, bấm 'Yêu cầu hủy phòng' $\rightarrow$ `:BookingCancellationService` tiếp nhận.*
> - *Tầng Control truy vấn thời gian nhận phòng và gọi thực thể chính sách `:RefundPolicy` với tham số `hoursRemaining` (số giờ còn lại tính đến 14:00 ngày check-in):*
>   - *Hủy trước $\ge 72$ giờ (3 ngày): **Hoàn 100%** tiền cọc.*
>   - *Hủy từ $24$ đến dưới $72$ giờ: **Hoàn 50%** tiền cọc (thu phí phạt 50%).*
>   - *Hủy dưới $24$ giờ hoặc No-show: **Hoàn 0%** (khách mất toàn bộ cọc).*
> - *Hệ thống hiển thị bảng tính xem trước (Preview) cho khách xác nhận.*
> - *Khi khách bấm xác nhận hủy: Hệ thống cập nhật `:Booking` thành `'Canceled'`, sinh biên bản hủy `:CancellationRecord`, ghi chứng từ hoàn tiền âm trong `:PaymentTransaction`, và lập tức **giải phóng các đêm phòng `:BookingNight`** để mở lại quỹ phòng trống cho khách hàng khác đặt trên mạng."*

---

## PHẦN 5: KIẾN TRÚC VẬT LÝ - BIỂU ĐỒ TRIỂN KHAI DEPLOYMENT DIAGRAM
⏱️ **Thời lượng**: 02 phút  
👉 **Visual Cue**: Mở `07_Deployment_Diagram_Saigon_Condao.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, để chứng minh hệ thống không chỉ nằm trên bản vẽ lý thuyết mà hoàn toàn có khả năng đóng gói đưa vào vận hành thực tế, nhóm đã thiết kế **Biểu đồ Triển khai Vật lý (UML 2.x Deployment Diagram)** theo kiến trúc 3 tầng (3-Tier Enterprise Architecture).*
>
> 👉 *[Chỉ vào Tầng 1: Client Tier]*:
> - *Bao gồm thiết bị của Khách hàng (`:KhachHangDevice`), Thiết bị di động của Buồng phòng (`:HousekeepingMobile` chạy Web PWA), và Máy trạm của Lễ tân (`:FrontDeskWorkstation` chạy Windows 11).*
> - *Máy trạm lễ tân kết nối trực tiếp với máy in hóa đơn nhiệt `:ThermalReceiptPrinter` qua giao thức cáp `USB 2.0 / Raw TCP Port 9100`.*
>
> 👉 *[Chỉ vào Tầng 2: Application Server Tier]*:
> - *Máy chủ ứng dụng chạy hệ điều hành Ubuntu Linux 22.04 LTS.*
> - *Tầng biên sử dụng **Nginx Web Server** làm Reverse Proxy, xử lý mã hóa bảo mật `TLS 1.3 / HTTPS Port 443` cho khách hàng và phân đoạn mạng nội bộ `VLAN 20` cho nhân viên.*
> - *Đặc biệt, kênh kết nối giữa Lễ tân và Máy chủ hỗ trợ `WebSocket (WSS)` thời gian thực để cập nhật sơ đồ phòng ngay tức khắc.*
> - *Bên trong máy chủ là môi trường **Python WSGI Application Container** chạy các dịch vụ: `BookingService`, `FolioSettlementService`, `CancellationService`, `HousekeepingService`, và tiến trình **Cron Background Daemon** (`cron_worker.py`) chuyên tự động dọn dẹp các phòng giữ chỗ quá hạn 15 phút.*
>
> 👉 *[Chỉ vào Tầng 3: Data & External Tier]*:
> - *Máy chủ Cơ sở Dữ liệu chuyên dụng nằm trong phân vùng mạng an toàn (`Dedicated DB Subnet`), giao tiếp qua giao thức bảo mật `ODBC / TCP Port 1433`.*
> - *Hệ thống liên kết với 2 dịch vụ điện toán đám mây ngoại vi: Cổng thanh toán tài chính **VNPay** qua `RESTful API / Webhook IPN` và Hệ thống Mail giao dịch **Cloud Mail Gateway** qua `SMTP Port 587` để gửi vé đặt phòng và hóa đơn điện tử tự động cho du khách."*

---

## PHẦN 6: THIẾT KẾ CƠ SỞ DỮ LIỆU CHUẨN HÓA 3NF & UML DATABASE DESIGN
⏱️ **Thời lượng**: 02 phút  
👉 **Visual Cue**: Mở `08_UML_Database_Design_Diagram_Saigon_Condao.drawio` và `00_Bieu_Do_ERD_Database_3NF.drawio`

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, sản phẩm cuối cùng nhưng là nền tảng chịu tải của toàn bộ hệ thống là **Biểu đồ Thiết kế Cơ sở Dữ liệu quan hệ đạt chuẩn 3NF (Third Normal Form)**.*
>
> 👉 *[Chỉ vào việc xóa bỏ God-table]*:
> - *Trong các hệ thống đặt phòng cũ thường mắc phải lỗi phản mẫu kiến trúc (Anti-pattern) là sử dụng 'God Table' - tức là nhồi nhét tất cả thông tin khách, số phòng, số tiền cọc, chi tiêu minibar và trạng thái buồng phòng vào một bảng duy nhất `New_Bookings`. Điều này gây ra dư thừa dữ liệu trầm trọng và dị thường cập nhật (Update Anomaly).*
> - *Nhóm đã thực hiện chuẩn hóa 3NF triệt để:*
>   1. ***Chuẩn hóa 1NF**: Mọi thuộc tính đều mang giá trị nguyên tố, không có cột đa trị (ví dụ: tách danh sách ngày lưu trú thành từng dòng riêng biệt trong bảng `booking_nights`).*
>   2. ***Chuẩn hóa 2NF**: Loại bỏ phụ thuộc hàm từng phần. Toàn bộ các bảng có khóa chính phức hợp đều phụ thuộc hoàn toàn vào khóa chính.*
>   3. ***Chuẩn hóa 3NF**: Loại bỏ phụ thuộc bắc cầu. Tách riêng bảng danh mục Khách sạn (`dim_hotels`), Hạng phòng (`dim_room_types`), Phòng vật lý (`physical_rooms`), Khách hàng (`users/customers`), và Bảng tài khoản Folio (`service_folios`).*
>
> 👉 *[Chỉ vào các cặp Khóa chính (PK) và Khóa ngoại (FK)]*:
> - *Mối quan hệ 1-N giữa `dim_room_types` và `physical_rooms` đảm bảo quản lý chính xác 14 phòng vật lý thực tế của resort.*
> - *Bảng `booking_master` giữ vai trò trung tâm, liên kết với `booking_nights` để kiểm soát lịch trống, liên kết với `service_folios` để kiểm soát chi tiêu, và liên kết với `payment_transactions` để lưu vết lịch sử dòng tiền theo chuẩn kiểm toán kế toán.*
> - *Cơ sở dữ liệu đã được kiểm thử với 43/43 ca kiểm thử tự động (Unit & Integration Tests) vượt qua 100%."*

---

## PHẦN 7: BỘ CÂU HỎI VẤN ĐÁP PHẢN BIỆN "SỐNG CÒN" (Q&A DEFENSE GUIDE)
> 💡 *Đây là bộ cẩm nang chuẩn bị sẵn để sinh viên trả lời trôi chảy khi Hội đồng đặt câu hỏi hóc búa.*

### ❓ Câu 1 (Về Sequence & BCE): *"Tại sao nhóm lại sử dụng mô hình BCE (Boundary - Control - Entity) để vẽ Sequence Diagram mà không dùng trực tiếp mô hình MVC hoặc vẽ thẳng giao diện gọi CSDL?"*
> 🎙️ **Trả lời chuẩn Lead Architect**:  
> *"Dạ thưa Thầy/Cô, trong phân tích thiết kế hướng đối tượng theo tiến trình thống nhất UP/RUP, **BCE** là mẫu phân tích chuẩn mực (Analysis Robustness Pattern) giúp bóc tách trách nhiệm hệ thống ở tầng khái niệm cao hơn:*
> - *Vẽ trực tiếp giao diện gọi CSDL là vi phạm nghiêm trọng nguyên lý phân lớp, làm lộ chi tiết lưu trữ kỹ thuật lên tầng trình diễn.*
> - *MVC là mẫu kiến trúc ở tầng cài đặt mã nguồn (Implementation Architecture), trong khi BCE tập trung mô hình hóa hành vi nghiệp vụ của bài toán: Boundary đại diện cho giao diện tương tác người dùng, Control đóng vai trò nhạc trưởng điều phối nghiệp vụ giao dịch độc lập với framework, và Entity là các thực thể mang dữ liệu nghiệp vụ.*
> - *Việc tuân thủ BCE giúp hệ thống có tính mở cao (Open-Closed Principle): Khi chúng em thay đổi giao diện từ Web sang Mobile App hoặc thay đổi CSDL từ SQLite sang PostgreSQL, toàn bộ tầng nghiệp vụ Control và Entity hoàn toàn không bị ảnh hưởng."*

---

### ❓ Câu 2 (Về Concurrency & Race Condition): *"Cơ chế khóa phòng 15 phút xử lý thế nào nếu hai khách hàng cùng bấm 'Đặt phòng' cho căn biệt thự duy nhất tại cùng một tích tắc (Race Condition)?"*
> 🎙️ **Trả lời chuẩn Lead Architect**:  
> *"Dạ thưa Thầy/Cô, đây chính là bài toán xung đột tranh chấp tài nguyên (Resource Contention) kinh điển trong ngành khách sạn.*
> - *Nhóm giải quyết bằng cơ chế **Khóa bi quan có thời hạn (Pessimistic Hold with TTL - Time To Live)** thông qua tầng `RoomLockService`.*
> - *Khi hai yêu cầu gửi đến cùng một thời điểm, tầng Control sẽ bọc thao tác kiểm tra và ghi bản ghi khóa phòng trong một Transaction nguyên tử (`Atomic Database Transaction` với mức cô lập `SERIALIZABLE` hoặc cơ chế `Atomic UPDATE ... WHERE status = 'AVAILABLE'`).*
> - *Yêu cầu nào chạm vào DB trước mili-giây sẽ giành được quyền tạo bản ghi trong bảng `room_locks` với thời hạn 15 phút. Yêu cầu đến sau mili-giây lập tức nhận kết quả '0 hàng bị ảnh hưởng' và hệ thống trả về thông báo phòng đang được khách khác giữ chỗ.*
> - *Tiến trình ngầm `cron_worker.py` liên tục quét các bản ghi khóa có `expires_at < CURRENT_TIMESTAMP` để giải phóng tự động nếu khách đầu tiên từ bỏ thanh toán."*

---

### ❓ Câu 3 (Về Kiến trúc Dữ liệu): *"Tại sao nhóm lại tách riêng `BookingMaster` và `BookingNight` mà không lưu ngày đến (arrival_date) và ngày đi (departure_date) ngay trong một bảng Booking duy nhất?"*
> 🎙️ **Trả lời chuẩn Lead Architect**:  
> *"Dạ thưa Thầy/Cô, việc tách `BookingNight` là quyết định thiết kế then chốt để đạt chuẩn 3NF và tối ưu hóa truy vấn kiểm tra phòng trống:*
> 1. *Nếu chỉ lưu `arrival_date` và `departure_date`, khi muốn kiểm tra xem ngày 20/11 khách sạn còn loại phòng Deluxe không, câu truy vấn SQL sẽ phải dùng các biểu thức phức tạp `BETWEEN` hoặc quét toàn bộ bảng (`Full Table Scan`), gây tắc nghẽn hiệu năng.*
> 2. *Bằng cách bóc tách ra bảng `booking_nights` (mỗi dòng đại diện cho đúng 1 đêm lưu trú của một đơn), việc kiểm tra phòng trống trở thành phép đếm đơn giản: `COUNT(*) FROM booking_nights WHERE stay_date = '2026-11-20' AND room_type_id = ?`.*
> 3. *Hơn nữa, trong trường hợp khách đặt phòng kéo dài 5 ngày nhưng muốn đổi phòng giữa chừng ở ngày thứ 3, cấu trúc `BookingNight` cho phép gán phòng vật lý linh hoạt cho từng đêm riêng lẻ mà không làm vỡ cấu trúc của toàn đơn hàng."*

---

### ❓ Câu 4 (Về Kế toán Khách sạn Folio): *"Khái niệm 'Folio' trong hệ thống này đóng vai trò gì và tại sao không cộng dồn tiền minibar thẳng vào tổng tiền của đơn đặt phòng?"*
> 🎙️ **Trả lời chuẩn Lead Architect**:  
> *"Dạ thưa Thầy/Cô, trong nghiệp vụ khách sạn chuẩn quốc tế (PMS), **Folio** là sổ cái tài khoản công nợ của phòng.*
> - *Tổng tiền đơn phòng (`total_amount`) ban đầu là số tiền dự kiến tính theo tiền phòng thuần túy được ký kết khi đặt phòng.*
> - *Tuy nhiên, trong suốt kỳ nghỉ, khách có thể phát sinh hàng chục dịch vụ khác nhau: ăn sáng, gọi đồ uống minibar, giặt ủi, thuê xe máy tham quan đảo, hoặc khách làm vỡ đồ đạc cần bồi thường.*
> - *Nếu cộng dồn trực tiếp vào đơn đặt phòng sẽ làm sai lệch giá trị hợp đồng ban đầu, gây rủi ro kiểm toán và không thể xuất hóa đơn chi tiết phân tách các mức thuế suất GTGT khác nhau (tiền phòng VAT khác tiền rượu bia dịch vụ).*
> - *Tài khoản `ServiceFolio` tách biệt cho phép ghi nhận đa khoản thu/chi theo thời gian thực (Posting Charges) và chỉ thực hiện đóng sổ (Settlement) khi lễ tân hoàn tất thủ tục check-out."*

---

### ❓ Câu 5 (Về Use Case Include vs Extend): *"Trong biểu đồ Use Case, khi nào dùng `<<include>>` và khi nào dùng `<<extend>>`? Hãy chỉ ra ví dụ cụ thể nhất trên biểu đồ của nhóm."*
> 🎙️ **Trả lời chuẩn Lead Architect**:  
> *"Dạ thưa Thầy/Cô:*
> - *`<<include>>` thể hiện mối quan hệ bao hàm bắt buộc: Use Case cơ sở không thể hoàn thành nếu không thực thi Use Case được include. Trên biểu đồ của nhóm: Use Case 'Đặt phòng trực tuyến' bắt buộc `<<include>>` 'Kiểm tra phòng trống & Khóa giữ phòng 15 phút'. Luồng chính của hệ thống luôn luôn chạy qua bước này, mũi tên nét đứt trỏ xuôi từ Use Case gốc sang Use Case được bao hàm.*
> - *`<<extend>>` thể hiện sự mở rộng có điều kiện: Use Case mở rộng chỉ được kích hoạt khi thỏa mãn một điều kiện nghiệp vụ tại Điểm mở rộng (Extension Point), và nếu không có nó thì Use Case cơ sở vẫn hoàn thành bình thường. Ví dụ: Use Case 'Áp dụng Voucher giảm giá' mở rộng cho 'Đặt phòng trực tuyến' chỉ khi khách hàng có mã và lựa chọn sử dụng. Mũi tên nét đứt trỏ ngược từ Use Case mở rộng về Use Case gốc.*
> - *Nhóm tuân thủ nghiêm ngặt chuẩn UML 2.x, không nhầm lẫn hướng mũi tên của 2 quan hệ này."*

---

## PHẦN 8: LỜI KẾT VÀ BÀN GIAO BẢO VỆ
⏱️ **Thời lượng**: 01 phút  
👉 **Visual Cue**: Trình chiếu Slide Cảm ơn & Thông tin thành viên nhóm

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô trong Hội đồng,*
>
> *Thông qua toàn bộ hồ sơ thiết kế từ **Mô hình chức năng Use Case**, **Dòng chảy nghiệp vụ Activity**, **Cấu trúc tĩnh Domain Class**, **Hành vi động 3 tầng Sequence BCE**, cho đến **Kiến trúc Triển khai Deployment** và **Mô hình CSDL 3NF**, nhóm chúng em đã giải quyết trọn vẹn bài toán vận hành của Khách sạn Sài Gòn - Côn Đảo Resort.*
>
> *Hệ thống đã chứng minh được tính đúng đắn về mặt lý thuyết hướng đối tượng, sự chặt chẽ về nghiệp vụ khách sạn thực tế, và khả năng vận hành ổn định với 100% ca kiểm thử tự động đã vượt qua.*
>
> *Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe bài thuyết trình của nhóm. Nhóm chúng em rất mong nhận được những ý kiến đóng góp quý báu từ Hội đồng để hoàn thiện hệ thống hơn nữa.*
>
> *Em xin trân trọng kính mời Thầy/Cô đặt câu hỏi phản biện ạ!"*
