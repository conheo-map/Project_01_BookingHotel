# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN OOAD THEO TỪNG SLIDE
## DỰ ÁN: HỆ THỐNG QUẢN LÝ VÀ ĐẶT PHÒNG KHÁCH SẠN SÀI GÒN - CÔN ĐẢO RESORT
> **Tài liệu trình chiếu chính thức**: Tệp slide `slide_N7.pdf` (gồm đúng 52 slide hoàn chỉnh)  
> **Tệp bản vẽ thiết kế gốc**: `Tong_hop_bieu_do_(1).drawio`  
> **Quy chuẩn chuyên môn**: Chuẩn RUP / UML 2.5 & Lead Enterprise Software Architect  
> **Phương pháp sử dụng**: Cầm clicker chuyển từng slide, đọc đúng lời thoại, rê chuột đúng điểm chỉ dẫn, và nắm chắc kiến thức phòng thủ để **thầy cô không thể hỏi vặn ngược lại**.

---

# MỤC LỤC 52 SLIDE TRÌNH CHIẾU

- [PHẦN I: GIỚI THIỆU & PHÂN TÍCH YÊU CẦU (SLIDE 01 - 16)](#phần-i-giới-thiệu--phân-tích-yêu-cầu-slide-01---16)
- [PHẦN II: THUYẾT TRÌNH CHI TIẾT TỪNG BIỂU ĐỒ HỆ THỐNG (SLIDE 17 - 45)](#phần-ii-thuyết-trình-chi-tiết-từng-biểu-đồ-hệ-thống-slide-17---45)
  - [Slide 17: Biểu đồ Use Case Tổng Quát](#slide-17-biểu-đồ-use-case-tổng-quát)
  - [Slide 18: Biểu đồ Phân Rã Use Case - Cổng Đặt Phòng Trực Tuyến B2C](#slide-18-biểu-đồ-use-case-phân-rã---cổng-đặt-phòng-trực-tuyến-b2c)
  - [Slide 19: Biểu đồ Phân Rã Use Case - Quản Lý Tài Khoản & Phân Quyền](#slide-19-biểu-đồ-use-case-phân-rã---quản-lý-tài-khoản--phân-quyền)
  - [Slide 20: Biểu đồ Phân Rã Use Case - Tác Nghiệp Tiền Sảnh & Lễ Tân](#slide-20-biểu-đồ-use-case-phân-rã---tác-nghiệp-quầy-tiền-sảnh--lễ-tân)
  - [Slide 21: Biểu đồ Phân Rã Use Case - Vận Hành Buồng Phòng](#slide-21-biểu-đồ-use-case-phân-rã---vận-hành-buồng-phòng)
  - [Slide 22: Biểu đồ Phân Rã Use Case - Quản Trị Doanh Thu, Bảng Giá & Báo Cáo](#slide-22-biểu-đồ-use-case-phân-rã---quản-trị-doanh-thu-bảng-giá--báo-cáo)
  - [Slide 23: Biểu đồ Hoạt Động - Đặt Phòng Trực Tuyến & Giữ Phòng 15 Phút (AD-01)](#slide-23-biểu-đồ-hoạt-động-đặt-phòng-trực-tuyến)
  - [Slide 24: Biểu đồ Hoạt Động - Check-In & Gán Phòng Vật Lý Động (AD-02)](#slide-24-biểu-đồ-hoạt-động-check-in-và-gán-phòng)
  - [Slide 25: Biểu đồ Hoạt Động - Sử Dụng Dịch Vụ & Ghi Nợ Folio (AD-03)](#slide-25-biểu-đồ-hoạt-động-sử-dụng-dịch-vụ-và-ghi-chi-tiêu-vào-folio)
  - [Slide 26: Biểu đồ Hoạt Động - Check-Out & Quyết Toán Folio (AD-04)](#slide-26-biểu-đồ-hoạt-động-check-out-và-quyết-toán)
  - [Slide 27: Biểu đồ Hoạt Động - Dọn Buồng Phòng & Bảo Trì Thiết Bị (AD-05)](#slide-27-biểu-đồ-hoạt-động-dọn-buồng-phòng-và-xử-lý-bảo-trì)
  - [Slide 28: Biểu đồ Tuần Tự - Giới Thiệu Khái Quát Mô Hình Tuần Tự](#slide-28-biểu-đồ-tuần-tự--quy-trình-đặt-phòng-tổng-quan)
  - [Slide 29: Biểu đồ Tuần Tự - Đặt Phòng & Khóa Phòng Chống Trùng (SD-01 BCE)](#slide-29-biểu-đồ-tuần-tự-đặt-phòng-và-khóa-phòng-chống-trùng-sd-01)
  - [Slide 30: Biểu đồ Tuần Tự - Thủ Tục Nhận Phòng & Gán Phòng Vật Lý (SD-02 BCE)](#slide-30-biểu-đồ-tuần-tự-làm-thủ-tục-nhận-phòng-sd-02)
  - [Slide 31: Biểu đồ Tuần Tự - Ghi Nhận Tiêu Dùng Dịch Vụ Vào Folio (SD-03 BCE)](#slide-31-biểu-đồ-tuần-tự-ghi-nhận-tiêu-dùng-dịch-vụ-sd-03)
  - [Slide 32: Biểu đồ Tuần Tự - Trả Phòng & Quyết Toán Hóa Đơn VAT (SD-04 BCE)](#slide-32-biểu-đồ-tuần-tự-trả-phòng-và-quyết-toán-sd-04)
  - [Slide 33: Biểu đồ Tuần Tự - Vận Hành Dọn Dẹp Buồng Phòng (SD-05 BCE)](#slide-33-biểu-đồ-tuần-tự-vận-hành-dọn-dẹp-buồng-phòng-sd-05)
  - [Slide 34: Biểu đồ Tuần Tự - Hủy Đặt Phòng & Hoàn Tiền Cọc Bậc Thang (SD-06 BCE)](#slide-34-biểu-đồ-tuần-tự-hủy-đặt-phòng-và-hoàn-tiền-cọc-sd-06)
  - [Slide 35: Biểu đồ Lớp - Giới Thiệu Cấu Trúc Lớp & Quan Hệ](#slide-35-biểu-đồ-lớp--class-diagram-giới-thiệu)
  - [Slide 36: Biểu đồ Lớp - Bản Vẽ Chi Tiết Domain Class Diagram](#slide-36-biểu-đồ-lớp--class-diagram-chi-tiết)
  - [Slide 37: Biểu đồ Gói - Package Diagram 5 Tầng](#slide-37-biểu-đồ-gói--package-diagram)
  - [Slide 38: Biểu đồ Triển Khai - Deployment Diagram 3-Tier](#slide-38-biểu-đồ-triển-khai--deployment-diagram)
  - [Slide 39: Biểu đồ Thành Phần Tổng Quát](#slide-39-biểu-đồ-thành-phần-tổng-quát)
  - [Slide 40: Biểu đồ Thành Phần - Đặt Phòng & Giữ Phòng Trực Tuyến](#slide-40-biểu-đồ-thành-phần-đặt-phòng-và-giữ-phòng-trực-tuyến)
  - [Slide 41: Biểu đồ Thành Phần - Nhận Phòng & Gán Phòng Vật Lý](#slide-41-biểu-đồ-thành-phần-nhận-phòng-và-gán-phòng-vật-lý)
  - [Slide 42: Biểu đồ Thành Phần - Ghi Nhận Dịch Vụ Phát Sinh](#slide-42-biểu-đồ-thành-phần-ghi-nhận-dịch-vụ-phát-sinh)
  - [Slide 43: Biểu đồ Thành Phần - Trả Phòng & Quyết Toán](#slide-43-biểu-đồ-thành-phần-trả-phòng)
  - [Slide 44: Biểu đồ Thành Phần - Vệ Sinh Buồng Phòng](#slide-44-biểu-đồ-thành-phần-vệ-sinh-buồng-phòng)
  - [Slide 45: Thiết Kế Cơ Sở Dữ Liệu - 15 Bảng Chuẩn Hóa 3NF](#slide-45-thiết-kế-dữ-liệu-15-bảng-3nf)
- [PHẦN III: THIẾT KẾ GIAO DIỆN & KẾT LUẬN (SLIDE 46 - 52)](#phần-iii-thiết-kế-giao-diện--kết-luận-slide-46---52)

---

# PHẦN I: GIỚI THIỆU & PHÂN TÍCH YÊU CẦU (SLIDE 01 - 16)

### Slide 01: Bìa Đồ Án
- **Nội dung slide**: `NHÓM 7 - ĐỀ TÀI: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG QUẢN LÝ ĐẶT PHÒNG Ở SAIGON - CONDAO RESORT`
- 🎙️ **Lời thoại**: *"Kính thưa Quý Thầy/Cô trong Hội đồng và các bạn sinh viên, em xin đại diện Nhóm 7 báo cáo đồ án môn Phân tích & Thiết kế Hệ thống Hướng đối tượng với đề tài: **Phân tích và Thiết kế Hệ thống Quản lý Đặt phòng ở Saigon - Condao Resort**."*

### Slide 02: Mục Lục Báo Cáo
- **Nội dung slide**: 5 Phần: 1. Giới thiệu đề tài | 2. Khảo sát & phân tích hiện trạng | 3. Phân tích yêu cầu hệ thống | 4. Mô hình hóa hệ thống | 5. Thiết kế giao diện.
- 🎙️ **Lời thoại**: *"Nội dung báo cáo hôm nay gồm 5 phần chính, trong đó Nhóm tập trung sâu nhất vào Phần 4 - Mô hình hóa hệ thống với trọn bộ 28 biểu đồ thiết kế kiến trúc chuẩn mực."*

### Slide 03 - 05: Bối Cảnh & Bài Toán Quản Lý Đặt Phòng
- **Nội dung slide**: Thực trạng tiếp nhận qua nhiều kênh (Website, Hotline, Fanpage); Bối cảnh Resort thuộc Saigontourist thành lập 1996 tại 18-24 Tôn Đức Thắng, Côn Đảo; Thách thức quản lý nhiều loại phòng và phòng vật lý.
- 🎙️ **Lời thoại**: *"Saigon - Condao Resort là khu nghỉ dưỡng cao cấp trực thuộc Saigontourist Group. Nghiệp vụ đặt phòng tại đây gặp 3 thách thức lớn: Thứ nhất là nguy cơ bán trùng phòng (Overbooking) khi khách dồn dập đặt theo chuyến bay/tàu cao tốc ra đảo; Thứ hai là sự tách biệt giữa Hạng phòng kinh doanh và Phòng vật lý thực tế; Thứ ba là việc theo dõi chi tiêu Folio tập trung và hoàn tiền khi tàu bè bị cấm biển do bão gió."*

### Slide 06 - 10: Mục Tiêu, Phạm Vi & Đánh Giá Hiện Trạng
- **Nội dung slide**: Mục tiêu xây dựng hệ thống quản lý chuẩn hóa; Phạm vi nghiệp vụ B2C và nội bộ Resort; Đánh giá ưu/nhược điểm hiện trạng bán phòng thủ công.
- 🎙️ **Lời thoại**: *"Mục tiêu của đề tài là xây dựng một hệ thống hoàn chỉnh giúp tự động hóa quy trình đặt phòng trực tuyến, chống nghẽn giữ chỗ, liên thông thời gian thực giữa Lễ tân và Buồng phòng, khắc phục hoàn toàn nhược điểm ghi chép rời rạc hiện nay."*

### Slide 11 - 16: Phân Tích Yêu Cầu, Tác Nhân, FR, NFR, BR
- **Nội dung slide**: Quy trình nghiệp vụ đề xuất; 5 Tác nhân chính (Khách hàng, Lễ tân, Buồng phòng, Quản lý, Quản trị viên); Ma trận yêu cầu chức năng FR01-FR12; 25 yêu cầu phi chức năng NFR01-NFR25; 16 Quy tắc nghiệp vụ BR01-BR16 (như Check-in 14:00, Check-out 12:00, Giữ phòng 15 phút, Chính sách hoàn cọc).
- 🎙️ **Lời thoại**: *"Dựa trên khảo sát, nhóm đã đặc tả 12 nhóm yêu cầu chức năng, 25 yêu cầu phi chức năng về an ninh, hiệu năng cao, và 16 quy tắc nghiệp vụ khắt khe. Đây là cơ sở nền tảng để nhóm chuyển hóa thành các mô hình thiết kế hướng đối tượng ngay sau đây."*

---

# PHẦN II: THUYẾT TRÌNH CHI TIẾT TỪNG BIỂU ĐỒ HỆ THỐNG (SLIDE 17 - 45)

---

### Slide 17: Biểu đồ Use Case Tổng Quát
- **Tiêu đề Slide**: `BIỂU ĐỒ USE CASE TỔNG QUÁT`
- **Nội dung hiển thị**: Các tác nhân: Khách hàng, Lễ tân, Buồng phòng, Quản lý resort, Quản trị viên, Cổng thanh toán, Máy chủ Cron; Bản vẽ sơ đồ Use Case bao trọn 15 chức năng nghiệp vụ.

👉 **Visual Cue**: Rê chuột từ các Actor bên ngoài ranh giới vào khung System Boundary.

🎙️ **Lời thoại thuyết trình**:
> *"Kính thưa Thầy/Cô, trên **Slide 17** là **Biểu đồ Use Case Tổng quát** của toàn hệ thống:*
> - *Hệ thống xác định 5 tác nhân người dùng tương tác trực tiếp: Khách hàng, Nhân viên Lễ tân, Nhân viên Buồng phòng, Quản lý Resort và Quản trị viên.*
> - *Hai tác nhân hệ thống bên ngoài: Cổng thanh toán VNPay (xử lý trừ tiền và gửi Webhook) và Máy chủ Cron (tác nhân thời gian chạy ngầm để dọn dẹp phòng giữ quá hạn).*
> - *Ranh giới hệ thống bao trọn 15 Use Case nghiệp vụ chính, bảo đảm phân định trách nhiệm rõ ràng, không để tác nhân nằm lẫn trong ranh giới."*

🛡️ **Kiến thức phòng thủ chống Thầy vặn**:
- **Thầy vặn**: *"Tại sao Cổng thanh toán và Cron lại vẽ là Actor?"*
- **Đáp ngay**: *"Thưa Thầy, theo chuẩn UML 2.5, Actor là bất kỳ thực thể nào **nằm ngoài ranh giới hệ thống** tương tác trao đổi thông tin với hệ thống. VNPay là hệ thống thứ ba tương tác qua Webhook IPN; Cron là tác nhân ngoại vi kích hoạt tiến trình theo chu kỳ thời gian (Temporal Event). Do đó cả hai đều là Actor hợp lệ."*

---

### Slide 18: Biểu đồ Use Case Phân Rã - Cổng Đặt Phòng Trực Tuyến B2C
- **Tiêu đề Slide**: `BIỂU ĐỒ USE CASE PHÂN RÃ THEO PHÂN HỆ - 1. CỔNG ĐẶT PHÒNG TRỰC TUYẾN B2C`
- **Nội dung hiển thị**: Tìm kiếm phòng, Xem thông tin & giá, Đặt phòng trực tuyến, Thanh toán tiền cọc, Hủy đặt phòng & hoàn tiền.

👉 **Visual Cue**: Chỉ vào mũi tên `<<include>>` trỏ từ Đặt phòng sang Khóa phòng 15 phút, và `<<extend>>` từ Áp dụng Voucher.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 18**, nhóm phân rã chi tiết **Phân hệ Đặt phòng B2C**:*
> - *Use Case cốt lõi **'Đặt phòng trực tuyến'** bắt buộc **`<<include>>`** chức năng **'Khóa phòng chống trùng (Hold Lock 15 phút)'** và **'Xác thực cổng thanh toán'**. Luồng nghiệp vụ không thể hoàn tất nếu thiếu 2 bước này.*
> - *Use Case **'Áp dụng mã giảm giá (Voucher)'** liên kết dạng **`<<extend>>`** trỏ ngược về Đặt phòng, chỉ kích hoạt tại Extension Point khi khách hàng sở hữu mã hợp lệ.*
> - *Bên dưới là luồng **'Hủy đặt phòng & hoàn tiền'**, tích hợp tính toán hoàn cọc tự động theo số giờ trước check-in."*

🛡️ **Kiến thức phòng thủ chống Thầy vặn**:
- **Thầy vặn**: *"Tại sao hướng mũi tên `<<include>>` và `<<extend>>` lại ngược nhau?"*
- **Đáp ngay**: *"Thưa Thầy, `<<include>>` là quan hệ bắt buộc, Use Case cơ sở **gọi** Use Case thành phần nên mũi tên trỏ **thuận**. Ngược lại, `<<extend>>` là hành vi mở rộng tùy chọn, Use Case mở rộng **chèn thêm hành vi** vào Use Case cơ sở nên mũi tên trỏ **ngược** từ Use Case mở rộng về Use Case cơ sở theo đúng chuẩn UML 2.5."*

---

### Slide 19: Biểu đồ Use Case Phân Rã - Quản Lý Tài Khoản & Phân Quyền
- **Tiêu đề Slide**: `BIỂU ĐỒ USE CASE PHÂN RÃ THEO PHÂN HỆ - 2. QUẢN LÝ TÀI KHOẢN VÀ PHÂN QUYỀN`
- **Nội dung hiển thị**: Đăng ký, đăng nhập; Quản lý tài khoản; Quản lý vai trò; Phân quyền truy cập.

👉 **Visual Cue**: Chỉ vào quan hệ `<<extend>>` Khóa tài khoản sau 5 lần đăng nhập sai.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 19**, phân hệ **Quản lý Tài khoản & Phân quyền**:*
> - *Khách hàng thao tác trên Đăng ký hội viên mới (`<<include>>` Xác thực và Tạo hồ sơ tích điểm Loyalty).*
> - *Chức năng Đăng nhập mở rộng thêm cơ chế an ninh **`<<extend>>` 'Khóa tài khoản khi đăng nhập sai 5 lần'** để chống tấn công vét cạn mật khẩu.*
> - *Quản trị viên thực hiện cấp phát tài khoản nội bộ, **Phân quyền vai trò (RBAC)** và tra cứu **Audit Logs** để kiểm soát mọi hành vi can thiệp dữ liệu nhạy cảm."*

---

### Slide 20: Biểu đồ Use Case Phân Rã - Tác Nghiệp Quầy Tiền Sảnh & Lễ Tân
- **Tiêu đề Slide**: `BIỂU ĐỒ USE CASE PHÂN RÃ THEO PHÂN HỆ - 3. TÁC NGHIỆP QUẦY TIỀN SẢNH VÀ LỄ TÂN`
- **Nội dung hiển thị**: Quản lý đơn đặt phòng; Check-in, gán phòng; Check-out; Ghi nhận thanh toán; Quản lý thông tin khách hàng.

👉 **Visual Cue**: Chỉ vào nhánh Walk-in tại quầy và Check-out quyết toán.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 20** là phân hệ nghiệp vụ lớn nhất của Resort - **Tác nghiệp Tiền sảnh & Lễ tân**:*
> - *Hệ thống hỗ trợ cả 2 luồng: Tiếp nhận khách đặt trước qua mạng và **Tiếp nhận khách Walk-in tại quầy** (tự động gán phòng tức thời và tạo đơn không cần tài khoản web).*
> - *Thủ tục **Check-in** `<<include>>` lưu trữ thông tin CCCD theo luật lưu trú và gán số phòng vật lý sạch.*
> - *Thủ tục **Check-out** `<<include>>` quyết toán công nợ Folio, xuất hóa đơn tài chính VAT và tự động chuyển phòng sang trạng thái chờ dọn.*
> - *Tích hợp chức năng quản lý **Sơ đồ phòng Gantt** và **Xử lý đơn vắng mặt (No-Show)** sau 23:59."*

---

### Slide 21: Biểu đồ Use Case Phân Rã - Vận Hành Buồng Phòng
- **Tiêu đề Slide**: `BIỂU ĐỒ USE CASE PHÂN RÃ THEO PHÂN HỆ - 4. VẬN HÀNH BUỒNG PHÒNG`
- **Nội dung hiển thị**: Theo dõi trạng thái phòng; Tiếp nhận yêu cầu dọn phòng; Cập nhật trạng thái vệ sinh; Xử lý sự cố và bảo trì.

👉 **Visual Cue**: Chỉ vào quan hệ `<<extend>>` Báo cáo sự cố hư hỏng vật tư.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 21**, phân hệ **Vận hành Buồng phòng**:*
> - *Nhân viên buồng phòng tiếp nhận danh sách phòng bẩn qua thiết bị di động, cập nhật tiến độ từ DIRTY sang CLEANING rồi đến CLEAN.*
> - *Khi phát hiện thiết bị trong phòng bị hư hại (vỡ gương, hỏng máy lạnh), nhân viên kích hoạt Use Case **`<<extend>>` 'Báo cáo sự cố hư hỏng vật tư / Bảo trì phòng'** để chuyển phòng sang diện MAINTENANCE.*
> - *Tổ trưởng buồng phòng thực hiện **'Nghiệm thu kiểm định phòng'** để xác nhận phòng sẵn sàng đón khách mới."*

---

### Slide 22: Biểu đồ Use Case Phân Rã - Quản Trị Doanh Thu, Bảng Giá & Báo Cáo
- **Tiêu đề Slide**: `BIỂU ĐỒ USE CASE PHÂN RÃ THEO PHÂN HỆ - 5. QUẢN TRỊ DOANH THU, BẢNG GIÁ VÀ BÁO CÁO`
- **Nội dung hiển thị**: Quản lý giá phòng; Quản lý khuyến mãi; Theo dõi doanh thu; Thống kê tình trạng và công suất phòng.

👉 **Visual Cue**: Chỉ vào cấu hình giá linh hoạt và báo cáo KPI.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 22**, phân hệ **Quản trị Doanh thu & Báo cáo** dành cho Giám đốc Resort:*
> - *Cho phép cấu hình **Giá linh hoạt theo mùa/cuối tuần (Dynamic Pricing)** và phát hành Voucher ưu đãi.*
> - *Thiết lập khung chính sách hoàn tiền cọc bậc thang theo thời gian báo hủy.*
> - *Hệ thống tự động kết xuất các báo cáo tài chính chuyên ngành khách sạn: Doanh thu thực thu, Công suất sử dụng phòng (Occupancy Rate), và Doanh thu trên mỗi phòng sẵn có (RevPAR)."*

---

### Slide 23: Biểu đồ Hoạt Động Đặt Phòng Trực Tuyến
- **Tiêu đề Slide**: `BIỂU ĐỒ HOẠT ĐỘNG ĐẶT PHÒNG TRỰC TUYẾN`
- **Nội dung hiển thị**: Các bước chính: 1. Khách nhập tìm kiếm $\rightarrow$ 2. Kiểm tra phòng trống $\rightarrow$ 3. Chọn loại phòng $\rightarrow$ 4. Tạo RoomHoldLock 15 phút $\rightarrow$ Thanh toán VNPay $\rightarrow$ Xác nhận đặt phòng.

👉 **Visual Cue**: Chỉ vào thanh ngang Fork phân tách 2 luồng song song (Timer 15 phút và Quét mã QR).

🎙️ **Lời thoại thuyết trình**:
> *"Kính thưa Thầy/Cô, trên **Slide 23** là **Biểu đồ Hoạt động Đặt phòng Trực tuyến (AD-01)**:*
> - *Điểm đột phá kiến trúc nằm ở nút kiểm tra phòng: Nếu còn phòng, hệ thống không chỉ kiểm tra mà ngay lập tức thực thi **Tạo RoomHoldLocks 15 phút** để tạm giữ tồn kho.*
> - *Thanh đồng bộ **Fork** kích hoạt 2 luồng song song: Một luồng khởi động bộ đếm Timer 15:00, luồng kia khách quét mã VietQR trên App Ngân hàng.*
> - *Tại thanh **Join**: Nếu Webhook thanh toán báo thành công trong 15 phút $\rightarrow$ hệ thống tạo Booking chính thức và hủy Timer. Nếu quá 15 phút mà không có tiền $\rightarrow$ Timer tự động kích hoạt tiến trình giải phóng phòng về kho chung."*

🛡️ **Kiến thức phòng thủ chống Thầy vặn**:
- **Thầy vặn**: *"Khác biệt giữa hình thoi Decision và thanh đậm Fork là gì?"*
- **Đáp ngay**: *"Thưa Thầy: Hình thoi Decision là rẽ nhánh có điều kiện (hoặc nhánh này HOẶC nhánh kia chạy). Còn thanh Fork là phân tách xử lý song song (CẢ HAI nhánh đều chạy đồng thời)."*

---

### Slide 24: Biểu đồ Hoạt Động Check-In và Gán Phòng
- **Tiêu đề Slide**: `BIỂU ĐỒ HOẠT ĐỘNG CHECK-IN VÀ GÁN PHÒNG`
- **Nội dung hiển thị**: 1. Khách đến resort $\rightarrow$ 2. Lễ tân tra cứu $\rightarrow$ 3. Kiểm tra trạng thái đơn $\rightarrow$ 4. Lựa chọn phòng vật lý phù hợp $\rightarrow$ 5. Kiểm tra phòng sạch (CLEAN) $\rightarrow$ Gán phòng và bàn giao chìa khóa.

👉 **Visual Cue**: Chỉ vào nút Decision kiểm tra `CLEAN, VACANT & Không trùng lịch`.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 24** là **Biểu đồ Hoạt động Check-in và Gán phòng vật lý (AD-02)**:*
> - *Hệ thống tách biệt rõ: Khách đặt trước chỉ có Hạng phòng, chưa có số phòng. Đến quầy lễ tân mới gán phòng.*
> - *Lễ tân tra cứu đơn, quét CCCD khách lưu trú.*
> - *Hệ thống tự động lọc các phòng vật lý thỏa mãn 3 điều kiện ngặt nghèo: **Thuộc đúng hạng phòng**, **Trạng thái vệ sinh là CLEAN**, và **Lịch phòng VACANT không bị trùng**.*
> - *Sau khi chọn phòng, hệ thống cập nhật phòng sang `OCCUPIED` và giao chìa khóa cho khách."*

---

### Slide 25: Biểu đồ Hoạt Động Sử Dụng Dịch Vụ và Ghi Chi Tiêu Vào Folio
- **Tiêu đề Slide**: `BIỂU ĐỒ HOẠT ĐỘNG SỬ DỤNG DỊCH VỤ VÀ GHI NHẬN CHI TIÊU`
- **Nội dung hiển thị**: 1. Khách dùng dịch vụ $\rightarrow$ 2. Tiếp nhận thông tin $\rightarrow$ 3. Kiểm tra khách và phòng lưu trú $\rightarrow$ 4. Ghi nhận dịch vụ và cộng dồn số dư Folio.

👉 **Visual Cue**: Chỉ vào nút kiểm tra điều kiện `Đúng khách, phòng OCCUPIED` và `Folio còn mở`.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 25** là **Biểu đồ Hoạt động Ghi nhận Dịch vụ vào Folio (AD-03)**:*
> - *Khách sử dụng minibar hoặc ăn uống tại nhà hàng và yêu cầu ghi nợ về phòng.*
> - *Nhân viên nhập số phòng. Hệ thống thực hiện kiểm tra kép: Phòng phải đang ở trạng thái `OCCUPIED` và tài khoản Folio chưa bị khóa.*
> - *Trong cùng một giao dịch (Atomic Transaction), hệ thống vừa lưu chi tiết Order tiêu dùng vừa **cộng dồn khoản nợ vào số dư Folio** của phòng, bảo đảm không bao giờ thất thoát doanh thu dịch vụ."*

---

### Slide 26: Biểu đồ Hoạt Động Check-Out và Quyết Toán
- **Tiêu đề Slide**: `BIỂU ĐỒ HOẠT ĐỘNG CHECK-OUT VÀ QUYẾT TOÁN`
- **Nội dung hiển thị**: 1. Khách yêu cầu trả phòng $\rightarrow$ 2. Lễ tân tra cứu $\rightarrow$ 3. Tổng hợp tiền phòng & dịch vụ $\rightarrow$ 4. Kiểm tra hóa đơn Folio $\rightarrow$ 5. Thanh toán / Hoàn cọc $\rightarrow$ Đổi phòng sang DIRTY.

👉 **Visual Cue**: Chỉ vào điều kiện bảo vệ `[Công nợ bằng 0?]`.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 26** là **Biểu đồ Hoạt động Check-out và Quyết toán (AD-04)**:*
> - *Lễ tân tiếp nhận yêu cầu, hệ thống tổng hợp toàn bộ chi phí: `Tiền phòng + Tiền dịch vụ phát sinh - Tiền cọc đã thu`.*
> - *Nếu khách nợ thêm: Lễ tân thu tiền. Nếu cọc thừa: Lễ tân hoàn tiền mặt.*
> - *Chốt chặn kiểm soát: **Bắt buộc số dư Folio phải bằng 0 (Balance == 0)** thì hệ thống mới cho phép in hóa đơn VAT Saigontourist Group, đóng đơn phòng và tự động đổi trạng thái phòng vật lý sang `DIRTY` (chờ dọn).'*

---

### Slide 27: Biểu đồ Hoạt Động Dọn Buồng Phòng và Xử Lý Bảo Trì
- **Tiêu đề Slide**: `BIỂU ĐỒ HOẠT ĐỘNG DỌN BUỒNG PHÒNG VÀ XỬ LÝ BẢO TRÌ`
- **Nội dung hiển thị**: 1. Phòng chuyển sang cần dọn $\rightarrow$ 2. Buồng phòng nhận danh sách $\rightarrow$ 3. Thực hiện vệ sinh $\rightarrow$ 4. Phát hiện hư hỏng chuyển bảo trì / Dọn sạch phát WebSocket CLEAN.

👉 **Visual Cue**: Chỉ vào 2 nhánh rẽ: Nhánh bình thường chuyển CLEAN và nhánh sự cố tạo MaintenanceTicket chuyển MAINTENANCE.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 27** là **Biểu đồ Hoạt động Vận hành Buồng phòng (AD-05)**:*
> - *Nhân viên buồng phòng mở điện thoại nhận phòng bẩn $\rightarrow$ chuyển sang `CLEANING`.*
> - *Nếu phát hiện sự cố: Chụp ảnh lỗi $\rightarrow$ hệ thống tạo `MaintenanceTicket` và khóa phòng sang `MAINTENANCE` để tổ kỹ thuật xử lý.*
> - *Nếu dọn đạt chuẩn sạch: Nhân viên bấm hoàn thành $\rightarrow$ hệ thống đổi sang `CLEAN` và **bắn sự kiện WebSocket thời gian thực** về quầy lễ tân để sơ đồ phòng chuyển xanh ngay tức khắc mà không cần nhân viên phải gọi bộ đàm."*

---

### Slide 28: Biểu đồ Tuần Tự – Quy Trình Đặt Phòng (Tổng Quan)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ – QUY TRÌNH ĐẶT PHÒNG`
- **Nội dung hiển thị**: Các đối tượng tham gia: Khách hàng, Giao diện website, Bộ xử lý đặt phòng, Cơ sở dữ liệu; Luồng xử lý chính.

👉 **Visual Cue**: Nhấn mạnh triết lý phân tầng BCE trước khi đi vào từng biểu đồ Sequence chi tiết.

🎙️ **Lời thoại thuyết trình**:
> *"Kính thưa Thầy/Cô, từ **Slide 28** mở đầu cho **Khối Biểu đồ Tuần tự BCE**. Toàn bộ 6 biểu đồ tiếp theo đều tuân thủ nguyên lý 3 tầng: **Boundary ($\vdash\bigcirc$)** là giao diện, **Control ($\circlearrowleft$)** là bộ xử lý nghiệp vụ, và **Entity ($\ominus$)** là dữ liệu thực thể. Nhóm tuân thủ quy tắc vàng: **CẤM NHẢY CÓC**, Boundary không được gọi thẳng vào Entity để bảo vệ tính đóng gói và an ninh dữ liệu."*

---

### Slide 29: Biểu đồ Tuần Tự Đặt Phòng và Khóa Phòng Chống Trùng (SD-01)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ ĐẶT PHÒNG VÀ KHÓA PHÒNG CHỐNG TRÙNG`
- **Bản vẽ**: Toàn bộ Sequence Diagram SD-01 với 17 thông điệp chi tiết.

👉 **Visual Cue**: Chỉ vào thông điệp tạo Hold Lock 15 phút, vạch kích hoạt và khung Alt vnp_ResponseCode == '00'.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 29** là **Sequence SD-01: Đặt phòng trực tuyến & Khóa giữ 15 phút**:*
> - *Khách chọn loại phòng trên Boundary `:SearchBookingUI` $\rightarrow$ gọi Control `:BookingService` hàm `yeuCauGiuChoTamThoi`.*
> - *`:BookingService` gọi Entity `:RoomInventory` kiểm tra phòng trống và thực thi hàm `createHoldLock(roomTypeId, expiresAt = now + 15m)` sinh mã `lockId`.*
> - *Giao diện hiển thị đếm ngược 15:00 và mã VietQR từ cổng VNPay.*
> - *Khung **Alt [Thành công, vnp_ResponseCode == '00']**: VNPay bắn Webhook IPN $\rightarrow$ `:BookingService` lưu giao dịch, tạo bản ghi `:Booking` trạng thái `CONFIRMED`, sinh `:BookingNights`, và gọi `markLockAsSold` chuyển khóa tạm sang ĐÃ BÁN.*
> - *Khung **Alt [else: Hết hạn / Khách hủy]**: Hệ thống gọi `markLockAsExpired` để hoàn trả tồn kho ngay lập tức."*

---

### Slide 30: Biểu đồ Tuần Tự Làm Thủ Tục Nhận Phòng (SD-02)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ LÀM THỦ TỤC NHẬN PHÒNG`
- **Bản vẽ**: Toàn bộ Sequence Diagram SD-02 với 16 thông điệp chi tiết.

👉 **Visual Cue**: Chỉ vào bước quét CCCD `saveIdentityProfile` và hàm `checkCleanRooms`.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 30** là **Sequence SD-02: Thủ tục Check-in & Gán phòng vật lý**:*
> - *Lễ tân nhập mã PNR trên `:FrontDeskGanttUI` $\rightarrow$ `:CheckInController` lấy thông tin đơn.*
> - *Quét CCCD khách $\rightarrow$ gọi `:GuestProfile` lưu thông tin lưu trú.*
> - *Control gọi thực thể `:PhysicalRoom` hàm `checkCleanRooms(roomTypeId, status='CLEAN')`.*
> - *Nếu có phòng sạch: Đổi trạng thái đơn `:Booking` sang `CHECKED_IN`, gọi `assignPhysicalRoom` gán số phòng cụ thể vào từng đêm trong `:BookingNight`, và đổi phòng vật lý sang `OCCUPIED`. Lễ tân in phiếu nhận phòng và giao thẻ từ cho khách."*

---

### Slide 31: Biểu đồ Tuần Tự Ghi Nhận Tiêu Dùng Dịch Vụ (SD-03)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ GHI NHẬN TIÊU DÙNG DỊCH VỤ`
- **Bản vẽ**: Toàn bộ Sequence Diagram SD-03 với 12 thông điệp chi tiết.

👉 **Visual Cue**: Chỉ vào bước `recordConsumption` và `postChargeToFolio`.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 31** là **Sequence SD-03: Ghi nhận Dịch vụ phát sinh vào Folio**:*
> - *Nhân viên nhập số phòng trên `:ServicePostingUI` $\rightarrow$ `:FolioBillingService` xác thực phòng đang `CHECKED_IN`.*
> - *Nhân viên chọn món minibar $\rightarrow$ Control lấy đơn giá từ `:PriceCatalog`, tính tổng tiền gồm VAT.*
> - *Control gọi thực thể `:FolioInvoice` hàm `recordConsumption` lưu chi tiết tiêu dùng, đồng thời gọi `postChargeToFolio` cộng dồn số dư nợ của phòng.*
> - *In phiếu Voucher cho khách ký xác nhận."*

---

### Slide 32: Biểu đồ Tuần Tự Trả Phòng và Quyết Toán (SD-04)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ TRẢ PHÒNG VÀ QUYẾT TOÁN`
- **Bản vẽ**: Toàn bộ Sequence Diagram SD-04 với 16 thông điệp chi tiết.

👉 **Visual Cue**: Chỉ vào bước tính công nợ, xuất hóa đơn VAT MST 0312456789-001, và đổi phòng sang DIRTY.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 32** là **Sequence SD-04: Thủ tục Check-out & Quyết toán Folio**:*
> - *Lễ tân nạp phụ thu kiểm phòng minibar $\rightarrow$ `:FolioBillingService` tính toán tổng nợ theo công thức kế toán:*
>   $$\text{Số dư} = \text{Tiền phòng} + \text{Dịch vụ phát sinh} - \text{Tiền cọc}$$
> - *Lễ tân thu tiền thiếu $\rightarrow$ lưu chứng từ `:PaymentTransaction`.*
> - *Hệ thống tự động khởi tạo hóa đơn tài chính điện tử `:Invoice` với thuế suất VAT 8%, mã số thuế Saigontourist Group `0312456789-001`.*
> - *Đổi trạng thái đơn `:Booking` sang `CHECKED_OUT`, đóng Folio, và lập tức gửi thông điệp đổi phòng `:PhysicalRoom` sang `DIRTY`."*

---

### Slide 33: Biểu đồ Tuần Tự Vận Hành Dọn Dẹp Buồng Phòng (SD-05)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ VẬN HÀNH DỌN DẸP BUỒNG PHÒNG`
- **Bản vẽ**: Toàn bộ Sequence Diagram SD-05 với 21 thông điệp chi tiết.

👉 **Visual Cue**: Chỉ vào bước bấm giờ `:CleaningLog` và thông điệp WebSocket `notifyRoomStatus(roomId, 'CLEAN')`.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 33** là **Sequence SD-05: Vận hành Dọn dẹp Buồng phòng**:*
> - *Nhân viên mở điện thoại $\rightarrow$ hệ thống hiển thị danh sách phòng `DIRTY`.*
> - *Bấm nhận dọn $\rightarrow$ đổi phòng sang `CLEANING` và tạo `:CleaningLog` bấm giờ ca dọn.*
> - *Dọn xong đạt chuẩn $\rightarrow$ đổi phòng sang `CLEAN`, đóng ca dọn kết quả `PASSED`.*
> - *Control bắn **WebSocket Event `notifyRoomStatus(roomId, 'CLEAN')`** $\rightarrow$ Sơ đồ buồng phòng tại quầy lễ tân lập tức đổi sang màu xanh đón khách mới.*
> - *Nếu phát hiện hỏng hóc: Chụp ảnh lỗi $\rightarrow$ chuyển phòng sang `MAINTENANCE` và tạo phiếu `:MaintenanceTicket` gửi tổ kỹ thuật."*

---

### Slide 34: Biểu đồ Tuần Tự Hủy Đặt Phòng và Hoàn Tiền Cọc (SD-06)
- **Tiêu đề Slide**: `BIỂU ĐỒ TUẦN TỰ HỦY ĐẶT PHÒNG VÀ HOÀN TIỀN CỌC`
- **Bản vẽ**: Toàn bộ Sequence Diagram SD-06 với 27 thông điệp chi tiết.

👉 **Visual Cue**: Chỉ vào hàm `getRefundPercentage(hoursRemaining)`, chứng từ tiền âm, và hàm `releaseBookedNights`.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 34** là **Sequence SD-06: Hủy phòng & Hoàn cọc bậc thang**:*
> - *Khách bấm Yêu cầu hủy trên `:BookingHistoryUI` $\rightarrow$ `:BookingCancellationService` tiếp nhận.*
> - *Control gọi `:RefundPolicy` với tham số `hoursRemaining` (tính đến 14:00 ngày check-in) để xác định tỷ lệ hoàn tiền: **100%** (trước 72h), **50%** (từ 24-72h), hoặc **0%** (dưới 24h).*
> - *Khách xác nhận hủy $\rightarrow$ đổi đơn sang `Canceled` và lưu biên bản `:CancellationRecord`.*
> - *Nếu có hoàn tiền (`refundAmount > 0`), hệ thống ghi nhận chứng từ hoàn tiền với **số tiền âm** (`-refundAmount`) vào `:PaymentTransaction`.*
> - *Thao tác then chốt: Gọi **`releaseBookedNights`** xóa các đêm lưu trú trong `:BookingNight` để mở lại phòng trống ngay lập tức trên website."*

---

### Slide 35: Biểu đồ Lớp – Class Diagram (Giới Thiệu)
- **Tiêu đề Slide**: `BIỂU ĐỒ LỚP – CLASS DIAGRAM`
- **Nội dung hiển thị**: Các mối quan hệ: Khách hàng thực hiện đặt phòng; Đặt phòng liên kết với phòng; Đặt phòng phát sinh hóa đơn; Nhân viên xử lý nghiệp vụ; Tài khoản gán quyền; Giới thiệu nguyên lý cấu trúc tĩnh.

👉 **Visual Cue**: Nhấn mạnh nguyên lý Information Expert và tách biệt thực thể nghiệp vụ với CSDL.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 35**, nhóm giới thiệu tổng quan về **Biểu đồ Lớp Lĩnh vực (Domain Class Diagram)**: Biểu đồ mô tả cấu trúc dữ liệu tĩnh của toàn bộ hệ thống thông qua các lớp đối tượng, thuộc tính, phương thức và các mối liên kết hướng đối tượng chuẩn mực."*

---

### Slide 36: Biểu đồ Lớp – Class Diagram (Chi Tiết)
- **Tiêu đề Slide**: `BIỂU ĐỒ LỚP – CLASS DIAGRAM`
- **Bản vẽ**: Toàn bộ Class Diagram 3 ngăn chi tiết.

👉 **Visual Cue**: Chỉ vào hình thoi đen đặc Composition giữa Booking và BookingNight, giữa Folio và FolioItem; và hình thoi trắng rỗng Aggregation giữa Hotel và RoomType.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 36** là **Bản vẽ chi tiết Biểu đồ Lớp**:*
> - *Mỗi lớp gồm 3 ngăn: Tên lớp, Thuộc tính và Phương thức theo nguyên lý **Information Expert** (như `tinhTongTien()`, `kiemTraPhongTrong()`), không đưa hàm SQL vào lớp.*
> - *Mối quan hệ **Hợp thành (Composition $\blacklozenge$)** ràng buộc sinh tử: `BookingMaster` hợp thành các `BookingNight`; `ServiceFolio` hợp thành các `FolioItem`.*
> - *Mối quan hệ **Thu nạp (Aggregation $\diamondsuit$)** độc lập vòng đời: `Hotel` thu nạp `RoomType`, `RoomType` thu nạp `PhysicalRoom`.*
> - *Mối quan hệ **Kế thừa (Generalization)** từ lớp cha `Account` sang `CustomerAccount` và `StaffAccount`."*

🛡️ **Kiến thức phòng thủ chống Thầy vặn**:
- **Thầy vặn**: *"Khác biệt giữa Composition và Aggregation trong bài này là gì?"*
- **Đáp ngay**: *"Thưa Thầy, Composition (kim cương đen) là quan hệ sở hữu sinh tử: nếu xóa `BookingMaster`, các `BookingNight` bên trong bắt buộc bị hủy theo. Còn Aggregation (kim cương trắng) là quan hệ độc lập vòng đời: nếu một `PhysicalRoom` tạm đóng để sơn sửa, hạng phòng `RoomType` và `Hotel` vẫn tồn tại bình thường."*

---

### Slide 37: Biểu đồ Gói – Package Diagram
- **Tiêu đề Slide**: `BIỂU ĐỒ GÓI – PACKAGE DIAGRAM`
- **Bản vẽ**: 5 Tầng kiến trúc: `<<user interface>>`, `<<application>>`, `<<domain>>`, `<<infrastructure>>`, `<<database>>`.

👉 **Visual Cue**: Chỉ vào chiều mũi tên nét đứt `<<use>>` một chiều từ trên xuống.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 37** là **Biểu đồ Gói (Package Diagram)** tổ chức mã nguồn theo mô hình phân tầng chuẩn mực:*
> - *Tầng trên cùng là **`<<user interface>>`** (màn hình người dùng) $\rightarrow$ phụ thuộc vào tầng **`<<application>>`** (điều phối request và kiểm tra quyền).*
> - *Tầng điều phối gọi xuống tầng nghiệp vụ lõi **`<<domain>>`** (chia thành 5 gói con: Đặt phòng, Nhận phòng, Dịch vụ phát sinh, Trả phòng, Buồng phòng).*
> - *Tầng Domain tương tác với hạ tầng qua **`<<infrastructure>>`** (quản lý kết nối, truy vấn, transaction) để lưu trữ vào **`<<database>>`**.*
> - *Cấu trúc bảo đảm nguyên lý Dependency Inversion, không xảy ra phụ thuộc vòng."*

---

### Slide 38: Biểu đồ Triển Khai – Deployment Diagram
- **Tiêu đề Slide**: `BIỂU ĐỒ TRIỂN KHAI – DEPLOYMENT DIAGRAM`
- **Bản vẽ**: Mô hình triển khai 3-Tier Enterprise: Client Tier, Application Server Tier, Data & External Services Tier.

👉 **Visual Cue**: Chỉ vào cáp USB máy in POS, Reverse Proxy Nginx, tiến trình Cron ngầm và Database subnet.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 38** là **Biểu đồ Triển khai Vật lý (Deployment Diagram)** chứng minh tính khả thi vận hành thực tế:*
> - **Tầng 1 (Client Tier)**: Thiết bị khách hàng B2C, Mobile buồng phòng (PWA), và Máy trạm Lễ tân kết nối trực tiếp máy in nhiệt POS qua cổng `USB 2.0 / TCP Port 9100` để in bill tức thì < 0.5s kể cả khi mất Internet.*
> - **Tầng 2 (App Server Tier)**: Máy chủ Ubuntu Linux với **Nginx Reverse Proxy** (mã hóa `TLS 1.3/HTTPS Port 443`, phân đoạn mạng nội bộ `VLAN 20`, WebSocket WSS thời gian thực), môi trường **Python WSGI Container**, và **Cron Daemon** ngầm (`cron_worker.py`) tự động dọn dẹp các phiên giữ phòng quá hạn 15 phút.*
> - **Tầng 3 (Data & External Tier)**: CSDL trong mạng biệt lập `Dedicated DB Subnet`, liên kết Cổng VNPay (REST/IPN) và Cổng Mail điện toán đám mây (SMTP Port 587)."*

---

### Slide 39: Biểu đồ Thành Phần Tổng Quát
- **Tiêu đề Slide**: `BIỂU ĐỒ THÀNH PHẦN TỔNG QUÁT`
- **Bản vẽ**: Kiến trúc mô-đun hóa tổng thể: Ứng dụng giao diện, Mô-đun giao tiếp, Ứng dụng nghiệp vụ, Thư viện kết nối và CSDL.

👉 **Visual Cue**: Chỉ vào sự phân tách giữa Executable giao diện và Executable nghiệp vụ.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 39** là **Biểu đồ Thành phần Tổng quát**: Thể hiện kiến trúc phần mềm ở mức các khối mô-đun độc lập có thể thay thế được (`<<executable>>`, `<<component>>`, `<<library>>`, `<<database>>`). Ứng dụng giao diện kết nối với Ứng dụng nghiệp vụ thông qua Mô-đun giao tiếp chuẩn hóa, độc lập hoàn toàn với tầng lưu trữ CSDL."*

---

### Slide 40: Biểu đồ Thành Phần - Đặt Phòng và Giữ Phòng Trực Tuyến
- **Tiêu đề Slide**: `BIỂU ĐỒ THÀNH PHẦN ĐẶT PHÒNG VÀ GIỮ PHÒNG TRỰC TUYẾN`
- **Bản vẽ**: Module Đặt phòng & thanh toán $\leftrightarrow$ Tiếp nhận $\leftrightarrow$ Giữ tồn phòng 15m $\leftrightarrow$ Xác nhận đặt phòng $\leftrightarrow$ CSDL.

👉 **Visual Cue**: Chỉ vào Module Giữ tồn phòng và luồng giữ tồn 15 phút.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 40** là **Biểu đồ Thành phần Phân hệ Đặt phòng B2C**: Giao diện đặt phòng gửi request qua mô-đun giao tiếp đến Mô-đun Tiếp nhận $\rightarrow$ kích hoạt **Mô-đun Giữ tồn phòng** để xác lập khóa tạm 15 phút trong CSDL $\rightarrow$ sau khi thanh toán thành công, Mô-đun Xác nhận đặt phòng cập nhật chính thức đơn hàng và xuất chứng từ."*

---

### Slide 41: Biểu đồ Thành Phần - Nhận Phòng và Gán Phòng Vật Lý
- **Tiêu đề Slide**: `BIỂU ĐỒ THÀNH PHẦN NHẬN PHÒNG VÀ GÁN PHÒNG VẬT LÝ`
- **Bản vẽ**: Màn hình lễ tân $\leftrightarrow$ Tiếp nhận yêu cầu nhận phòng $\leftrightarrow$ Gán phòng và nhận phòng $\leftrightarrow$ Truy cập dữ liệu CSDL.

👉 **Visual Cue**: Chỉ vào Mô-đun Gán phòng và nhận phòng.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 41** là **Biểu đồ Thành phần Phân hệ Nhận phòng**: Mô-đun tiếp nhận tại quầy liên kết với **Mô-đun Gán phòng và nhận phòng**, thực thi thuật toán kiểm tra phòng sạch và phân bổ số phòng vật lý vào các đêm lưu trú trong CSDL."*

---

### Slide 42: Biểu đồ Thành Phần - Ghi Nhận Dịch Vụ Phát Sinh
- **Tiêu đề Slide**: `BIỂU ĐỒ THÀNH PHẦN GHI NHẬN DỊCH VỤ PHÁT SINH`
- **Bản vẽ**: Ghi khoản phát sinh tại quầy $\leftrightarrow$ Tiếp nhận $\leftrightarrow$ Ghi dịch vụ phát sinh $\leftrightarrow$ Tính lại hóa đơn $\leftrightarrow$ CSDL.

👉 **Visual Cue**: Chỉ vào Mô-đun Tính lại hóa đơn.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 42** là **Biểu đồ Thành phần Ghi nhận Dịch vụ**: Khi nhân viên ghi khoản phát sinh tại quầy, yêu cầu được chuyển đến **Mô-đun Ghi dịch vụ phát sinh** $\rightarrow$ tự động kích hoạt **Mô-đun Tính lại hóa đơn** để cập nhật số dư công nợ Folio tức thời."*

---

### Slide 43: Biểu đồ Thành Phần - Trả Phòng
- **Tiêu đề Slide**: `BIỂU ĐỒ THÀNH PHẦN TRẢ PHÒNG`
- **Bản vẽ**: Màn hình quyết toán $\leftrightarrow$ Tiếp nhận $\leftrightarrow$ Quyết toán trả phòng $\leftrightarrow$ Chốt đặt phòng & Chuyển phòng sang chờ dọn.

👉 **Visual Cue**: Chỉ vào Mô-đun Quyết toán trả phòng và cổng kết nối đổi trạng thái phòng.

🎙️ **Lời thoại thuyết trình**:
> *"Tại **Slide 43** là **Biểu đồ Thành phần Trả phòng**: Màn hình quyết toán kết nối với **Mô-đun Quyết toán trả phòng**, thực hiện đối soát tổng tiền, ghi nhận thanh toán, chốt Folio và kích hoạt đổi trạng thái phòng vật lý sang chờ dọn (DIRTY) trong CSDL."*

---

### Slide 44: Biểu đồ Thành Phần - Vệ Sinh Buồng Phòng
- **Tiêu đề Slide**: `BIỂU ĐỒ THÀNH PHẦN VỆ SINH BUỒNG PHÒNG`
- **Bản vẽ**: Màn hình buồng phòng mobile $\leftrightarrow$ Tiếp nhận $\leftrightarrow$ Cập nhật phòng sạch $\leftrightarrow$ CSDL Phòng vật lý.

👉 **Visual Cue**: Chỉ vào Mô-đun cập nhật phòng sạch.

🎙️ **Lời thoại thuyết trình**:
> *"Trên **Slide 44** là **Biểu đồ Thành phần Vệ sinh Buồng phòng**: Ứng dụng di động buồng phòng giao tiếp qua API với **Mô-đun Tiếp nhận buồng phòng** để tải danh sách phòng bẩn và gửi tín hiệu xác nhận phòng sạch về máy chủ."*

---

### Slide 45: Thiết Kế Dữ Liệu (15 Bảng 3NF)
- **Tiêu đề Slide**: `THIẾT KẾ DỮ LIỆU`
- **Bản vẽ**: Bản vẽ UML Database Design gồm 15 bảng quan hệ chuẩn 3NF: `T_Role`, `T_StaffProfile`, `T_Account`, `T_CustomerProfile`, `T_RoomHoldLock`, `T_RoomType`, `T_PhysicalRoom`, `T_HousekeepingLog`, `T_MaintenanceTicket`, `T_Booking`, `T_BookingNight`, `T_ServiceItem`, `T_ServiceConsumption`, `T_FolioInvoice`, `T_PaymentTransaction`.

👉 **Visual Cue**: Chỉ vào cặp bảng `T_RoomType` vs `T_PhysicalRoom`, và `T_Booking` vs `T_BookingNight`.

🎙️ **Lời thoại thuyết trình**:
> *"Kính thưa Thầy/Cô, trên **Slide 45** là **Biểu đồ Thiết kế Dữ liệu gồm 15 bảng đạt chuẩn 3NF thuần khiết**, loại bỏ hoàn toàn God-table `New_Bookings`:*
> 1. *Tách biệt `T_RoomType` (loại phòng kinh doanh) và `T_PhysicalRoom` (14 phòng vật lý thực tế với trạng thái buồng phòng và lưu trú).*
> 2. *Tách biệt `T_Booking` (thông tin chung, PNR Code duy nhất) và `T_BookingNight` (lưu giá và trạng thái chi tiết từng đêm), giúp hỗ trợ đổi phòng giữa chừng (Split Stay) và tối ưu đếm phòng trống bằng phép `COUNT(*)` cực nhanh.*
> 3. *Bảng `T_RoomHoldLock` lưu vết phiên giữ chỗ 15 phút chống Race Condition.*
> 4. *Tài khoản `T_FolioInvoice` độc lập với Booking, tổng hợp chi tiêu từ `T_ServiceConsumption` và đối soát qua `T_PaymentTransaction`.*
> 5. *Toàn bộ CSDL được bảo vệ bởi khóa chính (PK) đỏ, khóa ngoại (FK) xanh, và đã vượt qua **43/43 tests tự động đạt 100%**."*

🛡️ **Kiến thức phòng thủ chống Thầy vặn**:
- **Thầy vặn**: *"Chứng minh bảng `T_Booking` và `T_BookingNight` đạt 3NF?"*
- **Đáp ngay**: *"Thưa Thầy:
  * Đạt **1NF**: Mọi thuộc tính đều nguyên tố, không có cột đa trị (nếu lưu chung ngày đến/đi thì danh sách các phòng được gán sẽ là mảng đa trị vi phạm 1NF).
  * Đạt **2NF**: Khóa chính đơn `nightId`, mọi thuộc tính (`stayDate`, `nightPrice`, `idPhysicalRoom`) đều phụ thuộc đầy đủ vào khóa chính.
  * Đạt **3NF**: Không có phụ thuộc bắc cầu qua thuộc tính không khóa. Thông tin loại phòng nằm ở `T_RoomType`, không lặp lại trong BookingNight."*

---

# PHẦN III: THIẾT KẾ GIAO DIỆN & KẾT LUẬN (SLIDE 46 - 52)

### Slide 46: Thiết Kế Giao Diện - Trang Chủ
- **Nội dung slide**: Hình ảnh giao diện Trang chủ phong cách Editorial Coastal Luxury (`#072A44`, `#DFB76C`, `#10B981`).
- 🎙️ **Lời thoại**: *"Chuyển sang Phần 5 - Thiết kế giao diện thực tế: Trên Slide 46 là Trang chủ B2C chuẩn 5 sao Coastal Luxury, tích hợp thanh tìm kiếm thông minh và hiển thị hình ảnh thực tế của resort."*

### Slide 47: Giao Diện Đăng Nhập & Đăng Ký
- **Nội dung slide**: Form xác thực đăng ký hội viên VIP và đăng nhập an toàn.
- 🎙️ **Lời thoại**: *"Slide 47 là giao diện Đăng ký/Đăng nhập với cơ chế mã hóa mật khẩu và phân quyền vai trò RBAC."*

### Slide 48: Giao Diện Tìm Phòng & Xem Chi Tiết
- **Nội dung slide**: Danh sách phòng theo thời gian thực và modal chi tiết tiện ích.
- 🎙️ **Lời thoại**: *"Slide 48 là giao diện Tìm phòng và Chi tiết hạng phòng, đồng bộ dữ liệu thời gian thực từ bảng `T_RoomType` và `T_PhysicalRoom`."*

### Slide 49: Giao Diện Giữ Phòng & Thanh Toán
- **Nội dung slide**: Đồng hồ đếm ngược 15:00 và mã VietQR thanh toán.
- 🎙️ **Lời thoại**: *"Slide 49 hiện thực hóa chính xác Sequence SD-01 và AD-01: Hiển thị đồng hồ đếm ngược 15:00 giữ chỗ tạm thời và mã QR thanh toán VNPay."*

### Slide 50: Giao Diện Lịch Sử Đặt Phòng
- **Nội dung slide**: Danh sách hành trình lưu trú của khách, tra cứu mã PNR và thẻ hội viên Gold.
- 🎙️ **Lời thoại**: *"Slide 50 là trang Lịch sử đặt phòng của khách, hiển thị chi tiết đêm ở, trạng thái đơn và tích lũy điểm thưởng Loyalty."*

### Slide 51: Giao Diện Hủy Phòng
- **Nội dung slide**: Bảng xem trước hoàn cọc bậc thang (Preview Modal) và nút xác nhận hủy.
- 🎙️ **Lời thoại**: *"Slide 51 hiện thực hóa Sequence SD-06 và AD-06: Tự động tính toán số tiền hoàn cọc theo chính sách trước 72h/24h và gửi biên bản hủy về hệ thống."*

### Slide 52: Lời Cảm Ơn & Q&A
- **Nội dung slide**: `THANK YOU - CẢM ƠN QUÝ THẦY CÔ VÀ CÁC BẠN ĐÃ LẮNG NGHE!`
- 🎙️ **Lời thoại**:
  > *"Kính thưa Quý Thầy/Cô trong Hội đồng,*
  >
  > *Toàn bộ 52 slide vừa qua đã trình bày trọn vẹn và nhất quán quá trình phân tích thiết kế hệ thống từ bài toán nghiệp vụ Côn Đảo, mô hình Use Case, dòng chảy Activity, tương tác 3 tầng Sequence BCE, kiến trúc Gói & Triển khai, cho đến CSDL 15 bảng 3NF và giao diện thực tế.*
  >
  > *Nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc đến Quý Thầy/Cô đã tận tình hướng dẫn. Nhóm xin trân trọng kính mời Hội đồng đặt câu hỏi phản biện ạ!"*
