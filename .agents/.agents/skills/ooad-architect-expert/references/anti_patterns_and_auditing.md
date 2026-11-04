# Sổ Tay Kiểm Toán Kiến Trúc & Bắt Lỗi Hệ Thống (UML & OOAD Audit Manual)

Tài liệu tham khảo chuyên sâu dùng để **soi chiếu, ánh xạ vào hệ thống hiện tại** và phát hiện các điểm chưa phù hợp (Anti-Patterns), lỗi thiết kế hoặc vi phạm quy chuẩn thiết kế phần mềm hướng đối tượng.

---

## 1. Ma Trận Ánh Xạ Giữa Yêu Cầu Nghiệp Vụ Và Bản Vẽ UML

| Yêu cầu thực tế | Biểu đồ phản ánh | Dấu hiệu thiết kế ĐÚNG | Dấu hiệu thiết kế SAI |
| :--- | :--- | :--- | :--- |
| **Phân quyền người dùng** | Use Case Diagram | Kế thừa Actor (Tổng quát hóa) hoặc Actor riêng gắn đúng UC | Gom tất cả người dùng vào 1 Actor chung "Người dùng" làm tất cả |
| **Tính năng bắt buộc đi kèm** | Use Case Diagram | Quan hệ `<<include>>` trỏ từ UC chính sang UC phụ | Dùng quan hệ kết hợp thường hoặc nhầm sang `<<extend>>` |
| **Tính năng khuyến mãi / Tùy chọn** | Use Case Diagram | Quan hệ `<<extend>>` trỏ NGƯỢC từ UC mở rộng về UC chính | Mũi tên trỏ xuôi hoặc biến thành `<<include>>` |
| **Luồng xử lý nghiệp vụ nhiều bên** | Activity Diagram | Chia làn bơi (Swimlane): Khách - Hệ thống - Bên thứ 3 | Gom chung 1 làn không biết ai làm gì, hoặc vẽ làn cho bên không tham gia |
| **Toàn vẹn dữ liệu mẹ - con** | Domain Class Diagram | Quan hệ Hợp thành (Composition - Kim cương đặc $\blacklozenge$) | Dùng liên kết thường khiến con tồn tại mà mẹ bị xóa |
| **Giao dịch lưu vào CSDL** | Sequence Diagram | Mũi tên `Create Message` đâm vào đỉnh Lifeline mới ở phía dưới | Vẽ Lifeline kéo dài từ đầu kịch bản như đã có sẵn trong CSDL |
| **Kiểm tra hợp lệ / Rẽ nhánh** | Sequence Diagram | Khung `alt` chia 2 ngăn: Hợp lệ vs Thất bại | Kịch bản chạy thẳng tuột một đường, bỏ qua trường hợp lỗi |

---

## 2. Quy Trình 5 Bước "Bắt Bệnh" Một Bản Vẽ UML Có Sẵn

Khi người dùng cung cấp một bản vẽ UML (ảnh chụp hoặc mô hình), hãy quét qua 5 bước kiểm toán sau:

### Bước 1: Kiểm toán Ranh giới & Tác nhân (Actor & Boundary Audit)
* Actor có phải là đối tượng nằm NGOÀI hệ thống không? (Ví dụ: `CSDL` không bao giờ là Actor).
* Có vẽ quá nhiều Boundary trong một kịch bản Use Case không? (Chỉ nên giữ 1 Boundary đại diện cho màn hình thực hiện kịch bản chính; tránh biến sơ đồ tương tác thành sơ đồ điều hướng website).

### Bước 2: Kiểm toán Quy tắc BCE & Luồng Thông Điệp (BCE Integrity Audit)
* **Kiểm tra vi phạm "Nhảy cóc"**:
  - Có mũi tên nào từ `Boundary` đâm thẳng vào `Entity` không? $\rightarrow$ **VI PHẠM TẦNG**.
  - Có mũi tên nào từ `Entity` trả kết quả thẳng về `Boundary` mà bỏ qua `Control` không? $\rightarrow$ **VI PHẠM TẦNG**.
  - Có `Entity` nào tự gọi sang `Entity` khác không? $\rightarrow$ **VI PHẠM TRÁCH NHIỆM**.
* **Kiểm tra tính đối xứng của Call Stack**: Gọi đi bằng nét liền ($\blacktriangleright$), trả về bằng nét đứt ($\dashrightarrow$) đúng cấp độ kích hoạt (Activation box).

### Bước 3: Kiểm toán Khởi tạo Đối tượng (Object Lifecycle Audit)
* Các đối tượng phát sinh trong quá trình chạy (Đơn hàng, Hóa đơn, Giao dịch) có được kích hoạt bằng **Create Message (`<<create>>`)** không?
* Hộp Lifeline của chúng có được vẽ **tụt xuống dưới** đúng thời điểm tạo ra không?

### Bước 4: Kiểm toán Tính Khả Dụng & Kịch Bản Ngoại Lệ (Exception Handling Audit)
* Có kiểm tra tồn kho, kiểm tra số dư, kiểm tra mã voucher không?
* Nếu có kiểm tra, **đã có khung `alt` xử lý khi kiểm tra thất bại chưa**? (Bắt lỗi "Happy Path Only").

### Bước 5: Kiểm toán Tính Nhất Quán Giữa Các Mô Hình (Traceability & Consistency Audit)
* Tên các Entity trong Sequence Diagram có trùng khớp với tên các Lớp trong Domain Class Diagram không?
* Các hàm gửi cho Entity trong Sequence Diagram có phản ánh đúng thuộc tính/trách nhiệm đã định nghĩa trong Class Diagram không?
