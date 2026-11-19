### Slide 17: Biểu đồ Use Case tổng quát
Kính thưa Thầy Cô, bước vào phần mô hình hóa hệ thống, Slide 17 thể hiện Biểu đồ Use Case tổng quát. Hệ thống đóng gói toàn bộ 15 Use Case cốt lõi bên trong ranh giới rõ ràng, phân định 5 nhóm tác nhân người dùng và 2 tác nhân ngoại vi là Cổng thanh toán VNPay cùng Máy chủ dịch vụ Cron System.

### Slide 18: Phân rã Use Case - Cổng đặt phòng B2C
Tại phân hệ Đặt phòng B2C, Use Case Đặt phòng trực tuyến bắt buộc quan hệ Include với Khóa phòng 15 phút chống trùng và Xác thực thanh toán trực tuyến. Khi khách hàng có mã ưu đãi, hành vi Áp dụng voucher sẽ được kích hoạt thông qua quan hệ Extend trỏ ngược về Use Case cơ sở.

### Slide 19: Phân rã Use Case - Quản lý tài khoản & Phân quyền
Phân hệ Tài khoản quản lý toàn bộ vòng đời người dùng từ Đăng ký hội viên đến Phân quyền đa vai trò RBAC cho nhân sự. Hệ thống tích hợp Audit Log ghi vết bảo mật và quan hệ Extend tự động khóa tài khoản sau 5 lần đăng nhập thất bại nhằm ngăn chặn tấn công Brute-force.

### Slide 20: Phân rã Use Case - Tác nghiệp quầy tiền sảnh & Lễ tân
Tại quầy tiền sảnh, hệ thống đáp ứng cả hai luồng nghiệp vụ: Đặt phòng trực tiếp Walk-in cho khách vãng lai và Check-in cho khách đặt trước. Lễ tân quản lý phòng trực quan qua sơ đồ Gantt thời gian thực, xử lý quyết toán Folio VAT khi Check-out và tự động hủy đơn No-Show đối với khách vắng mặt sau 23:59.

### Slide 21: Phân rã Use Case - Vận hành buồng phòng
Phân hệ Buồng phòng hỗ trợ nhân viên nhận ca làm việc trên thiết bị di động, theo dõi danh sách phòng bẩn và cập nhật tiến độ dọn dẹp. Khi phát hiện hỏng hóc vật tư, Use Case Báo cáo sự cố bảo trì được mở rộng qua quan hệ Extend để khóa phòng kỹ thuật trước khi Tổ trưởng nghiệm thu.

### Slide 22: Phân rã Use Case - Quản trị doanh thu & Báo cáo
Phân hệ Quản trị cho phép Ban Giám đốc thiết lập biểu giá linh hoạt Dynamic Pricing theo mùa cao điểm và ban hành chính sách hoàn cọc bậc thang. Toàn bộ doanh thu phòng, dịch vụ cùng các chỉ số KPI tiêu chuẩn của khách sạn như RevPAR và công suất phòng được tổng hợp tự động theo thời gian thực.

### Slide 23: Biểu đồ Hoạt động - Đặt phòng trực tuyến (AD-01)
Biểu đồ Hoạt động AD-01 mô hình hóa luồng xử lý đồng thời để giải quyết bài toán Overbooking. Ngay khi khách chọn phòng, hệ thống khởi tạo bản ghi RoomHoldLock giữ chỗ 15 phút. Thanh phân nhánh Fork kích hoạt song song đồng hồ đếm ngược 15:00 và tiến trình quét VietQR; nếu thanh toán thành công thì xác nhận Booking, nếu hết giờ thì tự động giải phóng phòng.

### Slide 24: Biểu đồ Hoạt động - Check-in và Gán phòng vật lý (AD-02)
Biểu đồ AD-02 quy định luồng kiểm soát gán phòng vật lý cho cả khách đặt trước và khách Walk-in. Hệ thống bọc điều kiện bảo vệ nghiêm ngặt: chỉ cho phép lễ tân gán những phòng thỏa mãn đồng thời ba tiêu chuẩn: đúng hạng phòng đã đăng ký, trạng thái buồng phòng đạt chuẩn Clean đã nghiệm thu, và lịch phòng hoàn toàn Vacant.

### Slide 25: Biểu đồ Hoạt động - Dịch vụ phát sinh và Ghi nợ Folio (AD-03)
Biểu đồ AD-03 thể hiện cơ chế quản trị công nợ lưu trú. Khi khách phát sinh tiêu dùng minibar hoặc ẩm thực, hệ thống kiểm tra trạng thái phòng đang Occupied và tài khoản Folio đang mở. Sau đó, một giao dịch nguyên tử được thực thi để ghi nhận chi tiết dịch vụ và tự động cộng dồn số dư nợ vào Folio của phòng.

### Slide 26: Biểu đồ Hoạt động - Check-out và Quyết toán công nợ (AD-04)
Biểu đồ AD-04 xử lý quy trình tất toán theo công thức: Số dư thanh toán bằng Tiền phòng cộng Tổng dịch vụ trừ Tiền cọc. Nút rẽ nhánh kiểm soát điều kiện công nợ bằng 0: chỉ khi số dư được đối soát cân bằng, hệ thống mới xuất hóa đơn tài chính VAT Saigontourist và tự động chuyển trạng thái phòng sang Dirty để kích hoạt ca dọn.

### Slide 27: Biểu đồ Hoạt động - Vận hành buồng phòng và Bảo trì (AD-05)
Biểu đồ AD-05 khép kín chu trình làm sạch: nhân viên nhận phòng chuyển trạng thái sang Cleaning. Nếu phát hiện hư hỏng, quy trình rẽ nhánh khóa Maintenance; nếu phòng dọn đạt chuẩn kiểm tra, hệ thống chuyển sang Clean và lập tức bắn tín hiệu WebSocket thời gian thực để sơ đồ quầy lễ tân đổi sang màu xanh tức thì.

### Slide 28: Biểu đồ Tuần tự - Giới thiệu mô hình kiến trúc BCE
Slide 28 mở đầu cho khối biểu đồ tuần tự. Toàn bộ 6 ca sử dụng then chốt được thiết kế theo đúng mẫu hình phân tầng Boundary - Control - Entity, tuân thủ nguyên tắc bao đóng: Boundary tiếp nhận tương tác nhưng không bao giờ truy cập trực tiếp vào Entity mà phải thông qua Control điều phối logic nghiệp vụ.

### Slide 29: Biểu đồ Tuần tự - Đặt phòng trực tuyến & Khóa 15m (SD-01)
Biểu đồ SD-01 thể hiện 17 thông điệp tương tác: BookingService yêu cầu RoomInventory khởi tạo khóa tạm CreateHoldLock 15 phút trong DB Transaction. Khi nhận Webhook IPN từ cổng VNPay, BookingService tạo thực thể Booking Confirmed, sinh các bản ghi BookingNights và gọi hàm MarkLockAsSold để chốt phòng thành công.

### Slide 30: Biểu đồ Tuần tự - Làm thủ tục nhận phòng Check-in (SD-02)
Biểu đồ SD-02 gồm 16 thông điệp: Lễ tân tra cứu mã PNR, quét thông tin CCCD lưu vào GuestProfile. Control gọi PhysicalRoom lọc danh sách phòng sạch CheckCleanRooms; sau đó thực thi hàm AssignPhysicalRoom để gán phòng cụ thể cho từng đêm lưu trú và cập nhật trạng thái phòng sang Occupied.

### Slide 31: Biểu đồ Tuần tự - Ghi nhận tiêu dùng dịch vụ (SD-03)
Biểu đồ SD-03 gồm 12 thông điệp: FolioBillingService xác thực phòng lưu trú hợp lệ, truy vấn đơn giá có thuế từ PriceCatalog. Tiếp đó, hệ thống lưu chi tiết tiêu dùng vào FolioItem và kích hoạt hàm PostChargeToFolio để cộng dồn khoản nợ vào số dư của hóa đơn phòng.

### Slide 32: Biểu đồ Tuần tự - Trả phòng và Quyết toán (SD-04)
Biểu đồ SD-04 gồm 16 thông điệp: Lễ tân nạp phụ thu phát sinh, hệ thống tính toán số dư cuối kỳ và thực thu số tiền còn thiếu. Ngay khi tất toán, Control khởi tạo hóa đơn Invoice với thuế suất VAT 8% theo mã số thuế Saigontourist và gửi thông điệp cập nhật trạng thái phòng sang Dirty.

### Slide 33: Biểu đồ Tuần tự - Vận hành dọn dẹp buồng phòng (SD-05)
Biểu đồ SD-05 gồm 21 thông điệp: Nhân viên buồng phòng nhận nhiệm vụ, cập nhật trạng thái Cleaning và khởi tạo CleaningLog để tính định mức thời gian. Khi công việc hoàn tất, hệ thống chuyển phòng sang Clean và phát sự kiện WebSocket NotifyRoomStatus cập nhật trực tiếp lên màn hình lễ tân.

### Slide 34: Biểu đồ Tuần tự - Hủy đặt phòng và Hoàn cọc (SD-06)
Biểu đồ SD-06 gồm 27 thông điệp: BookingCancellationService gọi RefundPolicy tính toán khoảng cách giờ đến thời điểm Check-in để áp mức hoàn cọc 100%, 50% hoặc 0%. Hệ thống cập nhật đơn sang Canceled, ghi nhận chứng từ hoàn tiền âm vào sổ quỹ và lập tức gọi ReleaseBookedNights để trả lại quỹ phòng trống cho thị trường.

### Slide 35: Biểu đồ Lớp Lĩnh vực - Khái quát cấu trúc tĩnh
Slide 35 khái quát cấu trúc tĩnh Domain Class Diagram với đầy đủ các thực thể đại diện cho toàn bộ miền nghiệp vụ khách sạn biển đảo, từ lưu trú, buồng phòng, dịch vụ đến thanh toán và chính sách giá.

### Slide 36: Biểu đồ Lớp Lĩnh vực - Chi tiết thuộc tính, phương thức và quan hệ
Slide 36 là bản vẽ chi tiết thiết kế 3 ngăn chuẩn mực. Điểm mấu chốt là mối quan hệ Hợp thành Composition ràng buộc sinh tử giữa BookingMaster và BookingNight, giữa ServiceFolio và FolioItem; cùng quan hệ Thu nạp Aggregation độc lập vòng đời giữa Hotel, RoomType và PhysicalRoom, giúp dữ liệu luôn bảo đảm tính toàn vẹn tham chiếu.

### Slide 37: Biểu đồ Gói - Kiến trúc phân tầng (Package Diagram)
Biểu đồ Gói tổ chức hệ thống thành 5 tầng cấu trúc rõ rệt: Tầng giao diện người dùng, Tầng ứng dụng Application, Tầng nghiệp vụ cốt lõi Domain, Tầng hạ tầng Infrastructure và Tầng cơ sở dữ liệu. Mối quan hệ phụ thuộc một chiều từ trên xuống dưới, triệt tiêu hoàn toàn nguy cơ phụ thuộc vòng.

### Slide 38: Biểu đồ Triển khai - Mô hình vật lý 3 tầng (Deployment Diagram)
Biểu đồ Triển khai thể hiện kiến trúc 3 tầng: Máy trạm quầy lễ tân kết nối trực tiếp máy in nhiệt POS qua cáp USB và cổng mạng TCP 9100 để in hóa đơn tức thì dưới 0.5 giây kể cả khi rớt Internet hải đảo. Máy chủ trung tâm bố trí Nginx Reverse Proxy mã hóa TLS 1.3, máy chủ ứng dụng Python WSGI, tiến trình Cron Daemon dọn dẹp khóa phòng ngầm và phân vùng cơ sở dữ liệu biệt lập.

### Slide 39: Biểu đồ Thành phần - Kiến trúc tổng quát
Biểu đồ Thành phần tổng quát phân định ranh giới giữa các mô-đun phần mềm có thể thay thế độc lập: từ khối Client Executable, khối Service Controller, khối Logic nghiệp vụ đến khối Data Access Library và Engine cơ sở dữ liệu, kết nối với nhau thông qua các cổng giao tiếp Interface chuẩn mực.

### Slide 40: Biểu đồ Thành phần - Quy trình Đặt phòng & Khóa giữ chỗ
Mô-đun Đặt phòng kết nối trực tiếp với RoomInventoryComponent qua giao diện kiểm tra phòng trống và giao tiếp với PaymentGateway qua giao diện Webhook IPN, bảo đảm tiến trình đặt phòng và giữ chỗ 15 phút vận hành độc lập, không gây nghẽn hệ thống.

### Slide 41: Biểu đồ Thành phần - Quy trình Check-in & Gán phòng vật lý
Mô-đun Check-in phối hợp giữa IdentityScannerComponent để trích xuất CCCD và RoomAssignmentComponent để tra cứu trạng thái buồng phòng, cho phép gán số phòng vật lý chính xác vào từng đêm lưu trú của khách.

### Slide 42: Biểu đồ Thành phần - Quy trình Tiêu dùng dịch vụ & Folio
Mô-đun Dịch vụ tích hợp PriceCatalogComponent và FolioLedgerComponent, cho phép mọi điểm bán POS tại khách sạn đồng bộ chi phí phát sinh trực tiếp vào sổ nợ phòng của khách hàng theo thời gian thực.

### Slide 43: Biểu đồ Thành phần - Quy trình Check-out & Quyết toán
Mô-đun Check-out kết nối FolioLedgerComponent để tổng hợp công nợ, giao tiếp PaymentProcessing để thu tiền cuối kỳ, kích hoạt InvoiceGeneratorComponent xuất hóa đơn điện tử và gửi tín hiệu giải phóng phòng sang hệ thống buồng phòng.

### Slide 44: Biểu đồ Thành phần - Quy trình Buồng phòng & Giám sát
Mô-đun Buồng phòng chạy trên thiết bị di động kết nối với HousekeepingComponent và SocketEmitterComponent, bảo đảm mọi thay đổi trạng thái buồng phòng được phát sóng thời gian thực về quầy lễ tân mà không phụ thuộc vào liên lạc thủ công.

### Slide 45: Thiết kế Dữ liệu - 15 Bảng quan hệ chuẩn hóa 3NF
Slide 45 là mô hình CSDL quan hệ gồm 15 bảng đạt chuẩn hóa 3NF tuyệt đối, xóa bỏ hoàn toàn bảng khổng lồ dư thừa: Tách biệt Hạng phòng kinh doanh và Phòng vật lý thực tế; tách biệt Booking tổng và BookingNight theo từng đêm; đồng thời thiết lập bảng RoomHoldLock kiểm soát khóa phòng tạm và FolioInvoice quản lý công nợ. Toàn bộ kiến trúc dữ liệu này đã được kiểm chứng qua 43/43 kịch bản kiểm thử tự động đạt độ chính xác 100%.
