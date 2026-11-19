### Slide 17: Biểu đồ Use Case tổng quát
Kính thưa Thầy Cô, mở đầu cho khối mô hình hóa hệ thống, Slide 17 thể hiện Biểu đồ Use Case tổng quát. Nhóm đã đóng khung toàn bộ 15 Use Case cốt lõi bên trong ranh giới hệ thống rõ ràng, phân định 5 nhóm tác nhân người dùng và 2 tác nhân ngoại vi là Cổng thanh toán VNPay cùng Máy chủ dịch vụ Cron System.

### Slide 18: Phân rã Use Case - Cổng đặt phòng B2C
Đi sâu vào phân hệ cốt lõi đầu tiên phục vụ du khách là Cổng đặt phòng B2C. Tại đây, Use Case Đặt phòng trực tuyến bắt buộc quan hệ Include với tiến trình Khóa phòng 15 phút chống trùng và Xác thực thanh toán trực tuyến. Đồng thời, khi du khách sở hữu mã giảm giá, hành vi Áp dụng voucher sẽ được kích hoạt thông qua quan hệ Extend trỏ ngược về Use Case cơ sở.

### Slide 19: Phân rã Use Case - Quản lý tài khoản & Phân quyền
Song hành cùng nghiệp vụ đặt phòng, để định danh khách hàng và kiểm soát quyền truy cập của nhân viên, phân hệ Tài khoản quản lý trọn vẹn từ Đăng ký hội viên đến Phân quyền vai trò RBAC. Hệ thống tích hợp Audit Log ghi vết bảo mật và quan hệ Extend tự động khóa tài khoản sau 5 lần đăng nhập thất bại nhằm ngăn chặn tấn công Brute-force.

### Slide 20: Phân rã Use Case - Tác nghiệp quầy tiền sảnh & Lễ tân
Khi các yêu cầu đặt phòng trực tuyến chuyển giao sang mặt đất tại quầy tiền sảnh, hệ thống đáp ứng linh hoạt cả hai đối tượng: khách đặt trước và khách vãng lai Walk-in. Lễ tân quản lý quỹ phòng trực quan trên sơ đồ Gantt thời gian thực, xử lý quyết toán Folio VAT khi Check-out và kích hoạt tự động hủy đơn No-Show đối với khách vắng mặt sau 23:59.

### Slide 21: Phân rã Use Case - Vận hành buồng phòng
Để quầy lễ tân luôn có phòng sẵn sàng đón tiếp khách, phân hệ Buồng phòng vận hành liên tục phía sau hậu trường. Nhân viên nhận ca làm việc trên thiết bị di động, cập nhật tiến độ dọn buồng và kích hoạt quan hệ Extend Báo cáo sự cố bảo trì để khóa phòng kỹ thuật ngay khi phát hiện hỏng hóc trước lúc Tổ trưởng nghiệm thu.

### Slide 22: Phân rã Use Case - Quản trị doanh thu & Báo cáo
Khép lại bức tranh chức năng, toàn bộ dữ liệu lưu trú và vận hành được tổng hợp về phân hệ Quản trị doanh thu. Tại đây, Ban Giám đốc có công cụ thiết lập biểu giá linh hoạt Dynamic Pricing theo mùa cao điểm hải đảo, ban hành chính sách hoàn cọc bậc thang và theo dõi các chỉ số KPI then chốt như RevPAR và công suất phòng theo thời gian thực.

### Slide 23: Biểu đồ Hoạt động - Đặt phòng trực tuyến (AD-01)
Nếu Use Case cho biết hệ thống làm được gì, thì Biểu đồ Hoạt động mô tả chi tiết dòng chảy nghiệp vụ xử lý ra sao. Mở đầu bằng quy trình Đặt phòng trực tuyến AD-01, hệ thống giải quyết bài toán Overbooking bằng cách tạo ngay bản ghi RoomHoldLock giữ chỗ 15 phút. Thanh phân nhánh Fork kích hoạt song song đồng hồ đếm ngược 15:00 và cổng quét VietQR; nếu thanh toán thành công phòng được xác nhận, nếu hết giờ hệ thống tự động hoàn phòng trống.

### Slide 24: Biểu đồ Hoạt động - Check-in và Gán phòng vật lý (AD-02)
Tiếp nối hành trình khi khách đặt chân đến resort sau chuyến bay hoặc tàu cao tốc, quy trình Check-in và Gán phòng AD-02 được kích hoạt. Điểm chốt chặn nghiệp vụ là điều kiện rẽ nhánh nghiêm ngặt: hệ thống chỉ cho phép lễ tân gán những phòng vật lý thỏa mãn đồng thời ba tiêu chuẩn: đúng hạng phòng kinh doanh, trạng thái buồng phòng đạt chuẩn Clean đã nghiệm thu và lịch phòng hoàn toàn Vacant.

### Slide 25: Biểu đồ Hoạt động - Dịch vụ phát sinh và Ghi nợ Folio (AD-03)
Trong suốt thời gian du khách lưu trú, mọi nhu cầu sử dụng minibar hay ẩm thực được kiểm soát qua quy trình AD-03. Hệ thống xác thực phòng đang ở trạng thái Occupied và tài khoản Folio đang mở, sau đó thực thi một giao dịch nguyên tử để ghi nhận chi tiết dịch vụ và tự động cộng dồn số dư nợ trực tiếp vào hóa đơn Folio của phòng.

### Slide 26: Biểu đồ Hoạt động - Check-out và Quyết toán công nợ (AD-04)
Đến ngày kết thúc kỳ nghỉ, dòng chảy nghiệp vụ chuyển sang quy trình Check-out và Quyết toán AD-04. Hệ thống tự động đối soát theo công thức: Số dư thanh toán bằng Tiền phòng cộng Chi phí dịch vụ trừ Tiền cọc ban đầu. Nút rẽ nhánh kiểm soát chặt chẽ điều kiện công nợ bằng 0: chỉ khi tất toán cân bằng, hóa đơn tài chính VAT Saigontourist mới được xuất và phòng lập tức chuyển sang trạng thái Dirty.

### Slide 27: Biểu đồ Hoạt động - Vận hành buồng phòng và Bảo trì (AD-05)
Ngay khi phòng chuyển sang trạng thái bẩn, quy trình Vận hành buồng phòng AD-05 lập tức khởi động để tái sinh quỹ phòng sạch. Nhân viên nhận phòng chuyển trạng thái sang Cleaning; nếu phát sinh sự cố thì rẽ nhánh khóa Maintenance, còn khi hoàn tất dọn dẹp đạt chuẩn thì chuyển sang Clean và lập tức bắn tín hiệu WebSocket thời gian thực về quầy lễ tân để sơ đồ phòng đổi sang màu xanh đón khách mới.

### Slide 28: Biểu đồ Tuần tự - Giới thiệu mô hình kiến trúc BCE
Để hiện thực hóa các luồng hoạt động trên ở tầng mã nguồn, Slide 28 mở đầu cho khối Biểu đồ Tuần tự. Toàn bộ 6 quy trình nghiệp vụ then chốt được thiết kế theo đúng mẫu hình phân tầng Boundary - Control - Entity, tuân thủ nguyên tắc bao đóng: lớp Boundary tiếp nhận tương tác giao diện nhưng không bao giờ truy cập trực tiếp vào Entity mà phải ủy quyền cho Control điều phối logic nghiệp vụ.

### Slide 29: Biểu đồ Tuần tự - Đặt phòng trực tuyến & Khóa 15m (SD-01)
Hiện thực hóa trực tiếp quy trình đặt phòng, biểu đồ tuần tự SD-01 mô tả chi tiết 17 thông điệp tương tác. Lớp BookingService điều phối RoomInventory tạo khóa tạm CreateHoldLock 15 phút trong một DB Transaction an toàn. Khi nhận Webhook IPN từ cổng VNPay, BookingService khởi tạo thực thể Booking Confirmed, sinh các bản ghi BookingNights và gọi hàm MarkLockAsSold để chốt giữ phòng thành công.

### Slide 30: Biểu đồ Tuần tự - Làm thủ tục nhận phòng Check-in (SD-02)
Tiếp nối thời điểm khách đến quầy, biểu đồ SD-02 chi tiết hóa 16 thông điệp của thủ tục Check-in. Lễ tân tra cứu mã PNR, quét thông tin CCCD lưu vào GuestProfile; Control gọi PhysicalRoom lọc danh sách phòng sạch CheckCleanRooms, sau đó thực thi hàm AssignPhysicalRoom để gán phòng cụ thể cho từng đêm lưu trú và cập nhật trạng thái phòng sang Occupied.

### Slide 31: Biểu đồ Tuần tự - Ghi nhận tiêu dùng dịch vụ (SD-03)
Khi khách phát sinh chi tiêu trong kỳ nghỉ, biểu đồ SD-03 thể hiện 12 thông điệp ghi nợ. FolioBillingService xác thực phòng đang lưu trú hợp lệ, truy vấn đơn giá có thuế từ PriceCatalog, lưu chi tiết tiêu dùng vào FolioItem và kích hoạt hàm PostChargeToFolio để cộng dồn khoản nợ vào số dư của hóa đơn phòng.

### Slide 32: Biểu đồ Tuần tự - Trả phòng và Quyết toán (SD-04)
Đến bước thanh toán ra về, biểu đồ SD-04 điều phối 16 thông điệp tất toán công nợ. Lễ tân nạp phụ thu phát sinh, hệ thống tính toán số dư cuối kỳ và thực thu phần tiền còn thiếu. Ngay khi tất toán, Control khởi tạo hóa đơn Invoice với thuế suất VAT 8% theo mã số thuế Saigontourist và gửi thông điệp cập nhật trạng thái phòng sang Dirty.

### Slide 33: Biểu đồ Tuần tự - Vận hành dọn dẹp buồng phòng (SD-05)
Song song với việc phòng chuyển bẩn sau Check-out, biểu đồ SD-05 mô tả 21 thông điệp vận hành buồng phòng di động. Nhân viên nhận việc cập nhật trạng thái Cleaning và khởi tạo CleaningLog để tính định mức thời gian; khi dọn xong, hệ thống đổi phòng sang Clean và phát sự kiện WebSocket NotifyRoomStatus cập nhật tức thời lên màn hình quầy lễ tân.

### Slide 34: Biểu đồ Tuần tự - Hủy đặt phòng và Hoàn cọc (SD-06)
Bên cạnh chu trình lưu trú thuận lợi, hệ thống xử lý tình huống ngoại lệ bằng biểu đồ SD-06 Hủy đặt phòng và Hoàn cọc. BookingCancellationService gọi RefundPolicy tính khoảng cách giờ đến thời điểm Check-in để áp mức hoàn cọc 100%, 50% hoặc 0%, ghi nhận chứng từ hoàn tiền âm vào sổ quỹ và lập tức gọi ReleaseBookedNights để trả lại phòng trống cho thị trường.

### Slide 35: Biểu đồ Lớp Lĩnh vực - Khái quát cấu trúc tĩnh
Từ các thực thể tham gia tương tác trong chuỗi biểu đồ tuần tự, Slide 35 chuyển sang bức tranh cấu trúc tĩnh của hệ thống qua Biểu đồ Lớp Lĩnh vực. Toàn bộ các thực thể đại diện cho miền nghiệp vụ khách sạn biển đảo được định danh đầy đủ, bao quát từ đặt phòng, buồng phòng, lưu trú, dịch vụ đến thanh toán và chính sách giá.

### Slide 36: Biểu đồ Lớp Lĩnh vực - Chi tiết thuộc tính, phương thức và quan hệ
Đi sâu vào bản vẽ chi tiết ở Slide 36, cấu trúc lớp được thiết kế 3 ngăn chuẩn mực theo nguyên lý Information Expert. Điểm mấu chốt là mối quan hệ Hợp thành Composition ràng buộc sinh tử giữa BookingMaster và BookingNight, giữa ServiceFolio và FolioItem; cùng quan hệ Thu nạp Aggregation độc lập vòng đời giữa Hotel, RoomType và PhysicalRoom, bảo đảm tính toàn vẹn dữ liệu ở cấp độ mã nguồn.

### Slide 37: Biểu đồ Gói - Kiến trúc phân tầng (Package Diagram)
Để các lớp nghiệp vụ này được tổ chức khoa học và không bị phụ thuộc chồng chéo, Biểu đồ Gói ở Slide 37 phân chia toàn bộ mã nguồn thành 5 tầng kiến trúc rõ rệt: Tầng giao diện người dùng, Tầng ứng dụng Application, Tầng nghiệp vụ cốt lõi Domain, Tầng hạ tầng Infrastructure và Tầng cơ sở dữ liệu. Mối quan hệ phụ thuộc một chiều từ trên xuống dưới, triệt tiêu hoàn toàn nguy cơ phụ thuộc vòng.

### Slide 38: Biểu đồ Triển khai - Mô hình vật lý 3 tầng (Deployment Diagram)
Toàn bộ các gói phần mềm trên được đưa vào môi trường vận hành vật lý qua Biểu đồ Triển khai ở Slide 38. Kiến trúc 3 tầng phân định rõ: Máy trạm lễ tân kết nối máy in nhiệt POS qua cổng USB và TCP 9100 để in hóa đơn tức thì dưới 0.5 giây kể cả khi rớt mạng biển đảo; Máy chủ trung tâm chạy Nginx Reverse Proxy mã hóa TLS 1.3, máy chủ ứng dụng Python WSGI, tiến trình Cron Daemon ngầm dọn phòng quá hạn; và Phân vùng cơ sở dữ liệu an toàn riêng biệt.

### Slide 39: Biểu đồ Thành phần - Kiến trúc tổng quát
Bên trong máy chủ ứng dụng đó, Biểu đồ Thành phần tổng quát ở Slide 39 phân rã hệ thống thành các khối thực thi độc lập có thể nâng cấp và thay thế được: từ khối Client Executable, khối Service Controller, khối Logic nghiệp vụ đến khối Data Access Library và Engine cơ sở dữ liệu, kết nối với nhau thông qua các cổng giao diện Interface chuẩn mực.

### Slide 40: Biểu đồ Thành phần - Quy trình Đặt phòng & Khóa giữ chỗ
Cụ thể hóa thành phần cho từng quy trình nghiệp vụ, Slide 40 thể hiện mô-đun Đặt phòng kết nối trực tiếp với RoomInventoryComponent qua giao diện kiểm tra phòng trống và giao tiếp với PaymentGateway qua giao diện Webhook IPN, bảo đảm tiến trình đặt phòng và giữ chỗ 15 phút vận hành độc lập, không gây nghẽn hệ thống.

### Slide 41: Biểu đồ Thành phần - Quy trình Check-in & Gán phòng vật lý
Tiếp nối tại quy trình Nhận phòng ở Slide 41, mô-đun Check-in phối hợp giữa IdentityScannerComponent để trích xuất CCCD và RoomAssignmentComponent để tra cứu trạng thái buồng phòng, cho phép gán số phòng vật lý chính xác vào từng đêm lưu trú của khách.

### Slide 42: Biểu đồ Thành phần - Quy trình Tiêu dùng dịch vụ & Folio
Đối với quy trình Dịch vụ tại Slide 42, mô-đun tích hợp PriceCatalogComponent và FolioLedgerComponent, cho phép mọi điểm bán POS tại nhà hàng, quầy bar đồng bộ chi phí phát sinh trực tiếp vào sổ nợ phòng của khách hàng theo thời gian thực.

### Slide 43: Biểu đồ Thành phần - Quy trình Check-out & Quyết toán
Tại quy trình Trả phòng ở Slide 43, mô-đun Check-out kết nối FolioLedgerComponent để tổng hợp công nợ, giao tiếp PaymentProcessing để thu tiền cuối kỳ, kích hoạt InvoiceGeneratorComponent xuất hóa đơn điện tử và gửi tín hiệu giải phóng phòng sang hệ thống buồng phòng.

### Slide 44: Biểu đồ Thành phần - Quy trình Buồng phòng & Giám sát
Và khép lại khối thành phần ở quy trình Buồng phòng Slide 44, mô-đun chạy trên thiết bị di động kết nối với HousekeepingComponent và SocketEmitterComponent, bảo đảm mọi thay đổi trạng thái buồng phòng được phát sóng thời gian thực về quầy lễ tân mà không phụ thuộc vào liên lạc thủ công.

### Slide 45: Thiết kế Dữ liệu - 15 Bảng quan hệ chuẩn hóa 3NF
Cuối cùng, làm nền tảng lưu trữ bền vững cho toàn bộ các biểu đồ trên là Thiết kế Cơ sở dữ liệu 15 bảng đạt chuẩn hóa 3NF tuyệt đối ở Slide 45. Nhóm đã xóa bỏ hoàn toàn bảng khổng lồ dư thừa: tách biệt Hạng phòng kinh doanh và Phòng vật lý thực tế; tách biệt Booking tổng và BookingNight theo từng đêm; đồng thời thiết lập bảng RoomHoldLock kiểm soát khóa tạm và FolioInvoice quản lý công nợ. Toàn bộ kiến trúc dữ liệu này đã được kiểm chứng qua 43/43 kịch bản kiểm thử tự động đạt độ chính xác 100%.
