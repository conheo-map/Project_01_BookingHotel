# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN OOAD TOÀN DIỆN (PHIÊN BẢN CẦM TAY CHỈ VIỆC)
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO RESORT

> **Quy chuẩn**: Phân tích Thiết kế Hệ thống Hướng đối tượng (OOAD) - Chuẩn RUP/UML 2.x & Lead Enterprise Architect  
> **Kiến trúc ứng dụng**: 3 Tầng Phân tích BCE (Boundary - Control - Entity)  
> **Kiến trúc vật lý**: 3-Tier Enterprise (Client - Application Server - Database & External Services)  
> **Mô hình dữ liệu**: CSDL Quan hệ chuẩn hóa bậc 3 (3NF)  
> **Thời lượng báo cáo**: 15 - 20 phút trình bày + 10 phút vấn đáp phản biện  

---

## MỤC LỤC KỊCH BẢN CHI TIẾT
- [1. Lời mở đầu & Thiết lập bối cảnh bài toán](#1-lời-mở-đầu--thiết-lập-bối-cảnh-bài-toán-02-phút)
- [2. Phân tích chức năng - Hệ thống Biểu đồ Use Case](#2-phân-tích-chức-năng---hệ-thống-biểu-đồ-use-case-03-phút)
  - [2.1. Use Case tổng quát & 5 Tác nhân (Actors)](#21-use-case-tổng-quát--5-tác-nhân-actors)
  - [2.2. Phân rã 5 phân hệ chức năng](#22-phân-rã-5-phân-hệ-chức-năng)
  - [2.3. Quy chuẩn học thuật về `<<include>>` và `<<extend>>`](#23-quy-chuẩn-học-thuật-về-include-và-extend)
- [3. Dòng chảy nghiệp vụ động - Bộ 5 Biểu đồ Hoạt động (Activity Diagrams)](#3-dòng-chảy-nghiệp-vụ-động---bộ-5-biểu-đồ-hoạt-động-activity-diagrams-03-phút)
  - [AD-01: Đặt phòng trực tuyến & Giữ phòng 15 phút](#ad-01-đặt-phòng-trực-tuyến--giữ-phòng-15-phút)
  - [AD-02: Check-in & Gán phòng vật lý động](#ad-02-check-in--gán-phòng-vật-lý-động)
  - [AD-03: Sử dụng dịch vụ & Ghi nợ vào Folio](#ad-03-sử-dụng-dịch-vụ--ghi-nợ-vào-folio)
  - [AD-04: Trả phòng, kiểm kê & Quyết toán Folio](#ad-04-trả-phòng-kiểm-kê--quyết-toán-folio)
  - [AD-05: Vận hành buồng phòng & Xử lý bảo trì thiết bị](#ad-05-vận-hành-buồng-phòng--xử-lý-bảo-trì-thiết-bị)
- [4. Mô hình cấu trúc tĩnh - Biểu đồ Lớp Lĩnh vực (Domain Class Diagram)](#4-mô-hình-cấu-trúc-tĩnh---biểu-đồ-lớp-lĩnh-vực-domain-class-diagram-02-phút)
- [5. Thiết kế hành vi động chi tiết - Bộ 6 Biểu đồ Tuần tự BCE (Sequence Diagrams)](#5-thiết-kế-hành-vi-động-chi-tiết---bộ-6-biểu-đồ-tuần-tự-bce-sequence-diagrams-06-phút)
  - [SD-01: Đặt phòng trực tuyến & Khóa giữ phòng 15 phút (Chi tiết từng message)](#sd-01-đặt-phòng-trực-tuyến--khóa-giữ-phòng-15-phút)
  - [SD-02: Check-in tiền sảnh & Gán phòng vật lý động](#sd-02-check-in-tiền-sảnh--gán-phòng-vật-lý-động)
  - [SD-03: Ghi nhận tiêu dùng dịch vụ phát sinh vào Folio](#sd-03-ghi-nhận-tiêu-dùng-dịch-vụ-phát-sinh-vào-folio)
  - [SD-04: Check-out, Quyết toán Folio VAT & Xuất hóa đơn GTGT 5 sao](#sd-04-check-out-quyết-toán-folio-vat--xuất-hóa-đơn-gtgt-5-sao)
  - [SD-05: Cập nhật tiến độ vệ sinh buồng phòng (Mobile Web PWA)](#sd-05-cập-nhật-tiến-độ-vệ-sinh-buồng-phòng-mobile-web-pwa)
  - [SD-06: Hủy phòng trực tuyến & Hoàn tiền cọc bậc thang](#sd-06-hủy-phòng-trực-tuyến--hoàn-tiền-cọc-bậc-thang)
- [6. Kiến trúc vật lý - Biểu đồ Triển khai (Deployment Diagram 3-Tier)](#6-kiến-trúc-vật-lý---biểu-đồ-triển-khai-deployment-diagram-3-tier-01-phút)
- [7. Thiết kế CSDL quan hệ 3NF & UML Database Design](#7-thiết-kế-csdl-quan-hệ-3nf--uml-database-design-01-phút)
- [8. Cẩm nang 15 câu hỏi vấn đáp phản biện "sống còn" (Q&A Defense Guide)](#8-cẩm-nang-15-câu-hỏi-vấn-đáp-phản-biện-sống-còn-qa-defense-guide)
- [9. Lời kết & Bàn giao đồ án](#9-lời-kết--bàn-giao-đồ-án)

---

## 1. LỜI MỞ ĐẦU & THIẾT LẬP BỐI CẢNH BÀI TOÁN (02 PHÚT)
- ⏱️ **Thời gian**: 00:00 - 02:00
- 👉 **Hành động**: Đứng tư thế chuẩn mực, mỉm cười, hướng mắt về Hội đồng, bật Slide 1 (Bìa đồ án) và chuyển sang Slide 2 (Bối cảnh bài toán).

🎙️ **[LỜI THOẠI MẪU TỪNG CÂU]**:
> *"Kính thưa Quý Thầy/Cô trong Hội đồng chấm bảo vệ đồ án và toàn thể các bạn sinh viên,*
>
> *Em tên là [Họ và Tên], đại diện cho nhóm nghiên cứu xin phép được báo cáo đồ án học phần Phân tích & Thiết kế Hệ thống Hướng đối tượng với đề tài: **'Phân tích & Thiết kế Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo Resort'**.*
>
> *Thưa Thầy/Cô, Sài Gòn - Côn Đảo là khu nghỉ dưỡng 4-5 sao cao cấp trực thuộc hệ thống Saigontourist Group, tọa lạc tại vị trí biệt lập ngoài hải đảo. Qua quá trình khảo sát nghiệp vụ thực tế, nhóm nhận thấy quản lý khách sạn biển đảo có 3 thách thức mang tính sống còn mà các hệ thống phần mềm thương mại phổ thông chưa giải quyết triệt để:*
>
> 1. ***Bài toán Tranh chấp tài nguyên cùng thời điểm (Race Condition & Overbooking)**: Do tính chất chuyến bay và tàu cao tốc ra Côn Đảo theo khung giờ cố định, du khách thường dồn dập đặt phòng vào cùng một thời điểm. Nếu không có cơ chế kiểm soát đồng thời, hệ thống sẽ bán trùng phòng (Overbooking).*
> 2. ***Sự tách biệt giữa Hạng phòng thương mại (Room Type) và Phòng vật lý thực tế (Physical Room)**: Khách đặt phòng B2C trên mạng chỉ chọn hạng phòng (như Superior Hướng Biển, Villa VIP). Việc gán số phòng cụ thể (như Villa 01, P.205) chỉ được Lễ tân thực hiện tại quầy khi check-in, phụ thuộc hoàn toàn vào tiến độ buồng phòng sạch thời gian thực.*
> 3. ***Quản lý Tài khoản chi tiêu Folio tập trung & Hoàn hủy bậc thang do thời tiết**: Mọi dịch vụ phát sinh từ minibar, giặt ủi đến tour ca-nô phải được hạch toán vào một sổ cái Folio thống nhất. Đồng thời, khi biển động bão gió cấm tàu, hệ thống phải tự động tính toán hoàn tiền cọc minh bạch theo số giờ trước check-in.*
>
> *Để giải quyết trọn vẹn bài toán trên, nhóm đã ứng dụng phương pháp luận **OOAD theo tiến trình chuẩn RUP**, áp dụng mẫu phân tích **3 Tầng BCE (Boundary - Control - Entity)**, chuẩn hóa cơ sở dữ liệu **3NF**, và xây dựng hệ thống biểu đồ UML 2.x hoàn chỉnh. Sau đây, em xin phép đi sâu vào từng biểu đồ thiết kế của đồ án."*

---

## 2. PHÂN TÍCH CHỨC NĂNG - HỆ THỐNG BIỂU ĐỒ USE CASE (03 PHÚT)
- ⏱️ **Thời gian**: 02:00 - 05:00
- 👉 **Hành động**: Trình chiếu file `diagrams/ooad_standard/00_So_Do_Use_Case_Tong_Quat.drawio`. Rê chuột chỉ vào ranh giới hệ thống, các Actor và 5 phân hệ.

### 2.1. Use Case tổng quát & 5 Tác nhân (Actors)
🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, trên màn hình là **Biểu đồ Use Case Tổng quát** của hệ thống:*
>
> 👉 *[Rê chuột vào các Actor bên ngoài ranh giới]*:
> *Hệ thống xác định 5 tác nhân (Actor) nằm ngoài ranh giới hệ thống đại diện cho các vai trò tương tác:*
> - **Khách hàng (Customer)**: Bao gồm Khách vãng lai và Khách có tài khoản thành viên VIP (hưởng chính sách tích lũy điểm Loyalty).*
> - **Lễ tân tiền sảnh (Receptionist)**: Tác nghiệp trực tiếp trên sơ đồ buồng phòng Gantt Rack, nhận khách, gán phòng, mở Folio, và quyết toán trả phòng.*
> - **Nhân viên Buồng phòng (Housekeeper)**: Nhận lệnh dọn phòng qua ứng dụng di động Web PWA, cập nhật tiến độ dọn và báo cáo sự cố bảo trì vật tư.*
> - **Quản lý khách sạn (Manager)**: Thiết lập cấu hình giá phòng linh hoạt, quản lý chương trình khuyến mãi Voucher, ban hành quy chế hoàn cọc và theo dõi báo cáo doanh thu RevPAR.*
> - **Quản trị hệ thống (Admin)**: Quản trị danh mục nền tảng (Hotel, RoomType, PhysicalRoom), phân quyền người dùng (RBAC), và quản lý nhật ký hệ thống.*

### 2.2. Phân rã 5 phân hệ chức năng
> 👉 *[Rê chuột lần lượt vào 5 gói phân hệ]*:
> 1. ***Phân hệ 1: Đặt phòng trực tuyến B2C**: Tìm kiếm phòng theo ngày, xem phòng 360°, chọn dịch vụ kèm theo, khóa phòng tạm 15 phút, và thanh toán trực tuyến qua VNPay QR.*
> 2. ***Phân hệ 2: Tác nghiệp Tiền sảnh (Front Desk)**: Xem sơ đồ phòng thời gian thực, Check-in khách đặt trước, tiếp nhận khách Walk-in tại quầy, đổi phòng (Move Room), báo vắng mặt (No-Show), và Check-out quyết toán Folio.*
> 3. ***Phân hệ 3: Vận hành Buồng phòng (Housekeeping)**: Quản lý danh sách phòng bẩn, nhận ca dọn, kiểm tra minibar, nghiệm thu buồng sạch và tạo phiếu bảo trì thiết bị.*
> 4. ***Phân hệ 4: Quản trị Doanh thu & Báo cáo**: Bảng điều khiển KPI (Doanh thu thực thu, Công suất phòng, Tỷ lệ hủy đơn), cài đặt giá theo mùa, chính sách hoàn tiền.*
> 5. ***Phân hệ 5: Quản trị Tài khoản & Danh mục Nền tảng**: Quản lý hồ sơ nhân viên, khóa tài khoản, cấu hình tham số khách sạn 3NF.*

### 2.3. Quy chuẩn học thuật về `<<include>>` và `<<extend>>`
> 👉 *[Chỉ chuột vào các đường nét đứt có gắn Badge `<<include>>` và `<<extend>>`]*:
> *"Điểm mấu chốt trong thiết kế Use Case của nhóm là sự chuẩn xác về mặt ngữ nghĩa UML 2.x:*
> - ***Quan hệ `<<include>>` (Bao hàm bắt buộc)**: Được sử dụng khi một Use Case cơ sở luôn luôn bắt buộc phải gọi Use Case thành phần để hoàn tất mục tiêu.
>   * *Ví dụ: Use Case 'Đặt phòng trực tuyến' bắt buộc phải `<<include>>` 'Kiểm tra phòng trống & Khóa giữ phòng 15 phút' và `<<include>>` 'Thanh toán trực tuyến'. Không thể có một đơn đặt phòng thành công mà bỏ qua việc trừ kho và thanh toán.*
>   * *Mũi tên nét đứt có nhãn `<<include>>` trỏ **THUẬN** từ Use Case cơ sở sang Use Case được bao hàm.*
> - ***Quan hệ `<<extend>>` (Mở rộng tùy chọn có điều kiện)**: Chỉ được kích hoạt khi thỏa mãn điều kiện bảo vệ tại Điểm mở rộng (Extension Point).
>   * *Ví dụ: Use Case 'Áp dụng Voucher giảm giá' mở rộng cho 'Đặt phòng trực tuyến' tại Extension Point `[Khách hàng có mã ưu đãi hợp lệ]`. Nếu không có voucher, Use Case Đặt phòng vẫn diễn ra bình thường.*
>   * *Use Case 'Hủy đặt phòng & Hoàn cọc' mở rộng cho 'Quản lý lịch sử đặt phòng' tại Extension Point `[Đơn ở trạng thái CONFIRMED và trước giờ Check-in]`.*
>   * *Mũi tên nét đứt có nhãn `<<extend>>` trỏ **NGƯỢC** từ Use Case mở rộng về Use Case cơ sở.*
> - *Nhóm tuân thủ tuyệt đối quy tắc: Không biến các thao tác vụn vặt (như click chuột, nhập ô tìm kiếm) thành Use Case; mỗi Use Case đại diện cho một chức năng nghiệp vụ hoàn chỉnh mang lại giá trị đo lường được cho tác nhân."*

---

## 3. DÒNG CHẢY NGHIỆP VỤ ĐỘNG - BỘ 5 BIỂU ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAMS) (03 PHÚT)
- ⏱️ **Thời gian**: 05:00 - 08:00
- 👉 **Hành động**: Trình chiếu file `bieu-do-hoat-dong-perfect.drawio` (các trang AD-01 đến AD-05).

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, để mô tả chi tiết dòng chảy logic điều khiển và phân định rõ trách nhiệm giữa các chủ thể, nhóm đã thiết kế bộ 05 Biểu đồ Hoạt động đa làn (Swimlanes).*

### AD-01: Đặt phòng trực tuyến & Giữ phòng 15 phút
> 👉 *[Chỉ vào trang AD-01]*:
> - *Biểu đồ gồm 3 làn bơi: **Khách hàng** | **Hệ thống Web Đặt phòng** | **Cổng thanh toán (VNPay / MoMo)**.*
> - *Khách hàng khởi đầu luồng bằng việc 'Chọn loại phòng và khoảng ngày lưu trú' $\rightarrow$ Hệ thống 'Kiểm tra tồn khả dụng cho từng đêm'.*
> - *Nút rẽ nhánh Decision `[Đủ phòng cho mọi đêm?]`:*
>   - *Nếu `[Sai]`: Hệ thống 'Thông báo hết phòng; đề nghị đổi lựa chọn' $\rightarrow$ Kết thúc.*
>   - *Nếu `[Đúng]`: Hệ thống thực thi hành động 'Kiểm tra lại và tạo RoomHoldLocks 15 phút' để chống Race Condition.*
> - *Nếu giữ chỗ thành công: Cổng thanh toán 'Tạo giao dịch và mã QR gắn với khóa giữ chỗ'. Hệ thống hiển thị đồng hồ đếm ngược 15:00.*
> - *Đặc biệt, hệ thống dùng thanh đồng bộ **Fork** phân tách 2 luồng:*
>   1. *Luồng 1: Bộ đếm thời gian Timer 'Chờ đến expiresAt hoặc tín hiệu hủy hẹn giờ'.*
>   2. *Luồng 2: Khách quét mã VietQR $\rightarrow$ Cổng thanh toán xác thực và gửi Webhook IPN về hệ thống.*
> - *Thanh **Join** hợp nhất luồng: Nếu Webhook hợp lệ trong 15 phút $\rightarrow$ 'Xác thực Webhook, tạo Booking & Hủy hẹn giờ' $\rightarrow$ Khách nhận mã Booking. Nếu quá hạn $\rightarrow$ 'Giải phóng phòng giữ chỗ & Hủy phiên thanh toán'.*

### AD-02: Check-in & Gán phòng vật lý động
> 👉 *[Chỉ vào trang AD-02]*:
> - *Gồm 3 làn: **Khách hàng** | **Lễ tân** | **Hệ thống PMS**.*
> - *Hệ thống hỗ trợ 2 kịch bản tại nút Decision `[Đã đặt trước?]`:*
>   - *Nếu `[Đúng]`: Lễ tân tra cứu mã PNR $\rightarrow$ kiểm tra tính hợp lệ của đơn.*
>   - *Nếu `[Sai]` (Khách Walk-in): Lễ tân chọn loại phòng, kiểm tra tồn phòng $\rightarrow$ Hệ thống 'Tạo hồ sơ khách và Booking tại quầy, không cần tài khoản'.*
> - *Khách xuất trình CCCD $\rightarrow$ Lễ tân quét giấy tờ $\rightarrow$ Hệ thống 'Lọc phòng khả dụng: CLEAN, VACANT & Không trùng'.*
> - *Nếu có phòng sạch: Lễ tân chọn phòng vật lý $\rightarrow$ Hệ thống 'Kiểm tra lại và gán phòng vào các BookingNights' $\rightarrow$ 'Lưu giờ nhận, chuyển phòng sang OCCUPIED' $\rightarrow$ Bàn giao chìa khóa cho khách.*
> - *Nếu chưa có phòng sạch: Hệ thống thông báo khách ngồi chờ buồng phòng dọn gấp.*

### AD-03: Sử dụng dịch vụ & Ghi nợ vào Folio
> 👉 *[Chỉ vào trang AD-03]*:
> - *Gồm 3 làn: **Khách hàng** | **Nhân viên Dịch vụ (Nhà hàng/Minibar)** | **Hệ thống PMS**.*
> - *Khách sử dụng dịch vụ $\rightarrow$ Tại nút Decision `[Thanh toán ngay?]`:*
>   - *Nếu khách trả tiền mặt: Nhân viên thu tiền $\rightarrow$ Hệ thống lưu Order và đánh dấu đã thanh toán.*
>   - *Nếu khách chọn ghi nợ phòng: Nhân viên 'Xác minh khách, Booking và phòng đang lưu trú'.*
> - *Hệ thống kiểm tra 2 điều kiện bảo vệ: `[Đúng khách, phòng OCCUPIED?]` và `[Folio còn mở để ghi nợ?]`.*
> - *Hệ thống thực thi giao dịch kép (Atomic Transaction): 'Lưu Order và Folio Details trong cùng giao dịch' $\rightarrow$ 'Cộng khoản chưa thanh toán vào số dư Folio' $\rightarrow$ Khách ký hóa đơn xác nhận.*

### AD-04: Trả phòng, kiểm kê & Quyết toán Folio
> 👉 *[Chỉ vào trang AD-04]*:
> - *Gồm 4 làn: **Khách hàng** | **Lễ tân** | **Buồng phòng** | **Hệ thống PMS**.*
> - *Lễ tân tiếp nhận yêu cầu trả phòng $\rightarrow$ gửi tín hiệu kiểm phòng sang buồng phòng.*
> - *Buồng phòng kiểm tra minibar, gửi báo cáo $\rightarrow$ Lễ tân nạp phụ thu vào Folio Details.*
> - *Hệ thống 'Tổng hợp tiền phòng, dịch vụ, hư hao và số đã thanh toán' $\rightarrow$ Trình bảng quyết toán.*
> - *Tại nút Decision kiểm tra số dư:*
>   - *Nếu `[Số dư dương]` (Khách nợ thêm): Lễ tân thu tiền bổ sung.*
>   - *Nếu `[Số dư âm]` (Cọc thừa): Lễ tân hoàn tiền mặt cho khách.*
> - *Điều kiện bảo vệ cốt lõi: **`[Công nợ bằng 0?]`** $\rightarrow$ Hệ thống mới cho phép 'Chốt Folio; lập hóa đơn VAT Saigontourist Group' $\rightarrow$ 'Đóng lưu trú, giải phóng phòng và chuyển sang DIRTY' $\rightarrow$ Đẩy phòng vào danh sách chờ dọn.*

### AD-05: Vận hành buồng phòng & Xử lý bảo trì thiết bị
> 👉 *[Chỉ vào trang AD-05]*:
> - *Gồm 4 làn: **Buồng phòng** | **Ứng dụng Di động PWA** | **Hệ thống Server PMS** | **Tổ Kỹ thuật / Lễ tân**.*
> - *Nhân viên buồng phòng mở danh sách phòng 'DIRTY' $\rightarrow$ chọn phòng $\rightarrow$ gửi yêu cầu đổi sang 'CLEANING'.*
> - *Trong quá trình dọn, nếu phát hiện sự cố (vỡ gương, hỏng máy lạnh):*
>   - *Nhân viên chụp ảnh lỗi $\rightarrow$ Ứng dụng gửi báo cáo $\rightarrow$ Server tạo `MaintenanceTicket` và chuyển phòng sang 'MAINTENANCE' (Khóa bảo trì).*
>   - *Tổ kỹ thuật nhận phiếu, sửa chữa $\rightarrow$ hoàn tất sửa chuyển về 'DIRTY' để dọn lại.*
> - *Nếu dọn đạt chuẩn sạch: Nhân viên gửi xác nhận $\rightarrow$ Server lưu trạng thái 'CLEAN' và **phát sự kiện WebSocket** $\rightarrow$ Sơ đồ buồng phòng tại quầy lễ tân lập tức chuyển sang màu xanh, sẵn sàng đón khách mới.*

---

## 4. MÔ HÌNH CẤU TRÚC TĨNH - BIỂU ĐỒ LỚP LĨNH VỰC DOMAIN CLASS DIAGRAM (02 PHÚT)
- ⏱️ **Thời gian**: 08:00 - 10:00
- 👉 **Hành động**: Trình chiếu file `00_Bieu_Do_Lop_Linh_Vuc_Domain_Class.drawio`.

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, đây là **Biểu đồ Lớp Lĩnh vực (Domain Class Diagram)** - mô hình tĩnh định hình toàn bộ thực thể bài toán theo nguyên lý **Information Expert** của mẫu GRASP.*
>
> 👉 *[Chỉ vào cấu trúc 3 ngăn]*:
> *Mỗi lớp được biểu diễn chuẩn mực gồm 3 ngăn: Tên lớp, Thuộc tính và Phương thức nghiệp vụ thuần túy:*
> - *Ví dụ, lớp `BookingMaster` chứa các phương thức: `tinhTongTien()`, `kiemTraHuyHopLe()`, `tinhTienPhatHuy()`, `dongHoSoCheckOut()`.*
> - *Lớp `RoomInventory` chứa: `kiemTraConPhong(roomTypeId, dates)`, `khoaGiuCho(roomTypeId, ttl)`.*
> - *Lớp `ServiceFolio` chứa: `ghiNoDichVu(itemId, amount)`, `tinhSoDuCongNo()`, `tatToanFolio()`.*
> - *Nhóm không đưa mã nguồn kỹ thuật như kết nối SQL hay setter/getter vụn vặt vào biểu đồ.*
>
> 👉 *[Chỉ vào 4 mối quan hệ sống còn và bản số Multiplicity]*:
> 1. ***Quan hệ Hợp thành (Composition - Kim cương đen đặc)** giữa `BookingMaster` và `BookingNight`: Một đơn đặt phòng gồm nhiều đêm lưu trú cụ thể. Đêm lưu trú không thể tồn tại độc lập nếu đơn đặt phòng bị hủy hoặc xóa. Tương tự, quan hệ giữa `ServiceFolio` và `FolioItem` là Composition.*
> 2. ***Quan hệ Thu nạp (Aggregation - Kim cương trắng rỗng)** giữa `Hotel` và `RoomType`, giữa `RoomType` và `PhysicalRoom`: Khách sạn có nhiều loại phòng, loại phòng quản lý các phòng vật lý thực tế. Khi một phòng vật lý bị khóa sửa chữa, loại phòng và khách sạn vẫn tồn tại độc lập.*
> 3. ***Quan hệ Kế thừa (Generalization - Tam giác trắng rỗng)**: Lớp cha `Account` (chứa username, password_hash, role, status) được chuyên biệt hóa thành `CustomerAccount` (bổ sung điểm Loyalty, hạng thẻ Vàng/Bạc) và `StaffAccount` (bổ sung mã nhân viên, ca trực).*
> 4. ***Bản số (Multiplicity)**: Được xác định chính xác ở hai đầu quan hệ: Một khách hàng có `0..*` đơn phòng, mỗi đơn phòng thuộc về đúng `1` khách hàng (`1..1`); một đơn phòng có `1..*` đêm lưu trú; một phòng vật lý thuộc đúng `1` loại phòng (`1..1`)."*

---

## 5. THIẾT KẾ HÀNH VI ĐỘNG CHI TIẾT - BỘ 6 BIỂU ĐỒ TUẦN TỰ SEQUENCE BCE (06 PHÚT)
- ⏱️ **Thời gian**: 10:00 - 16:00
- 👉 **Hành động**: Mở trình duyệt `00_Viewer_Toan_Bo_Sequence.html`, lần lượt chuyển qua từng tab SD-01 đến SD-06.

🎙️ **[LỜI THOẠI MẪU - TRIẾT LÝ BCE]**:
> *"Kính thưa Thầy/Cô, đây là phần trọng tâm nhất của đồ án. Toàn bộ 06 biểu đồ tuần tự được thiết kế tuân thủ nghiêm ngặt mô hình **BCE Pattern (Boundary - Control - Entity)** với quy tắc vàng: **CẤM NHẢY CÓC**. Boundary không được gọi trực tiếp vào Entity, và Entity không được gửi dữ liệu thẳng về Boundary mà mọi luồng trao đổi đều phải do tầng Control điều phối. Tất cả lời gọi đồng bộ (Sync Call mũi tên đen đặc) đều có vạch kích hoạt (Activation Bar) đối xứng với mũi tên trả về (Return Message nét đứt).*

---

### SD-01: Đặt phòng trực tuyến & Khóa giữ phòng 15 phút
👉 **Visual Cue**: Mở tab SD-01. Rê chuột theo từng bước từ Message 1 đến 17.

🎙️ **[LỜI THOẠI MẪU CHI TIẾT TỪNG THÔNG ĐIỆP]**:
> - ***Bước 1 (Msg 1 & 2)**: Khách hàng chọn loại phòng và ngày trên `:SearchBookingUI` $\rightarrow$ Giao diện gửi thông điệp đồng bộ `yeuCauGiuChoTamThoi(roomTypeId, checkIn, checkOut, quantity)` sang tầng điều khiển `:BookingService`.*
> - ***Bước 2 (Msg 3 & 3.1)**: `:BookingService` gọi sang `:RoomInventory` thực thi hàm `checkAvailability(roomTypeId, dates)`. Thuật toán kiểm tra: `Khả dụng = Tổng phòng - Đã bán - Khóa đang hoạt động`. Trả về: Còn phòng khả dụng.*
> - ***Bước 3 (Msg 4 & 4.1)**: Thay vì tạo ngay đơn hàng, `:BookingService` gọi `:RoomInventory` thực thi `createHoldLock(roomTypeId, expiresAt = now + 15m)`. Hệ thống sinh mã `lockId` với thời hạn chính xác 15 phút.*
> - ***Bước 4 (Msg 5 & 6)**: `:BookingService` trả `lockId` về `:SearchBookingUI`. Giao diện kích hoạt **đồng hồ đếm ngược 15:00** và mở màn hình thanh toán.*
> - ***Bước 5 (Msg 8, 9, 9.1)**: `:BookingService` gọi sang cổng `:VNPayGateway` hàm `createOrder(orderId, amount, callbackUrl, ipnUrl)`. Cổng thanh toán trả về URL và chuỗi dữ liệu VietQR.*
> - ***Bước 6 (Msg 10, 11, 11.1, 11.2)**: Giao diện hiển thị mã VietQR $\rightarrow$ Khách dùng App Ngân hàng quét mã và xác thực thanh toán thành công.*
> - ***Bước 7 - Khung ALT [Giao dịch thành công, vnp_ResponseCode == '00']**:*
>   * *Msg 12 & 12.1: Cổng VNPay bắn Webhook IPN sang `:VNPayGateway` $\rightarrow$ gọi `:PaymentTransaction` lưu bản ghi thanh toán với trạng thái `'SUCCESS'`.*
>   * *Msg 13 & 13.1: `:BookingService` gọi thực thể `:Booking` tạo bản ghi chính thức ở trạng thái `'CONFIRMED'`, sinh mã PNR.*
>   * *Msg 13.3 & 13.4: Tạo các đêm lưu trú chi tiết `:BookingNights`.*
>   * *Msg 13.5: Gọi `:RoomInventory` thực hiện `markLockAsSold(lockId)` - chuyển khóa tạm thời thành ĐÃ BÁN vĩnh viễn.*
>   * *Msg 14: Phản hồi HTTP 200 OK cho VNPay để xác nhận đã nhận IPN.*
>   * *Msg 15, 15.1, 15.3: Client định kỳ Polling hoặc nhận sự kiện SSE, cập nhật màn hình sang trạng thái 'PAID' và hiển thị Voucher xác nhận đặt phòng.*
> - ***Bước 8 - Khung ALT [else: Thanh toán thất bại hoặc khách hủy]**:*
>   * *Msg 16, 16.1: Ghi nhận giao dịch `'FAILED'`.*
>   * *Msg 16.3 & 16.4: Gọi `releaseHoldLock(lockId)` và `markLockAsExpired(lockId)` $\rightarrow$ Hoàn trả tồn kho phòng ngay tức khắc để mở lại cho khách khác.*
>   * *Msg 17 & 17.3: Màn hình khách báo lỗi giao dịch thất bại và phòng giữ chỗ đã được giải phóng."*

---

### SD-02: Check-in tiền sảnh & Gán phòng vật lý động
👉 **Visual Cue**: Mở tab SD-02.

🎙️ **[LỜI THOẠI MẪU CHI TIẾT TỪNG THÔNG ĐIỆP]**:
> - ***Msg 2 & 3**: Lễ tân nhập mã PNR trên `:FrontDeskGanttUI` $\rightarrow$ gọi `:CheckInController` hàm `getBookingDetails(pnrCode)` lấy thông tin hạng phòng, số đêm và tiền cọc.*
> - ***Msg 4, 5, 6**: Lễ tân quét thẻ CCCD khách $\rightarrow$ `:CheckInController` gọi `:GuestProfile` thực thi `saveIdentityProfile(guestData)` để lưu thông tin lưu trú theo quy định công an.*
> - ***Msg 7, 7.1, 7.2**: `:CheckInController` gọi `:PhysicalRoom` hàm `checkCleanRooms(roomTypeId, status='CLEAN')` để lọc các phòng vật lý thực tế thỏa mãn 2 điều kiện: Đúng hạng phòng khách đặt và phòng đã dọn sạch.*
> - ***Khung ALT [Có phòng CLEAN & Trống]**:*
>   * *Msg 7.3: Hệ thống đề xuất số phòng vật lý sẵn sàng (ví dụ: Villa 01).*
>   * *Msg 8 & 8.1: Đổi trạng thái đơn `:Booking` sang `'CHECKED_IN'`.*
>   * *Msg 9 & 9.1: Gọi hàm `assignPhysicalRoom(cleanRoomId)` gán số phòng cụ thể vào từng đêm trong `:BookingNight`.*
>   * *Msg 10 & 10.1: Đổi trạng thái phòng vật lý `:PhysicalRoom` sang `'OCCUPIED'` (Đang có khách).*
>   * *Msg 11, 12, 13: Kích hoạt thẻ từ mở phòng, in phiếu nhận phòng giao khách, và trên giao diện Gantt Rack đổi màu ô phòng sang Đỏ (OCCUPIED).*
> - ***Khung ALT [else: Chưa có phòng sạch]**:*
>   * *Msg 16: Hệ thống phát cảnh báo phòng đang 'DIRTY' hoặc bảo trì, đề xuất lễ tân yêu cầu buồng phòng dọn gấp hoặc nâng hạng phòng miễn phí cho khách."*

---

### SD-03: Ghi nhận tiêu dùng dịch vụ phát sinh vào Folio
👉 **Visual Cue**: Mở tab SD-03.

🎙️ **[LỜI THOẠI MẪU CHI TIẾT TỪNG THÔNG ĐIỆP]**:
> - ***Msg 2, 3, 3.1**: Nhân viên nhập số phòng trên `:ServicePostingUI` $\rightarrow$ gọi `:FolioBillingService` hàm `findActiveBooking(roomNumber, currentDate)`. Hệ thống kiểm tra xem phòng đó có đúng đang lưu trú (`CHECKED_IN`) hay không.*
> - ***Khung ALT [Phòng đang có khách lưu trú hợp lệ]**:*
>   * *Msg 3.2: Xác nhận phòng hợp lệ và hiển thị danh mục menu dịch vụ.*
>   * *Msg 4 & 5: Nhân viên chọn món (ví dụ: 2 lon bia Tiger, 1 gói hạt điều) và bấm Xác nhận.*
>   * *Msg 6 & 6.1: Gọi `:PriceCatalog` lấy đơn giá niêm yết và thuế suất VAT.*
>   * *Msg 7: `:FolioBillingService` tự tính tổng tiền: `Tổng = Số lượng × Đơn giá + VAT`.*
>   * *Msg 8 & 8.1: Gọi thực thể `:FolioInvoice` thực hiện `recordConsumption(bookingId, itemList, totalAmount)` để lưu chi tiết tiêu dùng.*
>   * *Msg 9 & 9.1: Gọi `postChargeToFolio(bookingId, totalAmount)` để ghi nợ lũy kế vào số dư tài khoản Folio của phòng.*
>   * *Msg 10 & 11: In phiếu ký nhận dịch vụ (Voucher) đưa khách ký tên và cập nhật công nợ.*
> - ***Khung ALT [else: Phòng trống hoặc đã Check-out]**:*
>   * *Msg 12: Hệ thống từ chối ghi nợ, báo lỗi phòng không có khách lưu trú để tránh thất thoát."*

---

### SD-04: Check-out, Quyết toán Folio VAT & Xuất hóa đơn GTGT 5 sao
👉 **Visual Cue**: Mở tab SD-04.

🎙️ **[LỜI THOẠI MẪU CHI TIẾT TỪNG THÔNG ĐIỆP]**:
> - ***Msg 1, 2, 3**: Lễ tân nhập kết quả kiểm phòng minibar (ví dụ: phát sinh 1 bia Heineken 35.000đ) $\rightarrow$ gọi `:CheckoutController` ghi nhận vào đơn hàng.*
> - ***Msg 4, 5, 6, 7**: `:CheckoutController` gọi `:FolioBillingService` tính toán công nợ theo công thức kế toán khách sạn:*
>   $$\text{Số dư quyết toán} = \text{Tiền phòng thực tế} + \text{Tổng dịch vụ phát sinh} - \text{Tiền cọc đã thu}$$
> - ***Msg 7.1 & 7.2**: Trả về bảng kê chi tiết quyết toán chi phí phòng.*
> - ***Msg 8, 9, 10, 11**: Lễ tân thu tiền (tiền mặt hoặc quẹt thẻ POS) $\rightarrow$ gọi `:PaymentTransaction` ghi nhận phiếu thu thành công.*
> - ***Msg 12 & 12.1**: Hệ thống tự động khởi tạo hóa đơn tài chính điện tử `:Invoice` với thuế suất VAT 8%, mã số thuế Saigontourist Group `0312456789-001`, sinh số hóa đơn chính thức.*
> - ***Msg 13 & 13.1**: Cập nhật trạng thái đơn `:Booking` sang `'CHECKED_OUT'` và đóng hồ sơ Folio.*
> - ***Msg 14 & 14.1**: Lập tức gửi thông điệp sang thực thể `:PhysicalRoom` cập nhật trạng thái phòng sang `'DIRTY'` (Phòng bẩn chờ dọn).*
> - ***Msg 15 & 16**: In hóa đơn VAT đưa khách và trên màn hình sơ đồ phòng Gantt tự động chuyển màu ô phòng sang Vàng/Đỏ (DIRTY) để kích hoạt đội buồng phòng."*

---

### SD-05: Cập nhật tiến độ vệ sinh buồng phòng (Mobile Web PWA)
👉 **Visual Cue**: Mở tab SD-05.

🎙️ **[LỜI THOẠI MẪU CHI TIẾT TỪNG THÔNG ĐIỆP]**:
> - ***Msg 3, 3.1, 3.2**: Nhân viên buồng phòng mở điện thoại $\rightarrow$ hệ thống truy vấn và hiển thị danh sách các phòng `'DIRTY'`.*
> - ***Msg 6, 6.1, 7, 7.1, 8**: Nhân viên bấm Nhận phòng $\rightarrow$ hệ thống cập nhật phòng sang `'CLEANING'` (Đang dọn) và tạo bản ghi nhật ký ca dọn `:CleaningLog` bấm giờ thực hiện.*
> - ***Khung ALT [Phòng đạt chuẩn vệ sinh & Đầy đủ tiện nghi]**:*
>   * *Msg 9, 10: Nhân viên hoàn tất dọn dẹp, kiểm tra checklist minibar và bấm Báo cáo hoàn thành.*
>   * *Msg 11 & 11.1: Hệ thống đổi trạng thái phòng sang `'CLEAN'`.*
>   * *Msg 12 & 12.1: Đóng ca dọn trong `:CleaningLog` với đánh giá `PASSED`.*
>   * *Msg 13 & 13.1: Hệ thống phát sự kiện **WebSocket Event `notifyRoomStatus(roomId, 'CLEAN')`** $\rightarrow$ Màn hình lễ tân tự động đổi ô phòng sang Xanh lục (CLEAN), sẵn sàng đón khách ngay.*
> - ***Khung ALT [else: Phát hiện hư hỏng vật tư - Chuyển BẢO TRÌ]**:*
>   * *Msg 16 & 17: Nhân viên phát hiện thiết bị hỏng (vỡ gương, hỏng máy lạnh), chụp ảnh và gửi báo cáo sự cố.*
>   * *Msg 18 & 18.1: Hệ thống đổi trạng thái phòng sang `'MAINTENANCE'` và khóa phòng trên hệ thống.*
>   * *Msg 19 & 19.1: Sinh phiếu sửa chữa `:MaintenanceTicket`.*
>   * *Msg 20: Đóng ca dọn dở dang.*
>   * *Msg 21 & 21.1: Bắn WebSocket Event cảnh báo sự cố đến tổ kỹ thuật và màn hình lễ tân lập tức đổi sang màu Xám (BẢO TRÌ)."*

---

### SD-06: Hủy phòng trực tuyến & Hoàn tiền cọc bậc thang
👉 **Visual Cue**: Mở tab SD-06.

🎙️ **[LỜI THOẠI MẪU CHI TIẾT TỪNG THÔNG ĐIỆP]**:
> - ***Msg 1, 2, 3**: Khách hàng vào lịch sử đơn trên `:BookingHistoryUI`, bấm 'Yêu cầu hủy phòng' $\rightarrow$ `:BookingCancellationService` lấy thông tin ngày đến, tiền cọc và trạng thái đơn.*
> - ***Khung ALT [Đơn ở trạng thái CONFIRMED & Chưa Check-in]**:*
>   * *Msg 5 & 6: Gọi thực thể chính sách `:RefundPolicy` với tham số `hoursRemaining` (tính đến 14:00 ngày check-in) để lấy tỷ lệ hoàn cọc: **100%** (trước 72h), **50%** (từ 24-72h), hoặc **0%** (dưới 24h).*
>   * *Msg 7 & 8: Tự động tính số tiền hoàn cọc và trả về bảng xem trước (Preview Modal).*
>   * *Msg 9, 10: Hiển thị điều khoản và biểu mẫu nhập lý do hủy phòng cho khách.*
>   * *Msg 11 & 12: Khách nhập lý do và bấm Xác nhận hủy.*
>   * *Msg 13 & 14: Cập nhật trạng thái đơn `:Booking` sang `'Canceled'`.*
>   * *Msg 15 & 16: Tạo bản ghi biên bản hủy `:CancellationRecord` lưu trữ lý do và tỷ lệ hoàn cọc.*
>   * *Msg 17 & 18: Nếu có hoàn tiền cọc (`refundAmount > 0`), hệ thống gọi `:PaymentTransaction` ghi nhận chứng từ hoàn tiền với **số tiền âm** (`-refundAmount`) phục vụ đối soát kế toán.*
>   * *Msg 19 & 20: Hành động then chốt: **`releaseBookedNights(bookingId)`** - Giải phóng toàn bộ các đêm lưu trú trong bảng `:BookingNight` để quỹ phòng trống lập tức mở lại trên website.*
>   * *Msg 21, 22, 23, 24: Thông báo hủy phòng thành công và đóng Modal.*
> - ***Khung ALT [else: Đơn đã Checked-in hoặc đã hủy trước đó]**:*
>   * *Msg 25, 26, 27: Từ chối hủy, hiển thị thông báo hướng dẫn khách liên hệ trực tiếp hotline Lễ tân."*

---

## 6. KIẾN TRÚC VẬT LÝ - BIỂU ĐỒ TRIỂN KHAI (DEPLOYMENT DIAGRAM 3-TIER) (01 PHÚT)
- ⏱️ **Thời gian**: 16:00 - 17:00
- 👉 **Hành động**: Mở file `07_Deployment_Diagram_Saigon_Condao.drawio`.

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, Biểu đồ Triển khai chứng minh kiến trúc hạ tầng phần cứng và môi trường thực thi của hệ thống theo mô hình **3-Tier Enterprise** chuẩn mực:*
>
> 👉 *[Chỉ vào Tầng 1: Client Tier]*:
> - *Gồm thiết bị di động của khách hàng B2C (`:KhachHangDevice`), thiết bị buồng phòng di động (`:HousekeepingMobile` chạy Web PWA), và máy trạm lễ tân (`:FrontDeskWorkstation` chạy Windows 11).*
> - *Máy trạm lễ tân kết nối trực tiếp với máy in hóa đơn nhiệt `:ThermalReceiptPrinter` qua cáp `USB 2.0 / Raw TCP Port 9100` để in bill tức thì mà không cần qua driver phức tạp.*
>
> 👉 *[Chỉ vào Tầng 2: Application Server Tier]*:
> - *Máy chủ trung tâm chạy Ubuntu Linux 22.04 LTS.*
> - *Tầng biên là **Nginx Web Server** chịu tải, thiết lập chứng chỉ `TLS 1.3 / HTTPS Port 443`, phân chia VLAN mạng nội bộ (`VLAN 20`). Nginx định tuyến các kết nối `WebSocket (WSS)` thời gian thực trực tiếp đến ứng dụng.*
> - *Môi trường **Python WSGI Container** chứa các Service nghiệp vụ: `BookingService`, `FolioSettlementService`, `CancellationService`, `HousekeepingService`.*
> - *Đặc biệt, hệ thống có tiến trình ngầm độc lập **Cron Daemon** (`cron_worker.py`) liên tục quét dọn các bản ghi giữ phòng quá hạn 15 phút mà không làm nghẽn luồng xử lý web chính.*
>
> 👉 *[Chỉ vào Tầng 3: Data & External Tier]*:
> - *Máy chủ CSDL nằm trong mạng bảo mật cách ly (`Dedicated DB Subnet`), giao tiếp nội bộ qua `ODBC / TCP Port 1433`.*
> - *Tích hợp 2 cổng dịch vụ điện toán đám mây ngoại vi: Cổng thanh toán tài chính **VNPay Gateway** qua REST API và Webhook IPN; Cổng thư điện tử giao dịch **Cloud Mail Gateway** qua `SMTP Port 587` có mã hóa TLS để tự động gửi vé xác nhận và hóa đơn GTGT."*

---

## 7. THIẾT KẾ CSDL QUAN HỆ 3NF & UML DATABASE DESIGN (01 PHÚT)
- ⏱️ **Thời gian**: 17:00 - 18:00
- 👉 **Hành động**: Mở file `08_UML_Database_Design_Diagram_Saigon_Condao.drawio`.

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Thầy/Cô, để lưu trữ dữ liệu an toàn và hiệu năng cao, nhóm đã thiết kế CSDL đạt **Chuẩn hóa bậc 3 (3NF)**:*
>
> 👉 *[Chỉ vào các cụm bảng 3NF]*:
> 1. ***Xóa bỏ hoàn toàn God-Table `New_Bookings`**: Thay vì lưu tất cả vào một bảng khổng lồ, hệ thống chuẩn hóa thành các cụm bảng chuyên biệt:*
>    - *Cụm danh mục (Dimensions): `dim_hotels` $\rightarrow$ `dim_room_types` $\rightarrow$ `physical_rooms` (Quản lý chính xác 14 phòng vật lý với trạng thái Clean/Dirty/Occupied).*
>    - *Cụm lưu trú: `booking_master` (quản lý thông tin chung, mã PNR, tiền cọc) liên kết 1-N với `booking_nights` (quản lý lịch trống chi tiết từng đêm).*
>    - *Cụm tài chính: `service_folios` (sổ cái công nợ phòng) liên kết 1-N với `folio_items` (chi tiết minibar/dịch vụ).*
>    - *Cụm đối soát: `payment_transactions` (lưu vết giao dịch VNPay/Tiền mặt) và `cancellation_records` (lưu vết biên bản hủy phòng).*
> 2. ***Đảm bảo toàn vẹn dữ liệu**: Ràng buộc Khóa chính (PK), Khóa ngoại (FK), Indexing trên các cột tra cứu (`booking_id`, `room_number`, `stay_date`), và quy tắc xóa an toàn `ON DELETE RESTRICT` để chống thất thoát dữ liệu lịch sử.*
> 3. ***Kiểm thử tự động**: Toàn bộ hệ sinh thái đã vượt qua **43/43 ca kiểm thử tự động (Unit, Smoke & E2E Tests)** đạt tỷ lệ thành công 100%."*

---

## 8. CẨM NANG 15 CÂU HỎI VẤN ĐÁP PHẢN BIỆN "SỐNG CÒN" (Q&A DEFENSE GUIDE)

### ❓ Câu 1: "Tại sao nhóm lại dùng mô hình BCE để vẽ Sequence Diagram mà không vẽ theo MVC hay vẽ trực tiếp Form gọi CSDL?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, trong quy trình phân tích thiết kế hướng đối tượng (OOAD) theo tiến trình Unified Process, **BCE (Boundary - Control - Entity)** là mẫu phân tích chuẩn mực (Analysis Pattern):*
> - *Vẽ trực tiếp Form gọi CSDL là vi phạm nghiêm trọng tính đóng gói và kiến trúc phân lớp, làm lộ chi tiết lưu trữ lên tầng hiển thị.*
> - *MVC là mẫu kiến trúc ở tầng cài đặt mã nguồn (Implementation Architecture), phụ thuộc vào framework. Trong khi đó, BCE mô hình hóa hành vi ở mức khái niệm bài toán: Boundary nhận tương tác, Control điều phối nghiệp vụ giao dịch độc lập công nghệ, và Entity quản lý dữ liệu nghiệp vụ.*
> - *Việc tuân thủ BCE đảm bảo nguyên lý Open-Closed (OCP): Khi thay đổi giao diện từ Web sang Mobile App hoặc thay đổi CSDL từ SQLite sang Oracle, toàn bộ tầng nghiệp vụ Control và Entity được tái sử dụng nguyên vẹn."*

---

### ❓ Câu 2: "Cơ chế khóa giữ phòng 15 phút xử lý thế nào nếu 2 người cùng bấm đặt phòng cho căn Villa duy nhất tại cùng một tích tắc (Race Condition)?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, nhóm giải quyết bằng cơ chế **Khóa bi quan có thời hạn (Pessimistic Hold with TTL)**:*
> - *Tại tầng Control (`RoomLockService`), thao tác kiểm tra số lượng và tạo bản ghi khóa được bọc trong một **Database Transaction nguyên tử** với mức cô lập cao (`SERIALIZABLE` hoặc mệnh đề atomic `UPDATE ... WHERE status = 'AVAILABLE'`).*
> - *Yêu cầu nào đến trước mili-giây sẽ thực thi thành công và tạo bản ghi trong bảng `room_locks` với `expires_at = now() + 15 phút`. Yêu cầu đến sau mili-giây sẽ nhận kết quả số phòng khả dụng bằng 0 và nhận thông báo phòng đang được người khác giữ chỗ.*
> - *Tiến trình ngầm `cron_worker.py` liên tục quét các khóa hết hạn để mở lại phòng tự động nếu khách đầu tiên không thanh toán."*

---

### ❓ Câu 3: "Tại sao phải tách riêng `BookingMaster` và `BookingNight` mà không lưu ngày đến và ngày đi trong một bảng duy nhất?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, việc tách `BookingNight` là quyết định thiết kế then chốt để đạt chuẩn 3NF và tối ưu hóa hiệu năng truy vấn:*
> 1. *Nếu chỉ lưu `arrival_date` và `departure_date`, khi tra cứu phòng trống cho một ngày bất kỳ, câu truy vấn SQL phải quét toàn bộ bảng với điều kiện khoảng ngày (`BETWEEN`), gây tắc nghẽn hiệu năng khi bảng có hàng chục ngàn đơn.*
> 2. *Tách ra `BookingNight` (mỗi dòng là 1 đêm), việc kiểm tra phòng trống quy về phép đếm cực nhanh: `COUNT(*) FROM booking_nights WHERE stay_date = ? AND room_type_id = ?` có index hỗ trợ.*
> 3. *Hơn nữa, nó hỗ trợ nghiệp vụ đổi phòng giữa chừng (Split Stay): Khách ở 4 đêm nhưng đêm 1-2 ở phòng 101, đêm 3-4 chuyển sang phòng 102 vẫn được quản lý chính xác mà không phá vỡ cấu trúc đơn hàng."*

---

### ❓ Câu 4: "Khái niệm Folio là gì và tại sao không gộp tiền minibar vào tổng tiền của đơn đặt phòng?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, trong nghiệp vụ khách sạn quốc tế (PMS), **Folio** là sổ cái công nợ lưu trú của phòng:*
> - *Tổng tiền đơn phòng (`total_amount`) ban đầu là giá trị hợp đồng dịch vụ lưu trú cố định được xác lập khi khách đặt trước.*
> - *Dịch vụ minibar, giặt ủi, ăn uống là các chi tiêu phát sinh biến động trong kỳ nghỉ với các mức thuế suất GTGT khác nhau (tiền phòng VAT khác tiền đồ uống có cồn).*
> - *Nếu cộng dồn trực tiếp vào đơn đặt phòng sẽ làm sai lệch giá trị hợp đồng ban đầu, gây rủi ro khi kiểm toán và không thể xuất hóa đơn tài chính bóc tách chi tiết.*
> - *Tách tài khoản `ServiceFolio` cho phép ghi nợ đa khoản theo thời gian thực (Posting Charges) và chỉ đóng sổ (Settlement) khi lễ tân hoàn tất thủ tục check-out."*

---

### ❓ Câu 5: "Trong biểu đồ Use Case, khi nào dùng `<<include>>` và khi nào dùng `<<extend>>`? Cho ví dụ trên đồ án."
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô:*
> - *`<<include>>` thể hiện quan hệ bao hàm bắt buộc: Use Case cơ sở không thể hoàn tất nếu thiếu Use Case thành phần. Mũi tên nét đứt trỏ **thuận** từ cơ sở sang thành phần. Ví dụ: 'Đặt phòng trực tuyến' bắt buộc `<<include>>` 'Kiểm tra phòng trống & Khóa giữ 15 phút'.*
> - *`<<extend>>` thể hiện sự mở rộng tùy chọn có điều kiện tại Điểm mở rộng (Extension Point). Mũi tên nét đứt trỏ **ngược** từ Use Case mở rộng về Use Case cơ sở. Ví dụ: 'Áp dụng Voucher' mở rộng cho 'Đặt phòng' tại Extension Point `[Khách hàng có mã ưu đãi]`."*

---

### ❓ Câu 6: "Làm thế nào hệ thống đảm bảo tính toàn vẹn khi khách hủy phòng trực tuyến (SD-06)?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, tại SD-06, việc hủy phòng được thực thi trong một Database Transaction thống nhất:*
> 1. *Cập nhật trạng thái đơn `:Booking` sang `'Canceled'`.*
> 2. *Tạo bản ghi `:CancellationRecord` lưu lý do và tỷ lệ phạt cọc.*
> 3. *Ghi chứng từ hoàn tiền âm vào `:PaymentTransaction`.*
> 4. *Gọi lệnh `releaseBookedNights` xóa hoặc giải phóng các đêm lưu trú trong `:BookingNight` để quỹ phòng lập tức khả dụng trở lại.*
> *Nếu bất kỳ bước nào gặp sự cố, toàn bộ giao dịch được Rollback, đảm bảo không bao giờ xảy ra tình trạng đơn đã hủy mà phòng vẫn bị chiếm giữ."*

---

### ❓ Câu 7: "Tại sao trong biểu đồ Triển khai (Deployment), máy in nhiệt POS lại nối cáp USB trực tiếp vào máy trạm lễ tân mà không qua máy chủ mạng?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, đây là đặc thù tác nghiệp tiền sảnh khách sạn 5 sao:*
> - *Việc in hóa đơn thanh toán và phiếu nhận phòng đòi hỏi tốc độ in tức thì dưới 1 giây để khách không phải chờ đợi tại quầy.*
> - *Kết nối cáp USB 2.0 / Raw TCP nội bộ giúp máy trạm gửi lệnh in trực tiếp bằng tập lệnh ESC/POS xuống máy in nhiệt ngay cả khi đường truyền Internet bên ngoài bị chập chờn, đảm bảo quầy lễ tân không bị tê liệt vận hành."*

---

### ❓ Câu 8: "Tại sao biểu đồ Triển khai lại tách riêng tiến trình Cron Daemon (`cron_worker.py`) ra khỏi Web Server chính?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, việc tách `cron_worker.py` thành tiến trình nền độc lập là để đảm bảo nguyên lý **Non-blocking I/O**:*
> - *Tiến trình Web Server Nginx và Python WSGI cần dành toàn bộ tài nguyên CPU và RAM để phục vụ các yêu cầu HTTP/HTTPS của người dùng với độ trễ thấp nhất.*
> - *Nếu tích hợp tác vụ quét kiểm tra phòng hết hạn vào luồng Web chính, khi có hàng ngàn bản ghi cần xử lý sẽ gây hiện tượng đứng trang (Page Freeze) cho người dùng khác.*
> - *Tách thành Daemon riêng giúp tác vụ dọn phòng chạy ngầm theo chu kỳ mà không ảnh hưởng đến trải nghiệm người dùng."*

---

### ❓ Câu 9: "Quy trình chuyển trạng thái của một phòng vật lý (PhysicalRoom) diễn ra như thế nào trong toàn bộ vòng đời?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, phòng vật lý trải qua vòng đời khép kín 5 trạng thái:*
> 1. `CLEAN` (Sạch sẽ, sẵn sàng đón khách) $\rightarrow$ Lễ tân Check-in $\rightarrow$ chuyển sang `OCCUPIED` (Đang có khách lưu trú).
> 2. `OCCUPIED` $\rightarrow$ Khách làm thủ tục Check-out $\rightarrow$ tự động chuyển sang `DIRTY` (Phòng bẩn chờ dọn).
> 3. `DIRTY` $\rightarrow$ Nhân viên buồng phòng nhận phòng $\rightarrow$ chuyển sang `CLEANING` (Đang dọn dẹp).
> 4. `CLEANING` $\rightarrow$ Dọn xong và đạt tiêu chuẩn $\rightarrow$ chuyển sang `CLEAN` (hoặc `INSPECTED` sau khi Tổ trưởng nghiệm thu).
> 5. *Trường hợp đặc biệt: Nếu phát hiện sự cố hỏng hóc thiết bị, phòng chuyển từ `CLEANING` sang `MAINTENANCE` (Khóa bảo trì) và chỉ trở về `DIRTY` sau khi tổ kỹ thuật sửa xong."*

---

### ❓ Câu 10: "Hệ thống làm thế nào để đảm bảo tính Idempotency (bất biến) khi nhận Webhook IPN từ cổng thanh toán VNPay?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, VNPay có thể gửi lại Webhook nhiều lần (Retry Mechanism) nếu mạng chập chờn:*
> - *Tại tầng Control, hệ thống kiểm tra trường `bank_tx_no` (Mã giao dịch ngân hàng) và trạng thái đơn hàng.*
> - *Nếu đơn đã ở trạng thái `'CONFIRMED'`, hệ thống bỏ qua việc tạo đơn lần hai và ngay lập tức phản hồi `HTTP 200 OK` kèm `RspCode='00'` về cho VNPay.*
> - *Điều này ngăn chặn triệt để lỗi cộng tiền trùng hoặc sinh nhiều đơn hàng cho cùng một giao dịch thanh toán."*

---

### ❓ Câu 11: "Sự khác biệt giữa Biểu đồ Hoạt động (Activity Diagram) và Biểu đồ Tuần tự (Sequence Diagram) trong thiết kế hệ thống là gì?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô:*
> - ***Biểu đồ Hoạt động (Activity Diagram)**: Tập trung vào **dòng điều khiển công việc (Control Flow)**, mô tả các bước nghiệp vụ diễn ra theo trình tự nào, rẽ nhánh ra sao qua các làn bơi chủ thể, mang tính quy trình logic tổng quát.*
> - ***Biểu đồ Tuần tự (Sequence Diagram)**: Tập trung vào **sự tương tác thông điệp giữa các đối tượng cụ thể (Object Interaction)** theo trục thời gian, thể hiện rõ hàm nào được gọi, tham số là gì, kiểu trả về là gì theo đúng cấu trúc mã nguồn hướng đối tượng."*

---

### 12. Câu 12: "Tại sao nhóm chọn kiến trúc phân đoạn mạng VLAN 20 trong biểu đồ Triển khai?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, đây là quy chuẩn bảo mật thông tin khách sạn:*
> - *Mạng Wi-Fi của du khách là mạng công cộng (Public Internet) có nguy cơ bị nghe lén hoặc tấn công dò quét.*
> - *Việc cô lập thiết bị Lễ tân và Buồng phòng vào phân đoạn mạng nội bộ `VLAN 20` có tường lửa bảo vệ giúp ngăn chặn du khách truy cập trái phép vào các API quản trị và máy chủ cơ sở dữ liệu."*

---

### ❓ Câu 13: "Làm thế nào để hệ thống xử lý trường hợp khách đặt phòng nhưng không đến (No-Show)?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô:*
> - *Theo chính sách khách sạn, sau 23:59 ngày check-in nếu khách không đến nhận phòng, chức năng Quản lý No-Show trên giao diện Lễ tân cho phép chuyển trạng thái đơn sang `'NO_SHOW'`.*
> - *Hệ thống đóng hồ sơ đơn, thu 100% tiền cọc lưu trú đêm đầu theo điều khoản hợp đồng, và giải phóng các đêm phòng còn lại về trạng thái trống để khách khác có thể đặt phòng cho các ngày tiếp theo."*

---

### ❓ Câu 14: "Tại sao trong Biểu đồ Lớp Lĩnh vực không đưa thuộc tính khóa ngoại (Foreign Key) vào lớp như trong CSDL?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, đây là lỗi rất phổ biến mà nhóm đã tránh được:*
> - *Trong mô hình hóa hướng đối tượng thuần túy (Domain Model), các đối tượng liên kết với nhau thông qua **quan hệ liên kết (Associations, References)** chứ không dùng thuộc tính khóa ngoại dạng cột ID như CSDL quan hệ.*
> - *Khóa ngoại là khái niệm của tầng lưu trữ CSDL vật lý (Physical Schema), không phải là thuộc tính tự nhiên của thực thể nghiệp vụ."*

---

### ❓ Câu 15: "Đồ án này đã được kiểm thử như thế nào để chứng minh các biểu đồ thiết kế đã chạy đúng trong thực tế?"
> 🎙️ **Trả lời**:  
> *"Dạ thưa Thầy/Cô, toàn bộ thiết kế kiến trúc đã được hiện thực hóa và kiểm thử tự động với bộ test suite gồm **43 ca kiểm thử (100% Passing)**:*
> - *Kiểm thử mô hình miền (Domain Models): 5/5 tests xác thực tính toàn vẹn của các thực thể và quan hệ.*
> - *Kiểm thử dịch vụ (Services Smoke Tests): 7/7 tests kiểm tra độc lập các luồng nghiệp vụ tính tiền, khóa phòng, hoàn cọc.*
> - *Kiểm thử API Endpoints: 5/5 tests kiểm tra tầng giao tiếp Boundary và Controller.*
> - *Kiểm thử giao diện Frontend Views: 6/6 tests xác thực toàn bộ 24 trang hiển thị.*
> - *Kiểm thử tích hợp vòng đời khép kín (E2E Lifecycle Tests): 4/4 tests mô phỏng từ Đặt phòng $\rightarrow$ Check-in $\rightarrow$ Ghi nợ Minibar $\rightarrow$ Quyết toán Check-out $\rightarrow$ Hủy hoàn tiền."*

---

## 9. LỜI KẾT & BÀN GIAO ĐỒ ÁN (01 PHÚT)
- ⏱️ **Thời gian**: 18:00 - 19:00
- 👉 **Hành động**: Chuyển sang slide Cảm ơn, hướng mắt về Hội đồng, cúi đầu chào trang trọng.

🎙️ **[LỜI THOẠI MẪU]**:
> *"Kính thưa Quý Thầy/Cô trong Hội đồng,*
>
> *Thông qua toàn bộ hồ sơ thiết kế từ **Biểu đồ Use Case**, **Biểu đồ Hoạt động Activity**, **Biểu đồ Lớp Lĩnh vực Domain Class**, chuỗi **06 Biểu đồ Tuần tự BCE**, cùng **Biểu đồ Triển khai 3-Tier** và **Mô hình CSDL 3NF**, nhóm chúng em đã giải quyết trọn vẹn và khoa học bài toán quản lý nghỉ dưỡng của Khách sạn Sài Gòn - Côn Đảo Resort.*
>
> *Đồ án không chỉ dừng lại ở bản vẽ lý thuyết mà đã được kiểm chứng bằng 43 ca kiểm thử tự động đạt độ chính xác 100%.*
>
> *Em xin đại diện nhóm bày tỏ lòng biết ơn sâu sắc đến Quý Thầy/Cô đã tận tình hướng dẫn và trang bị cho chúng em những nền tảng kiến trúc phần mềm quý báu trong suốt học phần.*
>
> *Nhóm chúng em rất mong nhận được những nhận xét, góp ý và câu hỏi phản biện từ Quý Thầy/Cô để hoàn thiện đề tài xuất sắc hơn nữa.*
>
> *Em xin trân trọng cảm ơn Thầy/Cô và xin mời Hội đồng bắt đầu phần chất vấn ạ!"*
