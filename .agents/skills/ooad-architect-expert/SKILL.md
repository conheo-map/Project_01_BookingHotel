---
name: ooad-architect-expert
description: >-
  Master Skill toàn diện về Phân tích & Thiết kế Hệ thống Hướng đối tượng (OOAD), quy chuẩn nghiệp vụ theo giáo trình bài giảng chuẩn NEU/Lead Architect và kỹ thuật dựng biểu đồ tương thích 100% với Diagrams.net (Draw.io XML). Áp dụng cho toàn bộ 6 sản phẩm đồ án: Use Case, Activity, Sequence BCE, Class Diagram, UI Design và ERD 3NF.
---

# Master Skill: Phân Tích Thiết Kế Hệ Thống & Chuẩn Hóa Biểu Đồ Diagrams.net (Draw.io)

Tài liệu này là **kim chỉ nam tối cao và duy nhất**, tích hợp toàn bộ tri thức nghiệp vụ hướng đối tượng (OOAD) từ slide bài giảng chuẩn mực và bộ quy chuẩn hình thức hiển thị bằng kho ký hiệu UML của Diagrams.net (Draw.io).

---

## PHẦN 1: BỘ NGUYÊN TẮC NGHIỆP VỤ HỌC THUẬT (TỪ SLIDE BÀI GIẢNG)

### 1.1. Bóc Tách Ngữ Pháp Miền Bài Toán (Domain Linguistic Mapping)
Trước khi dựng biểu đồ, bắt buộc phải ánh xạ các thành phần ngôn ngữ tự nhiên:
* **Danh từ chủ động** $\longrightarrow$ `Actor` (Nằm ngoài ranh giới hệ thống, đại diện cho tác nhân có mục tiêu).
* **Danh từ đối tượng dữ liệu** $\longrightarrow$ `Class` (Lớp lĩnh vực) / `Entity` (Thực thể BCE) / `Table` (ERD).
* **Danh từ đặc trưng** $\longrightarrow$ `Attribute` (Thuộc tính của lớp/bảng).
* **Động từ mục tiêu người dùng** $\longrightarrow$ `Use Case` (Chức năng nghiệp vụ mang lại giá trị hoàn chỉnh).
* **Động từ thao tác con** $\longrightarrow$ `Action` (trên Activity) / `Method` (trên Sequence & Class). Cấm biến thao tác tay (click, gõ phím, chọn dòng) thành Use Case riêng lẻ.
* **Điều kiện / Giới hạn** $\longrightarrow$ `Multiplicity` (Bản số) / `Guard Condition` (Điều kiện rẽ nhánh `[Alt]`).

### 1.2. Quy Chuẩn Nghiệp Vụ Từng Biểu Đồ

#### A. Biểu đồ Use Case (Tổng quát & Phân rã):
* **Ranh giới hệ thống (System Boundary)**: Bắt buộc đóng khung bao trọn các Use Case. Actor nằm ngoài.
* **Quan hệ `<<include>>` (Bắt buộc)**: Luôn thực thi khi Use Case gốc chạy. Mũi tên nét đứt trỏ **THUẬN** từ Use Case gốc sang Use Case được bao hàm.
* **Quan hệ `<<extend>>` (Tùy chọn có điều kiện)**: Chỉ chạy khi thỏa mãn điều kiện tại Extension Point (ví dụ: áp mã giảm giá, hủy phòng). Mũi tên nét đứt trỏ **NGƯỢC** từ Use Case mở rộng về Use Case gốc.
* **Kế thừa Actor (Generalization)**: Dùng tam giác rỗng trỏ từ vai trò chuyên biệt về vai trò cha (Ví dụ: `Khách hàng chưa đăng nhập` và `Khách hàng đã đăng nhập` $\longrightarrow$ `Khách hàng`).

#### B. Biểu đồ Hoạt động (Activity Diagram):
* **Phân làn Swimlane**: Chia tối thiểu 2-3 làn bơi theo đúng các chủ thể tham gia trực tiếp (`Người dùng` | `Hệ thống` | `Bên thứ ba/Cổng thanh toán`). Tuyệt đối không tạo làn cho tác nhân thụ động không tương tác.
* **Đồng bộ dòng chảy**: Rẽ nhánh dùng hình thoi `Decision/Merge` có điều kiện bảo vệ `[Guard]`. Xử lý song song dùng thanh đậm `Fork/Join`.

#### C. Biểu đồ Lớp Lĩnh Vực (Domain Class Diagram):
* **Cấu trúc 3 ngăn**: Tên lớp $\rightarrow$ Thuộc tính $\rightarrow$ Thao tác.
* **Ngăn Thao tác (Methods)**: Chỉ ghi các thao tác nghiệp vụ thuần túy theo nguyên lý *Information Expert* (`tinhTongTien()`, `kiemTraPhongTrong()`) hoặc để trống ở mức thuần khái niệm. **Cấm tuyệt đối** rò rỉ mã hạ tầng CSDL (`connectDB`, `saveSQL`, `renderUI`) hay `get/set` vụn vặt.
* **7 Loại Liên Kết & Bản Số**:
  - Hợp thành (Composition $\blacklozenge$): Toàn thể - bộ phận ràng buộc sinh tử (Đơn đặt phòng $\blacklozenge\longrightarrow$ Chi tiết đêm).
  - Thu nạp (Aggregation $\diamondsuit$): Toàn thể - bộ phận độc lập vòng đời (Khách sạn $\diamondsuit\longrightarrow$ Loại phòng).
  - Kế thừa (Generalization $\longrightarrow\!\!\triangleright$): Lớp cha - lớp con (`Account` $\longrightarrow$ `CustomerAccount`).
  - Bản số: Ghi rõ ở 2 đầu liên kết (`1`, `0..1`, `1..*`, `0..*`). Cấm bản số `0` đứng độc lập.

#### D. Biểu đồ Tuần Tự (Sequence Diagram theo mô hình BCE):
* **Cấu trúc 3 tầng BCE**: `Actor` $\longleftrightarrow$ `Boundary` ($\vdash\bigcirc$) $\longleftrightarrow$ `Control` ($\circlearrowleft$) $\longleftrightarrow$ `Entity` ($\ominus$).
* **Quy tắc CẤM NHẢY CÓC (Strict Layer Separation)**:
  - Boundary **không được** gọi thẳng vào Entity.
  - Entity **không được** tự gọi nhau hoặc trả data thẳng về Boundary mà không qua Control.
* **Tính đối xứng Call-Stack**: Gọi đi bằng nét liền ($\blacktriangleright$), trả về bằng nét đứt ($\dashrightarrow$) đúng cấp độ vạch kích hoạt.
* **Vòng đời đối tượng**: Bản ghi mới sinh ra (Đơn hàng, Hóa đơn) phải dùng **Create Message (`<<create>>`)** đâm vào đỉnh Lifeline mới vẽ tụt xuống dưới.
* **Khung kết hợp `Alt`**: Bắt buộc có khung `Alt` chia 2 nhánh `[Hợp lệ]` và `[Thất bại / Hết hàng / Hết hạn]`.

---

## PHẦN 2: CHUẨN MỰC HÌNH THỨC TRÊN DIAGRAMS.NET (DRAW.IO)

### 2.1. Phông Chữ & Cỡ Chữ Thống Nhất (Typography Hierarchy)
Toàn bộ biểu đồ sử dụng font không chân Unicode sạch sẽ (`Arial`, `Helvetica`, `Segoe UI`):
* **Tiêu đề biểu đồ (Góc trên bên trái)**: `fontSize=16;fontStyle=1;fontColor=#000000;` (VIẾT HOA BÔI ĐẬM, ví dụ: `ĐẶT PHÒNG`, `USE CASE TỔNG QUÁT`).
* **Tên Ranh giới hệ thống / Khung Alt**: `fontSize=13;fontStyle=1;fontColor=#1E293B;`.
* **Tên Actor**: `fontSize=11;fontStyle=1;fontColor=#000000;` (VIẾT HOA BÔI ĐẬM, đặt dưới chân hình que).
* **Tên Use Case (Elip)**: `fontSize=11;fontStyle=1;fontColor=#000000;whiteSpace=wrap;` (VIẾT HOA TOÀN BỘ, căn giữa 2 chiều, tự ngắt dòng).
* **Tên Lifeline (BCE)**: `fontSize=11;fontStyle=1;fontColor=#000000;` (Ghi rõ tiền tố: `UI_...`, `CTL_...`, `En_...`).
* **Tên Thông Điệp (Message)**: `fontSize=10;fontStyle=0;fontColor=#000000;` (Nằm trên mũi tên, không đè vạch kích hoạt).
* **Nhãn `<<include>>` / `<<extend>>`**: `fontSize=10;fontStyle=1;` (Đóng hộp Badge nổi bật đè lên đường nét đứt).
* **Điều Kiện Bảo Vệ**: `fontSize=10;fontStyle=2;fontColor=#334155;` (Đặt trong ngoặc vuông `[Điều kiện]`).

---

### 2.2. Kho Ký Hiệu Native UML Trên Draw.io (Tra Cứu Mã Shape)

#### A. Ký Hiệu Use Case:
```xml
<!-- Ranh giới hệ thống -->
style="shape=rect;fillColor=none;strokeColor=#475569;strokeWidth=1.5;rounded=0;verticalAlign=top;fontStyle=1;fontSize=13;"
<!-- Actor hình que -->
style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=none;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;"
<!-- Use Case elip -->
style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontColor=#000000;fontStyle=1;fontSize=11;"
<!-- Mũi tên <<include>> trỏ xuôi có badge -->
style="edgeStyle=orthogonalEdgeStyle;dashed=1;endArrow=open;endSize=8;strokeColor=#000000;strokeWidth=1.2;fontSize=10;fontStyle=1;" value="&lt;&lt;include&gt;&gt;"
<!-- Mũi tên <<extend>> trỏ ngược có badge -->
style="edgeStyle=orthogonalEdgeStyle;dashed=1;endArrow=open;endSize=8;strokeColor=#000000;strokeWidth=1.2;fontSize=10;fontStyle=1;" value="&lt;&lt;extend&gt;&gt;"
```

#### B. Ký Hiệu Sequence Diagram BCE & VẠCH KÍCH HOẠT:
```xml
<!-- Stereotype Boundary (Hình tròn thanh dọc trái) -->
style="shape=umlBoundary;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=#FFF2CC;strokeColor=#D6B656;strokeWidth=1.5;fontSize=11;fontStyle=1;"
<!-- Stereotype Control (Hình tròn mũi tên xoay đỉnh) -->
style="shape=umlControl;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=#FFF2CC;strokeColor=#D6B656;strokeWidth=1.5;fontSize=11;fontStyle=1;"
<!-- Stereotype Entity (Hình tròn thanh ngang chân) -->
style="shape=umlEntity;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=#FFF2CC;strokeColor=#D6B656;strokeWidth=1.5;fontSize=11;fontStyle=1;"

<!-- VẠCH KÍCH HOẠT BẮT BUỘC (ACTIVATION BAR) - Rộng 12px, trắng viền đen -->
style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.2;"

<!-- Mũi tên gọi đồng bộ (Sync Call): Cắm vào mép TRÁI vạch kích hoạt -->
style="endArrow=block;endFill=1;html=1;strokeColor=#000000;strokeWidth=1.2;fontSize=10;"
<!-- Mũi tên trả về (Return): Xuất phát từ mép PHẢI vạch kích hoạt -->
style="endArrow=open;dashed=1;endFill=0;html=1;strokeColor=#000000;strokeWidth=1.2;fontSize=10;"
<!-- Khung Alt Combined Fragment -->
style="shape=umlFrame;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#2563EB;strokeWidth=1.5;width=60;height=26;fontSize=11;fontStyle=1;" value="Alt"
```

#### C. Ký Hiệu Biểu Đồ Lớp (Class Diagram):
```xml
<!-- Khối lớp 3 ngăn chuẩn Draw.io -->
style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontSize=12;"
<!-- Hợp thành (Composition): Kim cương đen đặc -->
style="endArrow=diamond;endFill=1;strokeColor=#000000;strokeWidth=1.5;"
<!-- Thu nạp (Aggregation): Kim cương trắng rỗng -->
style="endArrow=diamond;endFill=0;strokeColor=#000000;strokeWidth=1.5;"
<!-- Kế thừa (Generalization): Tam giác trắng rỗng -->
style="endArrow=block;endFill=0;strokeColor=#000000;strokeWidth=1.5;"
```

#### D. Ký Hiệu Biểu Đồ Hoạt Động (Activity Diagram):
```xml
<!-- Làn bơi Swimlane -->
style="swimlane;startSize=30;horizontal=1;fillColor=#F8FAFC;strokeColor=#334155;strokeWidth=1.5;fontStyle=1;fontSize=12;"
<!-- Điểm bắt đầu (Hình tròn đen đặc 24x24) -->
style="ellipse;fillColor=#000000;strokeColor=none;"
<!-- Điểm kết thúc (Mắt bò 26x26) -->
style="ellipse;shape=doubleEllipse;fillColor=#000000;strokeColor=#FFFFFF;strokeWidth=3;"
<!-- Hành động bo góc -->
style="rounded=1;arcSize=25;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontSize=11;"
<!-- Rẽ nhánh Decision (Hình thoi) -->
style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontSize=10;"
<!-- Thanh đồng bộ Fork/Join (Thanh đen đặc cao 6px) -->
style="shape=rect;fillColor=#000000;strokeColor=none;rounded=0;"
```

#### E. Ký Hiệu Biểu Đồ ERD (CSDL 3NF):
```xml
<!-- Bảng thực thể -->
style="shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;html=1;fillColor=#F8FAFC;strokeColor=#000000;strokeWidth=1.5;"
<!-- Khóa chính (PK): Gạch chân, màu đỏ -->
style="shape=partialRectangle;collapsible=0;dropTarget=0;pointerEvents=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;fontStyle=5;fontColor=#B91C1C;fontSize=11;"
<!-- Khóa ngoại (FK): Nghiêng, màu xanh dương -->
style="shape=partialRectangle;collapsible=0;dropTarget=0;pointerEvents=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;fontStyle=4;fontColor=#1D4ED8;fontSize=11;"
```

---

## PHẦN 3: MA TRẬN BẮT LỖI HÌNH THỨC & KIẾN TRÚC (ANTI-PATTERNS AUDIT)

Bất kỳ biểu đồ nào trước khi xuất bản đều phải quét qua 10 chốt kiểm tra nghiêm ngặt:

| Mã lỗi | Tên Lỗi | Hành vi vi phạm thực tế | Cách xử lý chuẩn hóa |
| :---: | :--- | :--- | :--- |
| **AP-01** | **Missing Activation** | Mũi tên Sequence đâm thẳng vào nét đứt Lifeline không có vạch kích hoạt | **BẮT BUỘC chèn Vạch kích hoạt chữ nhật đứng 12px** |
| **AP-02** | **BCE Leapfrogging** | Boundary gọi thẳng vào Entity, hoặc Entity trả data thẳng về Boundary | Chèn Controller vào giữa làm trung gian điều phối |
| **AP-03** | **Reversed Extend** | Mũi tên `<<extend>>` trỏ xuôi từ UC gốc sang UC mở rộng | Đảo chiều: trỏ NGƯỢC từ UC mở rộng về UC gốc |
| **AP-04** | **Micro-action as UC** | Vẽ "Bấm nút", "Nhập SĐT", "Đăng nhập" thành Use Case nghiệp vụ lớn | Gom vào bước con của kịch bản đặc tả Use Case |
| **AP-05** | **Zombie Lifeline** | Đơn hàng mới sinh ra nhưng Lifeline lại vẽ kéo dài từ đầu kịch bản | Dùng Create Message (`<<create>>`) đâm vào đỉnh Lifeline tụt xuống |
| **AP-06** | **Happy-Path Only** | Sequence kiểm tra điều kiện nhưng không có khung `Alt` xử lý lỗi | Bổ sung khung `Alt` chia 2 nhánh: Hợp lệ vs Thất bại |
| **AP-07** | **Passive Swimlane** | Làn bơi được tạo ra nhưng không chứa bất kỳ hành động nào | Xóa bỏ làn bơi thừa, chỉ giữ các thực thể có tương tác thực tế |
| **AP-08** | **Tech-leaked Class** | Lớp lĩnh vực chứa hàm SQL, ORM, HTTP connection, render | Loại bỏ toàn bộ hàm kỹ thuật, chỉ giữ hàm nghiệp vụ nội tại |
| **AP-09** | **Solitary Zero** | Đầu mối liên kết ghi bản số `0` đứng một mình | Chuyển thành `0..1` (tùy chọn) hoặc `0..*` (danh sách có thể rỗng) |
| **AP-10** | **Typography Chaos** | Dùng lẫn lộn font chữ hoa/thường, font size không đồng nhất | Chuẩn hóa theo Typography Hierarchy ở Mục 2.1 |

---

## PHẦN 4: QUY TRÌNH XUẤT BẢN FILE BẮT BUỘC

Mỗi khi người dùng yêu cầu vẽ biểu đồ, AI Agent bắt buộc phải xuất bản:
1. **File vật lý `.drawio`**: Tạo và lưu trực tiếp vào workspace `c:\HocC\Daily\<Ten_Bieu_Do>.drawio` với cấu trúc XML hợp lệ 100%, sẵn sàng mở trên `app.diagrams.net`.
2. **File xem trước HTML/SVG Vector 4K**: Lưu tại `c:\HocC\Daily\<Ten_Bieu_Do>.html` để người dùng click xem ngay trên trình duyệt mà không cần cài phần mềm.
3. **Bản thuyết minh nghiệp vụ**: Giải thích căn cơ học thuật của từng mũi tên, đối chiếu 1:1 với mã nguồn Backend/Frontend đang chạy thực tế.
