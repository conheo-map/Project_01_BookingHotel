"""
Draw.io UML Use Case Diagram Generator
Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo
Tuân thủ 100% nguyên tắc ooad-architect-expert & drawio-uml-architect:
- Font Arial/Segoe UI, nhãn <<include>> trỏ thuận, <<extend>> trỏ ngược có badge nổi bật.
- Tọa độ không đè chữ, khoảng cách >= 60-80px, orthogonal lines.
- Xuất bản 17 file vật lý .drawio chuẩn xác.
"""

import os
import sys
import xml.sax.saxutils as saxutils

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

STYLE_TITLE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#0F172A;fontFamily=Arial;"
STYLE_SUBTITLE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;fontStyle=2;fontColor=#475569;fontFamily=Arial;"
STYLE_BOUNDARY = "shape=rect;fillColor=none;strokeColor=#475569;strokeWidth=1.5;rounded=0;verticalAlign=top;fontStyle=1;fontSize=13;fontFamily=Arial;fontColor=#1E293B;align=center;spacingTop=12;"
STYLE_ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#F8FAFC;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;fontFamily=Arial;fontColor=#000000;align=center;"
STYLE_UC_MOTHER = "ellipse;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;strokeWidth=2;fontColor=#1E3A8A;fontStyle=1;fontSize=11;fontFamily=Arial;align=center;verticalAlign=middle;spacing=6;"
STYLE_UC_SUB = "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontColor=#000000;fontStyle=1;fontSize=11;fontFamily=Arial;align=center;verticalAlign=middle;spacing=4;"
STYLE_EDGE_ASSOC = "edgeStyle=orthogonalEdgeStyle;endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.2;rounded=0;"
STYLE_EDGE_GEN = "edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;endSize=12;strokeColor=#000000;strokeWidth=1.5;html=1;rounded=0;"
STYLE_EDGE_INC = "edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=5 5;endArrow=open;endSize=8;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontStyle=1;fontFamily=Arial;html=1;rounded=0;labelBackgroundColor=#FFFFFF;labelBorderColor=#000000;"
STYLE_EDGE_EXT = "edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=5 5;endArrow=open;endSize=8;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontStyle=1;fontFamily=Arial;html=1;rounded=0;labelBackgroundColor=#FFFFFF;labelBorderColor=#000000;"
STYLE_NOTE = "shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor=#FEF9C3;strokeColor=#CA8A04;strokeWidth=1.2;fontColor=#713F12;fontSize=10;fontFamily=Arial;fontStyle=2;align=left;spacing=6;"
STYLE_NOTE_LINK = "edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=3 3;endArrow=none;strokeColor=#CA8A04;strokeWidth=1;html=1;rounded=0;"


class DrawioDiagram:
    def __init__(self, name="Page-1", width=1654, height=1169):
        self.name = name
        self.width = width
        self.height = height
        self.cells = []
        self.cell_id_seq = 2

    def next_id(self):
        cid = f"cell_{self.cell_id_seq}"
        self.cell_id_seq += 1
        return cid

    def add_title(self, title_text, subtitle_text="Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo"):
        cid_t = self.next_id()
        val_t = saxutils.escape(title_text)
        self.cells.append(
            f'<mxCell id="{cid_t}" value="{val_t}" style="{STYLE_TITLE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="40" y="24" width="800" height="30" as="geometry" />\n'
            f'</mxCell>'
        )
        cid_s = self.next_id()
        val_s = saxutils.escape(subtitle_text)
        self.cells.append(
            f'<mxCell id="{cid_s}" value="{val_s}" style="{STYLE_SUBTITLE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="40" y="52" width="800" height="20" as="geometry" />\n'
            f'</mxCell>'
        )

    def add_boundary(self, label, x, y, w, h):
        cid = self.next_id()
        val = saxutils.escape(label)
        self.cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{STYLE_BOUNDARY}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_actor(self, label, x, y, w=50, h=90):
        cid = self.next_id()
        val = saxutils.escape(label)
        self.cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{STYLE_ACTOR}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_use_case(self, label, x, y, w=210, h=70, is_mother=False):
        cid = self.next_id()
        val = saxutils.escape(label)
        style = STYLE_UC_MOTHER if is_mother else STYLE_UC_SUB
        self.cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_note(self, text, x, y, w=220, h=65):
        cid = self.next_id()
        val = saxutils.escape(text)
        self.cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{STYLE_NOTE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_association(self, source_id, target_id):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" style="{STYLE_EDGE_ASSOC}" edge="1" parent="1" source="{source_id}" target="{target_id}">\n'
            f'  <mxGeometry relative="1" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_generalization(self, child_id, parent_id):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" style="{STYLE_EDGE_GEN}" edge="1" parent="1" source="{child_id}" target="{parent_id}">\n'
            f'  <mxGeometry relative="1" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_include(self, source_id, target_id):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" value="&lt;&lt;include&gt;&gt;" style="{STYLE_EDGE_INC}" edge="1" parent="1" source="{source_id}" target="{target_id}">\n'
            f'  <mxGeometry relative="1" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_extend(self, extending_id, base_id):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" value="&lt;&lt;extend&gt;&gt;" style="{STYLE_EDGE_EXT}" edge="1" parent="1" source="{extending_id}" target="{base_id}">\n'
            f'  <mxGeometry relative="1" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_note_link(self, note_id, target_id):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" style="{STYLE_NOTE_LINK}" edge="1" parent="1" source="{note_id}" target="{target_id}">\n'
            f'  <mxGeometry relative="1" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def to_xml(self):
        cells_xml = "\n        ".join(self.cells)
        esc_name = saxutils.escape(self.name)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-31T16:00:00.000Z" agent="Mozilla/5.0" version="24.0.0" type="device">
  <diagram id="diagram_saigon_condao" name="{esc_name}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width}" pageHeight="{self.height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {cells_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

    def save(self, filepath):
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_xml())
        print(f"[OK] Đã xuất bản: {filepath}")


# ==============================================================================
# HÀM TẠO 17 BIỂU ĐỒ
# ==============================================================================

def create_00_overall():
    d = DrawioDiagram(name="Use Case Tong Quat", width=1750, height=1280)
    d.add_title("BIỂU ĐỒ USE CASE TỔNG QUÁT TOÀN HỆ THỐNG", "Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Saigon - Condao Islands Resort)")
    
    # Boundary
    d.add_boundary("RANH GIỚI HỆ THỐNG: SAIGON - CONDAO ISLANDS RESORT PLATFORM", 290, 90, 1120, 1040)
    
    # Left Actors
    act_cust = d.add_actor("KHÁCH HÀNG\n(CUSTOMER)", 70, 160)
    act_guest = d.add_actor("KHÁCH CHƯA ĐĂNG NHẬP\n(ANONYMOUS GUEST)", 40, 310)
    act_member = d.add_actor("HỘI VIÊN ĐÃ ĐĂNG NHẬP\n(LOYALTY MEMBER)", 170, 310)
    d.add_generalization(act_guest, act_cust)
    d.add_generalization(act_member, act_cust)
    
    act_rec = d.add_actor("NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)", 100, 560)
    act_hk = d.add_actor("NHÂN VIÊN BUỒNG PHÒNG\n(HOUSEKEEPER)", 100, 840)
    
    # Right Actors
    act_mgr = d.add_actor("QUẢN LÝ RESORT\n(HOTEL MANAGER)", 1470, 340)
    act_adm = d.add_actor("QUẢN TRỊ HỆ THỐNG\n(SYSTEM ADMIN)", 1470, 720)
    
    # Bottom Actors
    act_pay = d.add_actor("CỔNG THANH TOÁN\n(PAYMENT GATEWAY)", 530, 1160)
    act_cron = d.add_actor("MÁY CHỦ CHẠY NỀN\n(CRON SYSTEM)", 1020, 1160)

    # Use Cases - Column 1: B2C (x=330)
    uc1 = d.add_use_case("TÌM KIẾM PHÒNG TRỰC TUYẾN", 330, 130, 220, 60, True)
    uc2 = d.add_use_case("XEM CHI TIẾT & ĐÁNH GIÁ PHÒNG", 330, 220, 220, 60)
    uc3 = d.add_use_case("QUẢN LÝ GIỎ HÀNG ĐA PHÒNG", 330, 310, 220, 60)
    uc4 = d.add_use_case("ĐẶT PHÒNG TRỰC TUYẾN (B2C)", 330, 400, 220, 60, True)
    uc5 = d.add_use_case("HỦY PHÒNG & HOÀN TIỀN", 330, 490, 220, 60)
    uc6 = d.add_use_case("QUẢN LÝ TÀI KHOẢN & HỘI VIÊN", 330, 580, 220, 60)

    # Use Cases - Column 2: Tiền sảnh & Buồng phòng (x=700)
    uc7 = d.add_use_case("TIẾP NHẬN ĐẶT PHÒNG TẠI QUẦY (WALK-IN)", 700, 160, 230, 65, True)
    uc8 = d.add_use_case("LÀM THỦ TỤC NHẬN PHÒNG (CHECK-IN)", 700, 260, 230, 65, True)
    uc9 = d.add_use_case("GHI NHẬN TIÊU DÙNG DỊCH VỤ (EXTRA)", 700, 360, 230, 65)
    uc10 = d.add_use_case("LÀM THỦ TỤC TRẢ PHÒNG & QUYẾT TOÁN", 700, 460, 230, 65, True)
    uc11 = d.add_use_case("ĐIỀU PHỐI SƠ ĐỒ GANTT & XỬ LÝ NO-SHOW", 700, 560, 230, 65)
    uc12 = d.add_use_case("QUẢN LÝ VỆ SINH BUỒNG PHÒNG", 700, 740, 230, 65, True)
    uc13 = d.add_use_case("QUÉT DỌN PHÒNG KHÓA TẠM QUÁ HẠN", 700, 890, 230, 65, True)

    # Use Cases - Column 3: Quản lý & Admin (x=1080)
    uc14 = d.add_use_case("QUẢN LÝ LOẠI PHÒNG & PHÒNG VẬT LÝ", 1080, 240, 240, 65)
    uc15 = d.add_use_case("THIẾT LẬP GIÁ LINH HOẠT & VOUCHER", 1080, 400, 240, 65, True)
    uc16 = d.add_use_case("QUẢN TRỊ PHÂN QUYỀN RBAC & BÁO CÁO", 1080, 660, 240, 65, True)

    # Associations
    d.add_association(act_cust, uc1)
    d.add_association(act_cust, uc2)
    d.add_association(act_cust, uc3)
    d.add_association(act_cust, uc4)
    d.add_association(act_cust, uc5)
    d.add_association(act_member, uc6)

    d.add_association(act_rec, uc7)
    d.add_association(act_rec, uc8)
    d.add_association(act_rec, uc9)
    d.add_association(act_rec, uc10)
    d.add_association(act_rec, uc11)

    d.add_association(act_hk, uc12)

    d.add_association(act_mgr, uc14)
    d.add_association(act_mgr, uc15)
    d.add_association(act_mgr, uc16)
    d.add_association(act_adm, uc16)

    d.add_association(act_pay, uc4)
    d.add_association(act_pay, uc5)
    d.add_association(act_cron, uc13)

    return d


def create_decomposition(title, mother_name, actor_name, includes, extends, sec_actor=None):
    """Hàm khung chuẩn hóa để sinh biểu đồ phân rã độc lập đạt chuẩn OOAD."""
    d = DrawioDiagram(name=title, width=1550, height=880)
    d.add_title(f"PHÂN RÃ USE CASE: {title.upper()}", f"Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Nghiệp vụ chi tiết)")

    # Boundary
    d.add_boundary(f"RANH GIỚI NGHIỆP VỤ: {mother_name}", 240, 90, 1030, 720)

    # Primary Actor
    act = d.add_actor(actor_name, 70, 280)

    # Secondary Actor
    sec_act = None
    if sec_actor:
        sec_act = d.add_actor(sec_actor, 1350, 280)

    # Mother UC
    mother = d.add_use_case(mother_name, 560, 270, 240, 85, is_mother=True)
    d.add_association(act, mother)
    if sec_act:
        d.add_association(sec_act, mother)

    # Position Includes (bên phải / trên dưới)
    inc_x = 940
    inc_count = len(includes)
    start_y = 120
    spacing_y = int(460 / max(inc_count, 1))

    for i, inc_label in enumerate(includes):
        y_pos = start_y + i * spacing_y
        inc_node = d.add_use_case(inc_label, inc_x, y_pos, 240, 65)
        d.add_include(mother, inc_node)

    # Position Extends (bên dưới Mother UC)
    ext_count = len(extends)
    start_ext_x = 300
    ext_spacing_x = int(640 / max(ext_count, 1))
    ext_y = 570

    for j, (ext_label, ext_condition) in enumerate(extends):
        x_pos = start_ext_x + j * ext_spacing_x
        ext_node = d.add_use_case(ext_label, x_pos, ext_y, 230, 65)
        # extend trỏ ngược từ ext_node về mother
        ext_edge = d.add_extend(ext_node, mother)
        # Gắn note điều kiện
        note_node = d.add_note(f"Điểm mở rộng / Điều kiện:\n{ext_condition}", x_pos, ext_y + 80, 230, 65)
        d.add_note_link(note_node, ext_node)

    return d


def main():
    dest_dirs = [
        os.path.join(os.getcwd(), 'diagrams', 'use_cases'),
        r'c:\HocC\Daily'
    ]

    diagrams = {}

    # 00. Tổng Quát
    diagrams['00_Use_Case_Tong_Quat.drawio'] = create_00_overall()

    # 01. Tìm kiếm phòng
    diagrams['01_Phan_Ra_Tim_Kiem_Phong.drawio'] = create_decomposition(
        title="Tìm Kiếm Phòng Trực Tuyến",
        mother_name="TÌM KIẾM PHÒNG TRỰC TUYẾN",
        actor_name="KHÁCH HÀNG\n(CUSTOMER)",
        includes=[
            "NHẬP TIÊU CHÍ (NGÀY, SỐ LƯỢNG KHÁCH)",
            "QUÉT PHÒNG TRỐNG THỜI GIAN THỰC (REALTIME)",
            "TÍNH BÁO GIÁ HIỆU LỰC CHO TỪNG ĐÊM LƯU TRÚ"
        ],
        extends=[
            ("LỌC THEO MỨC GIÁ, SAO & TIỆN ÍCH", "Khách hàng chọn áp dụng bộ lọc chi tiết ở sidebar"),
            ("SẮP XẾP KẾT QUẢ THEO GIÁ / RATING", "Khách chọn tiêu chí sắp xếp tăng/giảm giá hoặc đánh giá"),
            ("GỢI Ý ĐẶT PHÒNG GHÉP PHÂN ĐOẠN", "Hết phòng liền mạch cho toàn bộ số đêm khách yêu cầu")
        ]
    )

    # 02. Chi tiết phòng
    diagrams['02_Phan_Ra_Chi_Tiet_Phong.drawio'] = create_decomposition(
        title="Xem Chi Tiết Phòng & Đánh Giá",
        mother_name="XEM CHI TIẾT PHÒNG & ĐÁNH GIÁ",
        actor_name="KHÁCH HÀNG\n(CUSTOMER)",
        includes=[
            "TRA CỨU THÔNG SỐ SỨC CHỨA & DIỆN TÍCH",
            "TÍNH TOÁN PHỤ THU NGƯỜI LỚN & TRẺ EM",
            "XEM DANH MỤC TIỆN ÍCH PHÒNG TIÊU CHUẨN"
        ],
        extends=[
            ("XEM BỘ SƯU TẬP ẢNH HIỆU ỨNG GSAP", "Khách kích hoạt chế độ trình diễn ảnh phóng to"),
            ("XEM LỊCH SỬ BÌNH LUẬN & ĐÁNH GIÁ", "Hạng phòng đã có đánh giá thực tế từ khách trước"),
            ("THÊM PHÒNG VÀO GIỎ HÀNG (CART)", "Khách hàng đồng ý chọn phòng và muốn lưu tạm")
        ]
    )

    # 03. Giỏ hàng
    diagrams['03_Phan_Ra_Quan_Ly_Gio_Hang.drawio'] = create_decomposition(
        title="Quản Lý Giỏ Hàng Đa Phòng",
        mother_name="QUẢN LÝ GIỎ HÀNG ĐA PHÒNG",
        actor_name="KHÁCH HÀNG\n(CUSTOMER)",
        includes=[
            "THÊM PHÒNG VÀO BẢNG CART_ITEMS",
            "XEM & KIỂM TRA TỔNG TIỀN GIỎ HÀNG",
            "CẬP NHẬT SỐ LƯỢNG KHÁCH VÀ NGÀY"
        ],
        extends=[
            ("XÓA BỎ PHÒNG KHỎI GIỎ HÀNG", "Khách chủ động bỏ chọn hoặc quá hạn giữ chỗ session"),
            ("TIẾN HÀNH THANH TOÁN GỘP ĐA PHÒNG", "Giỏ hàng có từ 2 phòng trở lên được xác nhận đặt")
        ]
    )

    # 04. Đặt phòng trực tuyến
    diagrams['04_Phan_Ra_Dat_Phong_Truc_Tuyen.drawio'] = create_decomposition(
        title="Đặt Phòng Trực Tuyến (B2C Booking)",
        mother_name="ĐẶT PHÒNG TRỰC TUYẾN (B2C)",
        actor_name="KHÁCH HÀNG\n(CUSTOMER)",
        includes=[
            "KHÓA GIỮ PHÒNG 10 PHÚT (ROOM_LOCK)",
            "TÍNH BÁO GIÁ VÀ PHỤ THU SỨC CHỨA",
            "LƯU ĐƠN VÀO BOOKING_MASTER & NIGHTS",
            "THANH TOÁN TIỀN PHÒNG / ĐẶT CỌC",
            "GIẢI PHÓNG KHÓA PHÒNG SAU KHI ĐẶT"
        ],
        extends=[
            ("ÁP DỤNG MÃ VOUCHER KHUYẾN MÃI", "Khách nhập mã voucher hợp lệ và còn lượt dùng"),
            ("ĐẶT PHÒNG GHÉP PHÂN ĐOẠN (FRAGMENTED)", "Khách sạn hết phòng liền mạch, đổi phòng giữa kỳ")
        ],
        sec_actor="CỔNG THANH TOÁN\n(PAYMENT GATEWAY)"
    )

    # 05. Hủy phòng & hoàn tiền
    diagrams['05_Phan_Ra_Huy_Phong_Hoan_Tien.drawio'] = create_decomposition(
        title="Hủy Phòng & Hoàn Tiền",
        mother_name="HỦY PHÒNG & HOÀN TIỀN",
        actor_name="KHÁCH HÀNG\n(CUSTOMER)",
        includes=[
            "TRA CỨU CHÍNH SÁCH REFUND_POLICY THEO GIỜ",
            "HỦY CÁC ĐÊM LƯU TRÚ (BOOKING_NIGHTS)",
            "CẬP NHẬT TRẠNG THÁI ĐƠN SANG CANCELED",
            "THỰC HIỆN HOÀN TIỀN CỌC THEO TỶ LỆ"
        ],
        extends=[
            ("GHI NHẬN LÝ DO HỦY ĐẶC BIỆT & XÉT MIỄN PHẠT", "Khách gặp sự cố bất khả kháng được duyệt ngoại lệ")
        ],
        sec_actor="CỔNG THANH TOÁN\n(PAYMENT GATEWAY)"
    )

    # 06. Tài khoản & Loyalty
    diagrams['06_Phan_Ra_Tai_Khoan_Va_Loyalty.drawio'] = create_decomposition(
        title="Quản Lý Tài Khoản & Hội Viên",
        mother_name="QUẢN LÝ TÀI KHOẢN & HỘI VIÊN",
        actor_name="HỘI VIÊN\n(LOYALTY MEMBER)",
        includes=[
            "ĐĂNG KÝ VÀ XÁC THỰC TÀI KHOẢN (ACCOUNTS)",
            "CẬP NHẬT HỒ SƠ CÁ NHÂN (CUSTOMER_PROFILES)",
            "TRA CỨU THẺ HỘI VIÊN & ĐIỂM TÍCH LŨY",
            "TÍCH LŨY ĐIỂM THƯỞNG THEO ĐÊM LƯU TRÚ",
            "TỰ ĐỘNG XÉT NÂNG HẠNG (SILVER / GOLD)"
        ],
        extends=[
            ("GỬI BÌNH LUẬN & ĐÁNH GIÁ SAO", "Kỳ lưu trú của đơn đặt phòng đã hoàn tất Checked-Out")
        ]
    )

    # 07. Walk-in tại quầy
    diagrams['07_Phan_Ra_Walkin_Tai_Quay.drawio'] = create_decomposition(
        title="Tiếp Nhận Đặt Phòng Tại Quầy (Walk-in)",
        mother_name="TIẾP NHẬN ĐẶT PHÒNG TẠI QUẦY",
        actor_name="NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)",
        includes=[
            "KIỂM TRA PHÒNG VẬT LÝ KHẢ DỤNG TẠI CHỖ",
            "GHI NHẬN KHÁCH VÃNG LAI (CUSTOMER_ID = NULL)",
            "THU TIỀN TRỰC TIẾP TẠI QUẦY (TIỀN MẶT/POS)",
            "LƯU ĐƠN BOOKING_MASTER & PHÁT HÀNH INVOICE"
        ],
        extends=[
            ("LIÊN KẾT TÀI KHOẢN HỘI VIÊN ĐỂ TÍCH ĐIỂM", "Khách vãng lai cung cấp SĐT/Email đã có tài khoản")
        ]
    )

    # 08. Thủ tục Check-in
    diagrams['08_Phan_Ra_Thu_Tuc_CheckIn.drawio'] = create_decomposition(
        title="Làm Thủ Tục Nhận Phòng (Check-in)",
        mother_name="LÀM THỦ TỤC NHẬN PHÒNG (CHECK-IN)",
        actor_name="NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)",
        includes=[
            "XÁC MINH MÃ ĐƠN & THÔNG TIN ĐẶT PHÒNG",
            "KIỂM TRA ĐIỀU KIỆN NGÀY NHẬN PHÒNG HỢP LỆ",
            "GIAO PHÒNG VẬT LÝ VÀ CHUYỂN SANG OCCUPIED",
            "CẬP NHẬT TRẠNG THÁI ĐƠN SANG CHECKED-IN"
        ],
        extends=[
            ("ĐIỀU CHUYỂN PHÒNG VẬT LÝ (ROOM MOVE)", "Khách yêu cầu nâng hạng hoặc phòng gặp sự cố kỹ thuật")
        ]
    )

    # 09. Tiêu dùng dịch vụ
    diagrams['09_Phan_Ra_Tieu_Dung_Dich_Vu.drawio'] = create_decomposition(
        title="Ghi Nhận Tiêu Dùng Dịch Vụ (Extra Services)",
        mother_name="GHI NHẬN TIÊU DÙNG DỊCH VỤ",
        actor_name="NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)",
        includes=[
            "TRA CỨU DANH MỤC DỊCH VỤ (SERVICE_CATALOG)",
            "GHI NHẬN TIÊU DÙNG MINIBAR VÀO ĐƠN PHÒNG",
            "GHI NHẬN GIẶT ỦI / THUÊ XE VÀO ĐƠN PHÒNG",
            "CẬP NHẬT TỔNG CHI PHÍ PHÁT SINH EXTRA_SERVICES"
        ],
        extends=[
            ("HỦY MÓN DỊCH VỤ GHI NHẦM (VOID ITEM)", "Lễ tân nhập sai số lượng hoặc khách hoàn trả nguyên vẹn")
        ]
    )

    # 10. Thủ tục Check-out
    diagrams['10_Phan_Ra_Thu_Tuc_CheckOut.drawio'] = create_decomposition(
        title="Làm Thủ Tục Trả Phòng & Quyết Toán",
        mother_name="LÀM THỦ TỤC TRẢ PHÒNG & QUYẾT TOÁN",
        actor_name="NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)",
        includes=[
            "TỔNG HỢP CHI PHÍ & LẬP BẢNG KÊ (STATEMENT)",
            "THU TIỀN PHÒNG & DỊCH VỤ CÒN THIẾU",
            "CẬP NHẬT TRẠNG THÁI ĐƠN SANG CHECKED-OUT",
            "XUẤT HÓA ĐƠN QUYẾT TOÁN INV CHÍNH THỨC",
            "TỰ ĐỘNG CHUYỂN PHÒNG VẬT LÝ SANG 'DIRTY'"
        ],
        extends=[
            ("GHI NHẬN BỒI THƯỜNG HỎNG HÓC / MẤT ĐỒ", "Buồng phòng phát hiện hỏng hóc hoặc thiếu tài sản phòng")
        ]
    )

    # 11. Sơ đồ Gantt & No-show
    diagrams['11_Phan_Ra_So_Do_Gantt_Va_NoShow.drawio'] = create_decomposition(
        title="Điều Phối Sơ Đồ Gantt & Xử Lý No-Show",
        mother_name="ĐIỀU PHỐI GANTT & XỬ LÝ NO-SHOW",
        actor_name="NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)",
        includes=[
            "TRA CỨU MA TRẬN PHÒNG THEO THỜI GIAN (GANTT)",
            "ĐIỀU PHỐI SẮP XẾP PHÒNG CHO ĐƠN TRỰC TUYẾN",
            "GHI NHẬN TRẠNG THÁI KHÁCH VẮNG MẶT (NO-SHOW)"
        ],
        extends=[
            ("THU PHÍ PHẠT NO-SHOW THEO QUY ĐỊNH", "Đơn đặt phòng có cọc hoặc liên kết thẻ đảm bảo trước")
        ]
    )

    # 12. Vệ sinh buồng phòng
    diagrams['12_Phan_Ra_Ve_Sinh_Buong_Phong.drawio'] = create_decomposition(
        title="Quản Lý Vệ Sinh Buồng Phòng",
        mother_name="QUẢN LÝ VỆ SINH BUỒNG PHÒNG",
        actor_name="NHÂN VIÊN BUỒNG PHÒNG\n(HOUSEKEEPER)",
        includes=[
            "TRA CỨU DANH SÁCH PHÒNG CẦN DỌN DẸP (DIRTY)",
            "CẬP NHẬT TRẠNG THÁI PHÒNG SANG 'CLEAN'"
        ],
        extends=[
            ("BÁO CÁO PHÒNG SỰ CỐ BẢO TRÌ ('MAINTENANCE')", "Phát hiện hỏng hóc thiết bị, điều hòa hoặc đường nước"),
            ("KIỂM ĐỊNH BUỒNG PHÒNG ('INSPECTING')", "Giám sát buồng phòng kiểm tra chất lượng trước khi mở bán")
        ]
    )

    # 13. Quét dọn khóa tạm
    diagrams['13_Phan_Ra_Quet_Don_Khoa_Tam.drawio'] = create_decomposition(
        title="Quét Dọn Phòng Khóa Tạm Quá Hạn",
        mother_name="QUÉT DỌN PHÒNG KHÓA TẠM QUÁ HẠN",
        actor_name="MÁY CHỦ CHẠY NỀN\n(CRON SYSTEM)",
        includes=[
            "KÍCH HOẠT TIẾN TRÌNH ĐỊNH KỲ MỖI 1 PHÚT (CRON)",
            "QUÉT BẢN GHI ROOM_LOCK QUÁ HẠN 10 PHÚT",
            "GIẢI PHÓNG KHÓA VÀ TRẢ PHÒNG VỀ KHO MỞ BÁN",
            "GHI NHẬT KÝ GIẢI PHÓNG KHÓA HỆ THỐNG"
        ],
        extends=[]
    )

    # 14. Quản lý loại phòng & phòng
    diagrams['14_Phan_Ra_Quan_Ly_Loai_Va_Phong.drawio'] = create_decomposition(
        title="Quản Lý Loại Phòng & Phòng Vật Lý",
        mother_name="QUẢN LÝ LOẠI PHÒNG & PHÒNG VẬT LÝ",
        actor_name="QUẢN LÝ RESORT\n(HOTEL MANAGER)",
        includes=[
            "CẬP NHẬT THÔNG TIN HẠNG PHÒNG (DIM_ROOMTYPE)",
            "QUẢN LÝ DANH SÁCH PHÒNG VẬT LÝ (PHYSICAL_ROOM)",
            "CẤU HÌNH TIỆN ÍCH VÀ SỨC CHỨA TIÊU CHUẨN"
        ],
        extends=[
            ("TẠM ĐÓNG PHÒNG BẢO TRÌ NÂNG CẤP HÀNG LOẠT", "Khách sạn có kế hoạch sửa chữa định kỳ hoặc cải tạo")
        ]
    )

    # 15. Giá linh hoạt & voucher
    diagrams['15_Phan_Ra_Gia_Linh_Hoat_Va_Voucher.drawio'] = create_decomposition(
        title="Thiết Lập Giá Linh Hoạt & Mã Giảm Giá",
        mother_name="THIẾT LẬP GIÁ LINH HOẠT & VOUCHER",
        actor_name="QUẢN LÝ RESORT\n(HOTEL MANAGER)",
        includes=[
            "CẬP NHẬT BẢNG GIÁ THEO NGÀY (ROOM_RATES)",
            "THIẾT LẬP GIÁ NGÀY LỄ VÀ CUỐI TUẦN",
            "KHỞI TẠO MÃ VOUCHER & TỶ LỆ CHIẾT KHẤU",
            "CẤU HÌNH GIỚI HẠN LƯỢT DÙNG & HẠNG THẺ"
        ],
        extends=[
            ("ÁP DỤNG GIÁ ĐỒNG LOẠT THEO MÙA DU LỊCH", "Thiết lập giá linh hoạt cho khoảng thời gian cao điểm"),
            ("DỪNG CHƯƠNG TRÌNH KHUYẾN MÃI TRƯỚC HẠN", "Hết ngân sách khuyến mãi hoặc đạt chỉ tiêu kinh doanh sớm")
        ]
    )

    # 16. Phân quyền RBAC & Báo cáo
    diagrams['16_Phan_Ra_Quan_Tri_RBAC_Va_Bao_Cao.drawio'] = create_decomposition(
        title="Quản Trị Phân Quyền RBAC & Báo Cáo Thống Kê",
        mother_name="QUẢN TRỊ PHÂN QUYỀN RBAC & BÁO CÁO",
        actor_name="QUẢN TRỊ HỆ THỐNG\n(SYSTEM ADMIN)",
        includes=[
            "QUẢN LÝ HỒ SƠ TÀI KHOẢN NHÂN VIÊN (STAFF_PROFILES)",
            "GÁN VAI TRÒ VÀ QUYỀN HẠN PHÂN HỆ (RBAC)",
            "TỔNG HỢP DOANH THU, CÔNG SUẤT PHÒNG & GIÁ ADR"
        ],
        extends=[
            ("KHÓA / THU HỒI TÀI KHOẢN NHÂN VIÊN", "Nhân viên nghỉ việc hoặc vi phạm quy chế bảo mật"),
            ("TRUY VẾT NHẬT KÝ HOẠT ĐỘNG (AUDIT LOG)", "Cần kiểm toán và điều tra dữ liệu bất thường"),
            ("XUẤT BÁO CÁO TÀI CHÍNH RA PDF / EXCEL", "Quản lý cần in ấn hoặc lưu trữ tài liệu báo cáo")
        ],
        sec_actor="QUẢN LÝ RESORT\n(HOTEL MANAGER)"
    )

    # Lưu toàn bộ 17 files vào cả 2 thư mục
    for target_dir in dest_dirs:
        os.makedirs(target_dir, exist_ok=True)
        print(f"\n>>> Đang xuất bản vào thư mục: {target_dir}")
        for filename, diag in diagrams.items():
            fpath = os.path.join(target_dir, filename)
            diag.save(fpath)

    print("\n[THÀNH CÔNG] ĐÃ XUẤT BẢN TRỌN BỘ 17/17 BIỂU ĐỒ DRAW.IO NATIVE!")


if __name__ == '__main__':
    main()
