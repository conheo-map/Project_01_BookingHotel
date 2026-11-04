---
name: system-audit-refactor
description: >-
  Quy trình kiểm toán, tái cấu trúc (Reverse Engineering & Architectural Refactoring) và chuẩn hóa một hệ thống web/phần mềm có sẵn thành bộ hồ sơ Phân tích & Thiết kế Hệ thống Hướng đối tượng (OOAD) hoàn chỉnh. Kích hoạt skill này khi người dùng muốn rà soát một dự án web cũ (mã nguồn, database, tính năng), bóc tách các lỗi cấu trúc (anti-patterns, quan hệ sai, dư thừa dữ liệu) và hoàn thiện 6 sản phẩm bàn giao đồ án: Use Case, Activity, Sequence BCE, Class Diagram, UI Design, và ERD/Database.
---

# Quy Trình Kiểm Toán, Tái Thiết Kế & Hoàn Thiện Hồ Sơ Đồ Án PTTKHT

Tài liệu này hướng dẫn AI Agent tiếp nhận một dự án web thực tế đã xây dựng từ trước (thường chưa chuẩn hóa, thiếu tính nhất quán hoặc cấu trúc CSDL chắp vá), thực hiện quy trình **Kỹ nghệ đảo ngược (Reverse Engineering)** để kiểm toán lỗi, tái cấu trúc chuẩn chuyên môn và xuất bản đầy đủ 6 tài liệu thiết kế của môn học.

---

## 1. Khung Làm Việc 3 Giai Đoạn (The 3-Phase Framework)

```text
  [Dự án Web cũ: Code / DB / UI / Mô tả]
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: KIỂM TOÁN HỆ THỐNG & "BẮT BỆNH" CẤU TRÚC   │
│ - Bóc tách danh mục tính năng hiện tại                 │
│ - Rà soát CSDL (Normalization 3NF, Khóa ngoại, Bảng)   │
│ - Đối chiếu luồng nghiệp vụ thực tế vs Logic chuẩn     │
│ - Xuất Bảng chẩn đoán lỗi kiến trúc & rủi ro           │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: TÁI CẤU TRÚC HỆ THỐNG CHUẨN HÓA (REFACTOR) │
│ - Tinh chỉnh quy tắc nghiệp vụ (Business Rules)        │
│ - Tái thiết kế lược đồ CSDL chuẩn hóa (Target Schema)  │
│ - Ánh xạ các thành phần Web cũ sang mô hình BCE        │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 3: SẢN XUẤT 6 SẢN PHẨM BÀN GIAO ĐỒ ÁN        │
│ 1. Use Case tổng quát & Phân rã                        │
│ 2. Biểu đồ Hoạt động (Activity Diagrams - Swimlanes)   │
│ 3. Biểu đồ Tuần tự (BCE Sequence Diagrams)             │
│ 4. Biểu đồ Lớp lĩnh vực & Thiết kế (Class Diagrams)    │
│ 5. Đặc tả Thiết kế Giao diện (UI Mockups & Boundary)   │
│ 6. Biểu đồ ERD & Lược đồ Cơ sở Dữ liệu quan hệ 3NF     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Giai Đoạn 1: Tiêu Chí Kiểm Toán "Bắt Bệnh" Hệ Thống Web Cũ

Khi nhận thông tin về website cũ (danh sách trang, bảng CSDL, API hoặc code), AI phải rà soát qua 4 chiều:

### 2.1. Kiểm Toán Cấu Trúc Cơ Sở Dữ Liệu & ERD
1. **Lỗi Vi phạm Chuẩn hóa (Unnormalized Schema)**:
   * Thuộc tính đa trị (Multi-valued): Lưu nhiều ID hoặc chuỗi JSON/danh sách phân tách bằng dấu phẩy trong 1 cột (ví dụ: cột `danh_sach_san_pham: "1,2,5"` trong bảng `DonHang` $\rightarrow$ Vi phạm 1NF).
   * Phụ thuộc một phần (Partial Dependency): Bảng có khóa chính phức hợp nhưng có cột chỉ phụ thuộc vào một nửa khóa (Vi phạm 2NF).
   * Phụ thuộc bắc cầu (Transitive Dependency): Bảng `DonHang` lưu cả `ten_khach_hang`, `dia_chi`, `so_dien_thoai` thay vì chỉ lưu `ma_khach_hang` (Vi phạm 3NF).
2. **Lỗi Quan Hệ & Khóa Ngoại (Foreign Key Defects)**:
   * Bảng quan hệ N - N (Many-to-Many) nhưng không có bảng trung gian (Junction/Associative Table).
   * Thiếu toàn vẹn tham chiếu (Foreign Keys bị thả nổi, xóa cha không xử lý con).
3. **Lỗi Vòng Đời & Trạng Thái Dữ Liệu**:
   * Thiếu trường quản lý trạng thái (`trang_thai: ChoXacNhan, DaThanhToan, DaHuy`) dẫn đến không thể truy vết kịch bản nghiệp vụ.

### 2.2. Kiểm Toán Luồng Nghiệp Vụ & Quy Trình
1. **Lỗ Hổng Logic Nghiệp Vụ (Business Logic Gaps)**:
   * Bỏ qua bước kiểm tra điều kiện tiên quyết (ví dụ: Cho phép đặt hàng khi kho = 0; cho phép đặt phòng khi lịch đã bị trùng).
   * Thiếu quy trình xử lý ngoại lệ: Giao dịch thất bại thì hoàn tiền/hủy trạng thái thế nào?
2. **Nhập Nhằng Quyền Hạn (Authorization & Actor Boundary)**:
   * Không phân định rõ hành động nào của Khách vãng lai, Khách đăng nhập, Nhân viên hay Admin.

---

## 3. Giai Đoạn 2: Ánh Xạ Kỹ Nghệ Đảo Ngược Sang Kiến Trúc Chuẩn

Chuyển đổi các thành phần của web cũ sang các thành phần mô hình hóa chuẩn:

| Thành phần Website cũ | Thành phần Phân tích Thiết kế tương ứng | Vai trò trong hồ sơ đồ án |
| :--- | :--- | :--- |
| **Giao diện HTML/React/Vue/Blade/JSP** | **Boundary Class (`├○`)** & UI Design | Màn hình tiếp nhận sự kiện và hiển thị kết quả cho Actor |
| **Routes / Controller / Service / Middleware** | **Control Class (`↻○`)** | Bộ não điều khiển, xác thực logic và điều phối luồng dữ liệu |
| **Models (ORM) / Database Tables** | **Entity Class (`⊖`)** & Domain Class | Nơi lưu trữ trạng thái dữ liệu và các thao tác nghiệp vụ nội tại |
| **Các nút bấm Submit / Gọi API** | **Thông điệp (Messages) / Actions** | Lời gọi hàm trên Sequence Diagram và bước luồng trên Activity Diagram |

---

## 4. Giai Đoạn 3: Chuẩn Mực Cho 6 Sản Phẩm Bàn Giao Đồ Án

### Sản Phẩm 1: Biểu Đồ Use Case Tổng Quát & Phân Rã
* **Use Case Tổng quát**: Bao quát toàn bộ ranh giới hệ thống, nhóm các Use Case theo các Actor chính (Khách hàng, Quản trị viên, Nhân viên...).
* **Use Case Phân rã**: Đi sâu vào các phân hệ phức tạp (ví dụ: Đặt hàng, Quản lý kho, Thanh toán), làm rõ các mối quan hệ `<<include>>` (bắt buộc) và `<<extend>>` (tùy chọn có điều kiện, mũi tên trỏ ngược).

### Sản Phẩm 2: Biểu Đồ Hoạt Động (Activity Diagram)
* Mỗi Use Case trọng tâm phải có một Biểu đồ Hoạt động tương ứng.
* Bắt buộc chia tối thiểu 2 đến 3 làn bơi (Swimlane): `[Người dùng]` | `[Hệ thống]` | `[Bên thứ 3]`.
* Thể hiện đầy đủ điểm bắt đầu ($\bullet$), điểm kết thúc ($\circledcirc$), rẽ nhánh điều kiện (Decision/Merge) và luồng xử lý song song (Fork/Join).

### Sản Phẩm 3: Biểu Đồ Trình Tự (BCE Sequence Diagram)
* Áp dụng nghiêm ngặt mô hình 3 tầng: **Boundary $\longleftrightarrow$ Control $\longleftrightarrow$ Entity**.
* Tuyệt đối **không nhảy cóc tầng** (Boundary không gọi thẳng Entity; Entity không tự gọi nhau).
* Bản ghi mới sinh ra trong giao dịch phải dùng **Create Message (`<<create>>`)** đâm vào đỉnh Lifeline mới ở phía dưới.
* Có khung kết hợp `alt` để rẽ nhánh xử lý trường hợp thành công và thất bại.

### Sản Phẩm 4: Biểu Đồ Lớp (Domain Class & Design Class Diagram)
* Thể hiện rõ tên lớp, thuộc tính (kèm kiểu dữ liệu), và thao tác nghiệp vụ.
* Xác định chính xác 7 loại mối quan hệ và ghi đầy đủ bản số (Multiplicity: `1`, `0..1`, `1..*`, `0..*`) ở cả 2 đầu liên kết.
* Tuyệt đối không để bản số `0` đứng độc lập. Không đưa các hàm kỹ thuật kết nối CSDL hạ tầng vào lớp lĩnh vực.

### Sản Phẩm 5: Thiết Kế Giao Diện (UI Mockups & Boundary Specifications)
* Thiết kế phác thảo wireframe/mockup cho các màn hình then chốt.
* Lập bảng mô tả ánh xạ các thành phần giao diện (Button, Input, Table) với các sự kiện kích hoạt gửi tới tầng Control.

### Sản Phẩm 6: Biểu Đồ ERD & Lược Đồ Cơ Sở Dữ Liệu Quan Hệ
* Biểu đồ ERD thể hiện các thực thể, thuộc tính khóa chính (PK), khóa ngoại (FK) và mối quan hệ.
* Lược đồ CSDL quan hệ đạt chuẩn chuẩn hóa **3NF (Third Normal Form)**, loại bỏ triệt để dị thường thêm/xóa/sửa (Anomalies) của web cũ.
* Bảng từ điển dữ liệu (Data Dictionary): Ghi rõ tên cột, kiểu dữ liệu, kích thước, ràng buộc Null/Unique/Default và mô tả ý nghĩa.
