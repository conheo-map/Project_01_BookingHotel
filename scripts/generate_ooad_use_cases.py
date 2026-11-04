"""
Generator for CAD-Standard OOAD Use Case Diagrams (Grade 10.0 University Defense Standard)
Project: Saigon - Condao Islands Resort Booking Platform
Strict Constraints:
- 100% Textbook Standard UML 2.x:
  * Primary Actors (Human / Initiators): ALWAYS on the LEFT.
  * Secondary Actors (External Systems / Supporting Services): ALWAYS on the RIGHT.
  * NO Actors at the Bottom or Top.
  * Single/Clean Use Case Alignment: Zero Crossings, Zero Slicing.
  * Pure UML Elements: ONLY Actor, Ellipse Use Case, Boundary, and Standard Connectors (Association, Generalization, «include», «extend»).
  * ABSOLUTELY ZERO Note/Comment boxes.
- 100% Monochrome Black & White (#FFFFFF background, #000000 strokes/text).
- Accurate UML Stereotypes using guillemets (&laquo;include&raquo; and &laquo;extend&raquo;).
- Strict UTF-8 without BOM.
"""

import os
import sys
import xml.sax.saxutils as saxutils

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Typography and Styling Constants (100% Monochrome B&W)
STYLE_TITLE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;"
STYLE_SUBTITLE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;fontStyle=2;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;"
STYLE_BOUNDARY = "shape=rect;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;rounded=0;verticalAlign=top;fontStyle=1;fontSize=13;fontFamily=Arial,Helvetica,sans-serif;fontColor=#000000;align=center;spacingTop=12;"
STYLE_ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;fontFamily=Arial,Helvetica,sans-serif;fontColor=#000000;align=center;"
STYLE_UC = "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontColor=#000000;fontStyle=1;fontSize=11;fontFamily=Arial,Helvetica,sans-serif;align=center;verticalAlign=middle;spacing=4;"
STYLE_EDGE_ASSOC = "edgeStyle=orthogonalEdgeStyle;endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.2;rounded=0;"
STYLE_EDGE_GEN = "edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;endSize=12;strokeColor=#000000;strokeWidth=1.5;html=1;rounded=0;"
STYLE_EDGE_INC = "edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=5 5;endArrow=open;endSize=8;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontStyle=1;fontFamily=Arial,Helvetica,sans-serif;html=1;rounded=0;labelBackgroundColor=#FFFFFF;fontColor=#000000;"
STYLE_EDGE_EXT = "edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=5 5;endArrow=open;endSize=8;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontStyle=1;fontFamily=Arial,Helvetica,sans-serif;html=1;rounded=0;labelBackgroundColor=#FFFFFF;fontColor=#000000;"


class BwDiagram:
    def __init__(self, name="Page-1", width=1450, height=1280):
        self.name = name
        self.width = width
        self.height = height
        self.cells = []
        self.seq = 2

    def next_id(self):
        cid = f"cell_{self.seq}"
        self.seq += 1
        return cid

    def add_title(self, title_text, subtitle_text="Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo"):
        cid_t = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid_t}" value="{saxutils.escape(title_text)}" style="{STYLE_TITLE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="40" y="24" width="950" height="30" as="geometry" />\n'
            f'</mxCell>'
        )
        cid_s = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid_s}" value="{saxutils.escape(subtitle_text)}" style="{STYLE_SUBTITLE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="40" y="52" width="950" height="20" as="geometry" />\n'
            f'</mxCell>'
        )

    def add_boundary(self, label, x, y, w, h):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" value="{saxutils.escape(label)}" style="{STYLE_BOUNDARY}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_actor(self, label, x, y, w=50, h=90):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" value="{saxutils.escape(label)}" style="{STYLE_ACTOR}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_uc(self, label, x, y, w=280, h=50):
        cid = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid}" value="{saxutils.escape(label)}" style="{STYLE_UC}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_assoc(self, src, tgt, exit_pt=None, entry_pt=None, waypoints=None):
        cid = self.next_id()
        style = f"{STYLE_EDGE_ASSOC}"
        if exit_pt:
            style += f"exitX={exit_pt[0]};exitY={exit_pt[1]};exitDx=0;exitDy=0;"
        if entry_pt:
            style += f"entryX={entry_pt[0]};entryY={entry_pt[1]};entryDx=0;entryDy=0;"
        
        pts_xml = ""
        if waypoints:
            pt_tags = "\n".join([f'      <mxPoint x="{px}" y="{py}" />' for px, py in waypoints])
            pts_xml = f'    <Array as="points">\n{pt_tags}\n    </Array>\n'

        self.cells.append(
            f'<mxCell id="{cid}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'{pts_xml}'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def add_gen(self, child, parent, exit_pt=(0.5, 0), entry_pt=(0.5, 1), waypoints=None):
        cid = self.next_id()
        style = f"{STYLE_EDGE_GEN}exitX={exit_pt[0]};exitY={exit_pt[1]};exitDx=0;exitDy=0;entryX={entry_pt[0]};entryY={entry_pt[1]};entryDx=0;entryDy=0;"
        pts_xml = ""
        if waypoints:
            pt_tags = "\n".join([f'      <mxPoint x="{px}" y="{py}" />' for px, py in waypoints])
            pts_xml = f'    <Array as="points">\n{pt_tags}\n    </Array>\n'

        self.cells.append(
            f'<mxCell id="{cid}" style="{style}" edge="1" parent="1" source="{child}" target="{parent}">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'{pts_xml}'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def add_inc(self, mother, sub, exit_pt=(1, 0.5), entry_pt=(0, 0.5), waypoints=None):
        cid = self.next_id()
        style = f"{STYLE_EDGE_INC}exitX={exit_pt[0]};exitY={exit_pt[1]};exitDx=0;exitDy=0;entryX={entry_pt[0]};entryY={entry_pt[1]};entryDx=0;entryDy=0;"
        pts_xml = ""
        if waypoints:
            pt_tags = "\n".join([f'      <mxPoint x="{px}" y="{py}" />' for px, py in waypoints])
            pts_xml = f'    <Array as="points">\n{pt_tags}\n    </Array>\n'

        self.cells.append(
            f'<mxCell id="{cid}" value="&amp;laquo;include&amp;raquo;" style="{style}" edge="1" parent="1" source="{mother}" target="{sub}">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'{pts_xml}'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def add_ext(self, extending, mother, exit_pt=(0.5, 0), entry_pt=(0.5, 1), waypoints=None):
        cid = self.next_id()
        style = f"{STYLE_EDGE_EXT}exitX={exit_pt[0]};exitY={exit_pt[1]};exitDx=0;exitDy=0;entryX={entry_pt[0]};entryY={entry_pt[1]};entryDx=0;entryDy=0;"
        pts_xml = ""
        if waypoints:
            pt_tags = "\n".join([f'      <mxPoint x="{px}" y="{py}" />' for px, py in waypoints])
            pts_xml = f'    <Array as="points">\n{pt_tags}\n    </Array>\n'

        self.cells.append(
            f'<mxCell id="{cid}" value="&amp;laquo;extend&amp;raquo;" style="{style}" edge="1" parent="1" source="{extending}" target="{mother}">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'{pts_xml}'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def to_xml(self):
        cells_xml = "\n        ".join(self.cells)
        esc_name = saxutils.escape(self.name)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-31T17:00:00.000Z" agent="Mozilla/5.0" version="24.0.0" type="device">
  <diagram id="saigon_condao_ooad" name="{esc_name}">
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
# 00. SƠ ĐỒ USE CASE TỔNG QUÁT TOÀN HỆ THỐNG (SYSTEM OVERVIEW)
# QUY CHUẨN KINH ĐIỂN UML:
# - CỘT TRÁI: 100% Primary Actors (Con người / Khởi xướng mục tiêu)
# - CỘT GIỮA: Ranh giới hệ thống chứa các Use Case chức năng
# - CỘT PHẢI: 100% Secondary Actors (Hệ thống ngoài / Bên thứ ba hỗ trợ)
# - ĐÁY & ĐỈNH: TUYỆT ĐỐI KHÔNG CÓ ACTOR NÀO
# ==============================================================================
def build_00_overview():
    d = BwDiagram(name="Use Case Tong Quat Toan He Thong", width=1450, height=1280)
    d.add_title("BIỂU ĐỒ USE CASE TỔNG QUÁT TOÀN HỆ THỐNG (SYSTEM OVERVIEW)",
                "Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Saigon - Condao Resort)")
    
    # Boundary ở giữa: x=290, y=90, w=760, h=1150
    d.add_boundary("RANH GIỚI HỆ THỐNG: SAIGON - CONDAO RESORT PLATFORM", 290, 90, 760, 1150)

    # ─── 1. CỘT TRÁI: PRIMARY ACTORS (CON NGƯỜI) ──────────────────────────────
    act_cust = d.add_actor("KHÁCH HÀNG\n(CUSTOMER)", 70, 240)
    act_rec  = d.add_actor("NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)", 70, 600)
    act_mgr  = d.add_actor("QUẢN LÝ RESORT\n(HOTEL MANAGER)", 70, 840)
    act_hk   = d.add_actor("NHÂN VIÊN BUỒNG PHÒNG\n(HOUSEKEEPER)", 70, 990)
    act_adm  = d.add_actor("QUẢN TRỊ VIÊN HỆ THỐNG\n(SYSTEM ADMIN)", 70, 1100)

    # Quan hệ Kế thừa Actor: Quản lý kế thừa Lễ tân (đi thẳng đứng trong lề trái)
    d.add_gen(act_mgr, act_rec, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    # ─── 2. CỘT PHẢI: SECONDARY ACTORS (HỆ THỐNG BÊN NGOÀI) ───────────────────
    act_pay  = d.add_actor("CỔNG THANH TOÁN\n(PAYMENT GATEWAY)", 1170, 250)
    act_cron = d.add_actor("MÁY CHỦ CHẠY NỀN\n(CRON SYSTEM)", 1170, 440)

    # ─── 3. CỘT GIỮA: CÁC USE CASE HỆ THỐNG (x=530, w=280) ───────────────────
    # A. Phân hệ B2C & Khách hàng
    uc_c1 = d.add_uc("TÌM KIẾM PHÒNG KHẢ DỤNG", 530, 130, 280, 48)
    uc_c2 = d.add_uc("XEM CHI TIẾT & ĐÁNH GIÁ PHÒNG", 530, 190, 280, 48)
    uc_c3 = d.add_uc("QUẢN LÝ GIỎ HÀNG ĐA PHÒNG", 530, 250, 280, 48)
    uc_c4 = d.add_uc("ĐẶT PHÒNG TRỰC TUYẾN (B2C)", 530, 310, 280, 48)
    uc_c5 = d.add_uc("HỦY ĐẶT PHÒNG & HOÀN TIỀN CỌC", 530, 370, 280, 48)
    uc_cron = d.add_uc("QUÉT DỌN PHIÊN GIỮ PHÒNG QUÁ HẠN", 530, 440, 280, 48)
    uc_c6 = d.add_uc("ĐĂNG KÝ, ĐĂNG NHẬP & HỒ SƠ", 530, 500, 280, 48)

    # Nối Khách hàng sang mép trái Use Case B2C (entryX=0; entryY=0.5)
    d.add_assoc(act_cust, uc_c1, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_cust, uc_c2, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_cust, uc_c3, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_cust, uc_c4, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_cust, uc_c5, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_cust, uc_c6, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # Nối Secondary Actors bên phải sang mép phải Use Case (entryX=1; entryY=0.5)
    # Cổng thanh toán nối thẳng sang Đặt phòng B2C và Hủy cọc
    d.add_assoc(act_pay, uc_c4, exit_pt=(0, 0.4), entry_pt=(1, 0.5))
    d.add_assoc(act_pay, uc_c5, exit_pt=(0, 0.6), entry_pt=(1, 0.5))
    # Máy chủ Cron nối thẳng sang Quét dọn phòng quá hạn
    d.add_assoc(act_cron, uc_cron, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    # B. Phân hệ Lễ tân tiền sảnh
    uc_r1 = d.add_uc("TIẾP NHẬN ĐẶT PHÒNG TẠI QUẦY (WALK-IN)", 530, 570, 280, 48)
    uc_r2 = d.add_uc("CHECK-IN & ĐIỀU CHUYỂN PHÒNG", 530, 630, 280, 48)
    uc_r3 = d.add_uc("GHI NHẬN TIÊU DÙNG DỊCH VỤ PHÁT SINH", 530, 690, 280, 48)
    uc_r4 = d.add_uc("CHECK-OUT & QUYẾT TOÁN CÔNG NỢ", 530, 750, 280, 48)
    uc_r5 = d.add_uc("SƠ ĐỒ PHÒNG GANTT & XỬ LÝ NO-SHOW", 530, 810, 280, 48)

    d.add_assoc(act_rec, uc_r1, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_rec, uc_r2, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_rec, uc_r3, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_rec, uc_r4, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_rec, uc_r5, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # C. Phân hệ Quản lý Resort
    uc_m1 = d.add_uc("QUẢN LÝ DANH MỤC HẠNG PHÒNG", 530, 875, 280, 48)
    uc_m2 = d.add_uc("THIẾT LẬP GIÁ LINH HOẠT & VOUCHER", 530, 935, 280, 48)
    uc_m3 = d.add_uc("BÁO CÁO DOANH THU & PHÂN TÍCH KPI", 530, 995, 280, 48)

    d.add_assoc(act_mgr, uc_m1, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_mgr, uc_m2, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_mgr, uc_m3, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # D. Phân hệ Buồng phòng & Quản trị Admin
    uc_hk = d.add_uc("QUẢN LÝ VỆ SINH BUỒNG PHÒNG", 530, 1060, 280, 48)
    uc_adm = d.add_uc("QUẢN TRỊ PHÂN QUYỀN RBAC & NHÂN SỰ", 530, 1125, 280, 48)

    d.add_assoc(act_hk, uc_hk, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_assoc(act_adm, uc_adm, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    return d


# ==============================================================================
# 01. PHÂN HỆ 01: CỔNG ĐẶT PHÒNG TRỰC TUYẾN B2C
# ==============================================================================
def build_01_b2c_booking():
    d = BwDiagram(name="Phan He 01 - Dat Phong Truc Tuyen B2C", width=1650, height=820)
    d.add_title("PHÂN HỆ 01: CỔNG ĐẶT PHÒNG TRỰC TUYẾN B2C (ONLINE BOOKING & REFUND)",
                "Đặc tả phân rã các quan hệ &laquo;include&raquo; bắt buộc và &laquo;extend&raquo; có điều kiện")

    d.add_boundary("RANH GIỚI PHÂN HỆ: CỔNG ĐẶT PHÒNG TRỰC TUYẾN B2C", 240, 90, 1160, 690)

    # Left Actor (Primary)
    act_cust = d.add_actor("KHÁCH HÀNG\n(CUSTOMER)", 70, 310)

    # ─── KHỐI 1: ĐẶT PHÒNG B2C TRỰC TUYẾN ─────────────────────────────────────
    uc_book = d.add_uc("ĐẶT PHÒNG TRỰC TUYẾN (B2C)", 380, 150, 270, 70)
    d.add_assoc(act_cust, uc_book, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # Includes (Cột x=800 bên phải)
    inc_lock = d.add_uc("KHÓA PHÒNG CHỐNG TRÙNG (HOLD LOCK 15 PHÚT)", 800, 110, 290, 50)
    inc_price = d.add_uc("TÍNH BÁO GIÁ VÀ PHỤ THU SỨC CHỨA", 800, 175, 290, 50)
    inc_pay = d.add_uc("XÁC THỰC CỔNG THANH TOÁN (VNPAY/MOMO)", 800, 240, 290, 50)

    d.add_inc(uc_book, inc_lock, exit_pt=(1, 0.25), entry_pt=(0, 0.5))
    d.add_inc(uc_book, inc_price, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_inc(uc_book, inc_pay, exit_pt=(1, 0.75), entry_pt=(0, 0.5))

    # Right Actor (Secondary)
    act_pay = d.add_actor("CỔNG THANH TOÁN\n(PAYMENT GATEWAY)", 1220, 220)
    d.add_assoc(act_pay, inc_pay, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    # Extends (Bố trí song song x=260 và x=530 bên dưới)
    ext_promo = d.add_uc("ÁP DỤNG MÃ GIẢM GIÁ (VOUCHER)", 260, 290, 245, 55)
    d.add_ext(ext_promo, uc_book, exit_pt=(0.5, 0), entry_pt=(0.25, 1))

    ext_frag = d.add_uc("GỢI Ý ĐẶT PHÒNG GHÉP PHÂN ĐOẠN", 530, 290, 245, 55)
    d.add_ext(ext_frag, uc_book, exit_pt=(0.5, 0), entry_pt=(0.75, 1))

    # ─── KHỐI 2: QUÉT DỌN PHÒNG KHÓA TẠM (CRON JOB) ───────────────────────────
    uc_cron = d.add_uc("QUÉT DỌN PHIÊN GIỮ PHÒNG QUÁ HẠN", 800, 350, 290, 50)
    act_cron = d.add_actor("MÁY CHỦ CRON\n(CRON SYSTEM)", 1220, 330)
    d.add_assoc(act_cron, uc_cron, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    # ─── KHỐI 3: HỦY ĐẶT PHÒNG & HOÀN TIỀN CỌC ────────────────────────────────
    uc_cancel = d.add_uc("HỦY ĐẶT PHÒNG & HOÀN TIỀN", 380, 480, 270, 70)
    d.add_assoc(act_cust, uc_cancel, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    inc_calc_ref = d.add_uc("TÍNH TOÁN HOÀN CỌC THEO CHÍNH SÁCH NGÀY HỦY", 800, 460, 290, 50)
    inc_update_bm = d.add_uc("CẬP NHẬT TRẠNG THÁI BOOKING & NIGHTS", 800, 525, 290, 50)
    d.add_inc(uc_cancel, inc_calc_ref, exit_pt=(1, 0.4), entry_pt=(0, 0.5))
    d.add_inc(uc_cancel, inc_update_bm, exit_pt=(1, 0.6), entry_pt=(0, 0.5))

    ext_waiver = d.add_uc("XÉT MIỄN PHẠT DO BẤT KHẢ KHÁNG", 380, 610, 270, 55)
    d.add_ext(ext_waiver, uc_cancel, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    return d


# ==============================================================================
# 02. PHÂN HỆ 02: QUẢN LÝ TÀI KHOẢN & PHÂN QUYỀN (IAM & RBAC)
# ==============================================================================
def build_02_iam_rbac():
    d = BwDiagram(name="Phan He 02 - Tai Khoan Va Phan Quyen RBAC", width=1650, height=820)
    d.add_title("PHÂN HỆ 02: QUẢN LÝ TÀI KHOẢN & PHÂN QUYỀN (IAM & RBAC)",
                "Bóc tách quản trị danh tính người dùng và phân quyền vai trò nội bộ")

    d.add_boundary("RANH GIỚI PHÂN HỆ: QUẢN LÝ TÀI KHOẢN & PHÂN QUYỀN", 240, 90, 1160, 690)

    # Left Actor (Customer / User)
    act_user = d.add_actor("KHÁCH HÀNG / HỘI VIÊN\n(USER)", 70, 280)
    # Right Actor (System Admin)
    act_admin = d.add_actor("QUẢN TRỊ VIÊN HỆ THỐNG\n(SYSTEM ADMIN)", 1440, 390)

    # ─── NHÁNH KHÁCH HÀNG (Cột x=310) ─────────────────────────────────────────
    uc_reg = d.add_uc("ĐĂNG KÝ HỘI VIÊN MỚI", 310, 140, 250, 60)
    d.add_assoc(act_user, uc_reg, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_auth_contact = d.add_uc("XÁC THỰC EMAIL HOẶC SỐ ĐIỆN THOẠI", 650, 115, 270, 45)
    inc_init_profile = d.add_uc("KHỞI TẠO HỒ SƠ CUSTOMER_PROFILES", 650, 175, 270, 45)
    d.add_inc(uc_reg, inc_auth_contact, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_reg, inc_init_profile, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    uc_login = d.add_uc("ĐĂNG NHẬP & XÁC THỰC BẢO MẬT", 310, 280, 250, 60)
    d.add_assoc(act_user, uc_login, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_pwd_hash = d.add_uc("KIỂM TRA BĂM MẬT KHẨU (PASSWORD HASH)", 650, 285, 270, 45)
    d.add_inc(uc_login, inc_pwd_hash, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    ext_lock = d.add_uc("KHÓA TÀI KHOẢN KHI ĐĂNG NHẬP SAI 5 LẦN", 310, 390, 250, 55)
    d.add_ext(ext_lock, uc_login, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    uc_profile = d.add_uc("CẬP NHẬT HỒ SƠ & ĐỔI MẬT KHẨU", 310, 520, 250, 55)
    d.add_assoc(act_user, uc_profile, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # ─── NHÁNH QUẢN TRỊ ADMIN (Cột x=1020) ────────────────────────────────────
    uc_staff_mgmt = d.add_uc("QUẢN LÝ HỒ SƠ NHÂN SỰ (STAFF_PROFILES)", 1020, 210, 270, 60)
    d.add_assoc(act_admin, uc_staff_mgmt, exit_pt=(0, 0.5), entry_pt=(1, 0.5))
    inc_create_staff = d.add_uc("LẬP HỒ SƠ VÀ CẤP TÀI KHOẢN NỘI BỘ", 650, 215, 270, 45)
    d.add_inc(uc_staff_mgmt, inc_create_staff, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    uc_rbac = d.add_uc("CẤU HÌNH PHÂN QUYỀN VAI TRÒ (RBAC)", 1020, 390, 270, 60)
    d.add_assoc(act_admin, uc_rbac, exit_pt=(0, 0.5), entry_pt=(1, 0.5))
    inc_assign_role = d.add_uc("GÁN VAI TRÒ ROLE_ID CHO TÀI KHOẢN", 650, 370, 270, 45)
    inc_assign_perm = d.add_uc("THIẾT LẬP QUYỀN TRUY CẬP TỪNG PHÂN HỆ", 650, 430, 270, 45)
    d.add_inc(uc_rbac, inc_assign_role, exit_pt=(0, 0.3), entry_pt=(1, 0.5))
    d.add_inc(uc_rbac, inc_assign_perm, exit_pt=(0, 0.7), entry_pt=(1, 0.5))

    uc_audit = d.add_uc("GHI NHẬN & TRA CỨU AUDIT LOGS", 1020, 550, 270, 60)
    d.add_assoc(act_admin, uc_audit, exit_pt=(0, 0.5), entry_pt=(1, 0.5))
    ext_alert = d.add_uc("CẢNH BÁO CAN THIỆP DỮ LIỆU BẤT THƯỜNG", 1020, 650, 270, 55)
    d.add_ext(ext_alert, uc_audit, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    return d


# ==============================================================================
# 03. PHÂN HỆ 03: TÁC NGHIỆP QUẦY TIỀN SẢNH & LỄ TÂN
# ==============================================================================
def build_03_front_desk():
    d = BwDiagram(name="Phan He 03 - Tac Nghiep Le Tan Tien Sanh", width=1750, height=980)
    d.add_title("PHÂN HỆ 03: TÁC NGHIỆP QUẦY TIỀN SẢNH & LỄ TÂN (FRONT DESK & PMS)",
                "Quy trình quản lý Walk-in, Check-in, Extra services, Check-out và Gantt Matrix")

    d.add_boundary("RANH GIỚI PHÂN HỆ: TÁC NGHIỆP TIỀN SẢNH & LỄ TÂN", 240, 90, 1220, 850)

    # Left Actor (Primary)
    act_rec = d.add_actor("NHÂN VIÊN LỄ TÂN\n(RECEPTIONIST)", 70, 460)

    # ─── BĂNG 1: WALK-IN (y=130) ──────────────────────────────────────────────
    uc_walkin = d.add_uc("TIẾP NHẬN ĐẶT PHÒNG TẠI QUẦY (WALK-IN)", 330, 130, 270, 65)
    d.add_assoc(act_rec, uc_walkin, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_assign_room = d.add_uc("GÁN PHÒNG VẬT LÝ TỨC THỜI", 710, 100, 270, 45)
    inc_collect_cash = d.add_uc("THU TIỀN CỌC TRỰC TIẾP (TIỀN MẶT/POS)", 710, 155, 270, 45)
    inc_anon_cust = d.add_uc("GHI NHẬN KHÁCH VÃNG LAI (CUSTOMER_ID=NULL)", 710, 210, 270, 45)
    d.add_inc(uc_walkin, inc_assign_room, exit_pt=(1, 0.2), entry_pt=(0, 0.5))
    d.add_inc(uc_walkin, inc_collect_cash, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_inc(uc_walkin, inc_anon_cust, exit_pt=(1, 0.8), entry_pt=(0, 0.5))

    # ─── BĂNG 2: CHECK-IN & ROOM MOVE (y=300) ─────────────────────────────────
    uc_checkin = d.add_uc("LÀM THỦ TỤC NHẬN PHÒNG (CHECK-IN)", 330, 300, 270, 65)
    d.add_assoc(act_rec, uc_checkin, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_cccd = d.add_uc("LƯU TRỮ THÔNG TIN CCCD / HỘ CHIẾU", 710, 285, 270, 45)
    inc_occupy = d.add_uc("CẬP NHẬT TRẠNG THÁI PHÒNG SANG OCCUPIED", 710, 340, 270, 45)
    d.add_inc(uc_checkin, inc_cccd, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_checkin, inc_occupy, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    ext_move = d.add_uc("XỬ LÝ ĐỔI PHÒNG (ROOM MOVE)", 330, 410, 270, 55)
    d.add_ext(ext_move, uc_checkin, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    # ─── BĂNG 3: EXTRA SERVICES (y=520) ───────────────────────────────────────
    uc_extra = d.add_uc("GHI NHẬN TIÊU DÙNG DỊCH VỤ PHÁT SINH", 330, 520, 270, 60)
    d.add_assoc(act_rec, uc_extra, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_catalog = d.add_uc("TRA CỨU SERVICE_CATALOG (MINIBAR, TOUR)", 710, 495, 270, 45)
    inc_extra_row = d.add_uc("GHI NHẬN VÀO HÓA ĐƠN EXTRA_SERVICES", 710, 550, 270, 45)
    d.add_inc(uc_extra, inc_catalog, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_extra, inc_extra_row, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    # ─── BĂNG 4: CHECK-OUT (y=650) ────────────────────────────────────────────
    uc_checkout = d.add_uc("LÀM THỦ TỤC TRẢ PHÒNG (CHECK-OUT)", 330, 650, 270, 65)
    d.add_assoc(act_rec, uc_checkout, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_vat = d.add_uc("QUYẾT TOÁN CÔNG NỢ & IN HÓA ĐƠN VAT", 710, 630, 270, 45)
    inc_dirty = d.add_uc("TỰ ĐỘNG CHUYỂN PHÒNG SANG CHỜ DỌN (DIRTY)", 710, 685, 270, 45)
    d.add_inc(uc_checkout, inc_vat, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_checkout, inc_dirty, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    ext_damage = d.add_uc("THU TIỀN ĐỀN BỒI HỎNG HÓC VẬT TƯ", 330, 755, 270, 55)
    d.add_ext(ext_damage, uc_checkout, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    # ─── BĂNG 5: GANTT & NO-SHOW (y=840) ──────────────────────────────────────
    uc_gantt = d.add_uc("SƠ ĐỒ PHÒNG GANTT & XỬ LÝ NO-SHOW", 330, 850, 270, 65)
    d.add_assoc(act_rec, uc_gantt, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_gantt_matrix = d.add_uc("THEO DÕI MA TRẬN PHÒNG DÒNG THỜI GIAN", 710, 830, 270, 45)
    inc_noshow_row = d.add_uc("XỬ LÝ HỦY ĐƠN VẮNG MẶT (NO-SHOW)", 710, 885, 270, 45)
    d.add_inc(uc_gantt, inc_gantt_matrix, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_gantt, inc_noshow_row, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    ext_noshow_fee = d.add_uc("THU PHÍ PHẠT NO-SHOW", 1070, 885, 250, 45)
    d.add_ext(ext_noshow_fee, inc_noshow_row, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    return d


# ==============================================================================
# 04. PHÂN HỆ 04: VẬN HÀNH BUỒNG PHÒNG (HOUSEKEEPING)
# ==============================================================================
def build_04_housekeeping():
    d = BwDiagram(name="Phan He 04 - Van Hanh Buong Phong", width=1550, height=750)
    d.add_title("PHÂN HỆ 04: VẬN HÀNH BUỒNG PHÒNG (HOUSEKEEPING MANAGEMENT)",
                "Quản lý danh sách phòng bẩn, tiến trình dọn dẹp, kiểm định và bảo trì")

    d.add_boundary("RANH GIỚI PHÂN HỆ: VẬN HÀNH BUỒNG PHÒNG", 240, 90, 1060, 600)

    # Left Actor (Primary)
    act_hk = d.add_actor("NHÂN VIÊN BUỒNG PHÒNG\n(HOUSEKEEPER)", 70, 270)

    # Mother UC (Center)
    uc_hk = d.add_uc("QUẢN LÝ VỆ SINH BUỒNG PHÒNG", 360, 250, 270, 80)
    d.add_assoc(act_hk, uc_hk, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # Included UCs (Right Column x=760)
    inc_view_dirty = d.add_uc("XEM DANH SÁCH PHÒNG CẦN DỌN (DIRTY/OUT OF ORDER)", 760, 150, 280, 55)
    inc_assign_task = d.add_uc("TIẾP NHẬN PHÂN CÔNG VIỆC DỌN PHÒNG", 760, 245, 280, 55)
    inc_status_flow = d.add_uc("CẬP NHẬT TIẾN ĐỘ DỌN (DIRTY -> CLEANING -> CLEAN)", 760, 340, 280, 55)

    d.add_inc(uc_hk, inc_view_dirty, exit_pt=(1, 0.2), entry_pt=(0, 0.5))
    d.add_inc(uc_hk, inc_assign_task, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    d.add_inc(uc_hk, inc_status_flow, exit_pt=(1, 0.8), entry_pt=(0, 0.5))

    # Extends (Bố trí bên dưới thông thoáng, không đâm xuyên)
    ext_maint = d.add_uc("BÁO CÁO SỰ CỐ HƯ HỎNG VẬT TƯ / BẢO TRÌ PHÒNG", 360, 440, 270, 60)
    d.add_ext(ext_maint, uc_hk, exit_pt=(0.5, 0), entry_pt=(0.5, 1))

    ext_inspect = d.add_uc("NGHIỆM THU KIỂM ĐỊNH PHÒNG (INSPECTING)", 760, 440, 280, 60)
    d.add_ext(ext_inspect, uc_hk, exit_pt=(0, 0.5), entry_pt=(1, 0.75))

    return d


# ==============================================================================
# 05. PHÂN HỆ 05: QUẢN TRỊ DOANH THU, BẢNG GIÁ & BÁO CÁO
# ==============================================================================
def build_05_revenue_analytics():
    d = BwDiagram(name="Phan He 05 - Quan Tri Doanh Thu Va Bao Cao", width=1750, height=880)
    d.add_title("PHÂN HỆ 05: QUẢN TRỊ DOANH THU, BẢNG GIÁ & BÁO CÁO (REVENUE & ANALYTICS)",
                "Cấu hình giá linh hoạt, chính sách voucher, quản lý hạng phòng và báo cáo KPI")

    d.add_boundary("RANH GIỚI PHÂN HỆ: QUẢN TRỊ DOANH THU & BÁO CÁO", 240, 90, 1220, 750)

    # Left Actor (Primary)
    act_mgr = d.add_actor("QUẢN LÝ RESORT\n(HOTEL MANAGER)", 70, 390)

    # ─── HÀNG 1: QUẢN LÝ HẠNG PHÒNG (y=120) ──────────────────────────────────
    uc_type = d.add_uc("QUẢN LÝ DANH MỤC HẠNG PHÒNG & TIỆN NGHI", 330, 120, 270, 55)
    d.add_assoc(act_mgr, uc_type, exit_pt=(1, 0.5), entry_pt=(0, 0.5))

    # ─── HÀNG 2: PHÒNG VẬT LÝ & TẠM ĐÓNG (y=230) ─────────────────────────────
    uc_phys = d.add_uc("QUẢN LÝ DANH SÁCH PHÒNG VẬT LÝ", 330, 230, 270, 55)
    d.add_assoc(act_mgr, uc_phys, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    ext_block = d.add_uc("TẠM ĐÓNG PHÒNG ĐỂ BẢO TRÌ NÂNG CẤP", 710, 230, 270, 55)
    d.add_ext(ext_block, uc_phys, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    # ─── HÀNG 3: DYNAMIC PRICING & VOUCHER (y=370) ────────────────────────────
    uc_pricing = d.add_uc("THIẾT LẬP GIÁ LINH HOẠT THEO MÙA (DYNAMIC PRICING)", 330, 370, 270, 65)
    d.add_assoc(act_mgr, uc_pricing, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_daily_rates = d.add_uc("CẬP NHẬT BẢNG GIÁ THEO NGÀY (ROOM_RATES)", 710, 345, 270, 45)
    inc_holiday = d.add_uc("CẤU HÌNH PHỤ THU NGÀY LỄ VÀ CUỐI TUẦN", 710, 400, 270, 45)
    d.add_inc(uc_pricing, inc_daily_rates, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_pricing, inc_holiday, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    ext_bulk_price = d.add_uc("ÁP DỤNG BẢNG GIÁ HÀNG LOẠT THEO MÙA", 1070, 375, 250, 45)
    d.add_ext(ext_bulk_price, uc_pricing, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    # ─── HÀNG 4: PROMOTIONS / VOUCHER (y=520) ─────────────────────────────────
    uc_promo = d.add_uc("QUẢN LÝ MÃ GIẢM GIÁ VOUCHER (PROMOTIONS)", 330, 520, 270, 60)
    d.add_assoc(act_mgr, uc_promo, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_promo_cfg = d.add_uc("THIẾT LẬP TỶ LỆ CHIẾT KHẤU & HẠN DÙNG", 710, 495, 270, 45)
    inc_promo_atomic = d.add_uc("GIỚI HẠN LƯỢT DÙNG NGUYÊN TỬ (ATOMIC LIMIT)", 710, 550, 270, 45)
    d.add_inc(uc_promo, inc_promo_cfg, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_promo, inc_promo_atomic, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    # ─── HÀNG 5: KPI ANALYTICS & EXPORT (y=670) ───────────────────────────────
    uc_kpi = d.add_uc("XEM BÁO CÁO DOANH THU & TỶ LỆ LẤP ĐẦY (KPI)", 330, 670, 270, 65)
    d.add_assoc(act_mgr, uc_kpi, exit_pt=(1, 0.5), entry_pt=(0, 0.5))
    inc_kpi_calc = d.add_uc("TÍNH TOÁN CHỈ SỐ OCCUPANCY, REVPAR, ADR", 710, 645, 270, 45)
    inc_funnel = d.add_uc("PHÂN TÍCH PHỄU CHUYỂN ĐỔI MARKETING (UTM)", 710, 700, 270, 45)
    d.add_inc(uc_kpi, inc_kpi_calc, exit_pt=(1, 0.3), entry_pt=(0, 0.5))
    d.add_inc(uc_kpi, inc_funnel, exit_pt=(1, 0.7), entry_pt=(0, 0.5))

    ext_export = d.add_uc("XUẤT BÁO CÁO TÀI CHÍNH RA PDF / EXCEL", 1070, 675, 250, 45)
    d.add_ext(ext_export, uc_kpi, exit_pt=(0, 0.5), entry_pt=(1, 0.5))

    return d


# ==============================================================================
# HTML MASTER VIEWER & INDIVIDUAL HTML GENERATOR
# ==============================================================================
def generate_viewers(dest_dir, diagrams_dict):
    """Tạo file HTML Master Viewer và từng file HTML lẻ để mở trực tiếp trong trình duyệt."""
    items_html = []
    for filename, diag in diagrams_dict.items():
        xml_content = diag.to_xml()
        esc_xml = saxutils.escape(xml_content)
        title = diag.name
        html_single = filename.replace('.drawio', '.html')
        
        single_path = os.path.join(dest_dir, html_single)
        single_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Saigon Condao Resort OOAD</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
    <style>
        body {{ background-color: #f8fafc; font-family: Arial, Helvetica, sans-serif; }}
        .header-bar {{ background: #000000; color: #ffffff; padding: 20px 0; margin-bottom: 25px; }}
        .mxgraph {{ overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header-bar text-center">
        <h4 class="fw-bold mb-1">{title}</h4>
        <small class="text-white-50">Quy chuẩn OOAD Tiêu chuẩn Đồ án Điểm 10.0 • Primary Left / Secondary Right • No Bottom Actors</small>
        <div class="mt-2">
            <a href="viewer.html" class="btn btn-sm btn-outline-light me-2">&laquo; Quay lại Master Viewer</a>
            <a href="{filename}" download class="btn btn-sm btn-light">Tải tệp .drawio</a>
        </div>
    </div>
    <div class="container-fluid px-4">
        <div class="card shadow-sm border-dark">
            <div class="card-body bg-white text-center p-3">
                <div class="mxgraph" style="max-width:100%;border:1px solid #000;padding:15px;background:#ffffff;" 
                     data-mxgraph="{esc_xml}"></div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        with open(single_path, "w", encoding="utf-8") as sf:
            sf.write(single_content)
        print(f"[OK] Đã tạo HTML độc lập: {single_path}")

        items_html.append(f"""
        <div class="card mb-5 shadow-sm border-dark">
            <div class="card-header bg-black text-white d-flex justify-content-between align-items-center py-3">
                <h5 class="mb-0 fw-bold"><i class="bi bi-diagram-3-fill me-2"></i>{title}</h5>
                <div>
                    <a href="{html_single}" class="btn btn-sm btn-outline-light me-2" target="_blank">Mở tab riêng</a>
                    <a href="{filename}" download class="btn btn-sm btn-light">Tải .drawio</a>
                </div>
            </div>
            <div class="card-body bg-white text-center p-4">
                <div class="mxgraph" style="max-width:100%;border:1px solid #000;padding:15px;background:#ffffff;" 
                     data-mxgraph="{esc_xml}"></div>
            </div>
            <div class="card-footer bg-light text-dark small py-2 d-flex justify-content-between">
                <span><strong>Quy chuẩn:</strong> 100% Monochrome Black & White • Chuẩn Giáo trình UML: Primary Trái - Secondary Phải</span>
                <span>Tệp nguồn: <code>{filename}</code></span>
            </div>
        </div>
        """)

    master_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hồ Sơ Biểu Đồ Use Case Chuẩn Mực - Resort Sài Gòn Côn Đảo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
    <style>
        body {{ background-color: #f1f5f9; font-family: Arial, Helvetica, sans-serif; }}
        .header-bar {{ background: #000000; color: #ffffff; padding: 30px 0; margin-bottom: 35px; border-bottom: 3px solid #334155; }}
        .mxgraph {{ overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header-bar text-center">
        <h2 class="fw-bold tracking-wide">HỒ SƠ THIẾT KẾ BIỂU ĐỒ USE CASE CHUẨN MỰC OOAD (TIÊU CHUẨN ĐIỂM 10.0)</h2>
        <p class="mb-1 text-white-50">Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Saigon - Condao Resort)</p>
        <div class="mt-2">
            <span class="badge bg-light text-black me-2 px-3 py-2">100% Monochrome Black & White</span>
            <span class="badge bg-light text-black me-2 px-3 py-2">Primary Actor Trái - Secondary Phải</span>
            <span class="badge bg-light text-black px-3 py-2">Tuyệt đối không có Actor ở đáy</span>
        </div>
    </div>

    <div class="container-fluid px-5">
        {''.join(items_html)}
    </div>

    <footer class="text-center py-4 text-muted border-top mt-5 bg-white">
        <p class="mb-1"><strong>Hệ Thống Phân Tích Thiết Kế Hướng Đối Tượng (OOAD Standard)</strong></p>
        <small>Lead System Architect & Senior Lecturer Review Board | Saigon - Condao Islands Resort Platform</small>
    </footer>
</body>
</html>
"""
    viewer_path = os.path.join(dest_dir, "viewer.html")
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(master_html)
    print(f"[OK] Đã tạo Master HTML Viewer: {viewer_path}")


def main():
    dest_dirs = [
        os.path.join(os.getcwd(), 'diagrams', 'ooad_standard'),
        r'c:\HocC\Daily\ooad_standard'
    ]

    diagrams = {
        '00_So_Do_Use_Case_Tong_Quat.drawio': build_00_overview(),
        '01_Phan_He_Dat_Phong_Truc_Tuyen_B2C.drawio': build_01_b2c_booking(),
        '02_Phan_He_Tai_Khoan_Va_Phan_Quyen_RBAC.drawio': build_02_iam_rbac(),
        '03_Phan_He_Tac_Nghiep_Le_Tan_Tien_Sanh.drawio': build_03_front_desk(),
        '04_Phan_He_Van_Hanh_Buong_Phong.drawio': build_04_housekeeping(),
        '05_Phan_He_Quan_Tri_Doanh_Thu_Va_Bao_Cao.drawio': build_05_revenue_analytics(),
    }

    for ddir in dest_dirs:
        os.makedirs(ddir, exist_ok=True)
        print(f"\n>>> Đang xuất bản vào thư mục: {ddir}")
        for fname, d in diagrams.items():
            fpath = os.path.join(ddir, fname)
            d.save(fpath)
        generate_viewers(ddir, diagrams)

    print("\n[HOÀN TẤT] Toàn bộ 6 file .drawio và HTML Viewers đã được tạo thành công!")


if __name__ == '__main__':
    main()
