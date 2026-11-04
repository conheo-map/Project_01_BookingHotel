"""
Generator for CAD-Standard OOAD Sequence Diagrams (Grade 10.0 University Defense Standard)
Architecture: BCE (Boundary - Control - Entity) Pattern
Project: Saigon - Condao Islands Resort Booking Platform
Strict Constraints:
- 100% Monochrome Black & White (#FFFFFF background, #000000 strokes/text). Zero colors.
- Strict Layer Separation: Actor <-> Boundary <-> Control <-> Entity (No BCE Leapfrogging).
- Explicit Activation Bars (Width 12px) for every execution context.
- Synchronous calls: Solid line with filled arrow (endArrow=block;endFill=1).
- Return messages: Dashed line with open arrow (endArrow=open;dashed=1;endFill=0).
- Combined Fragments: Standard Alt frames with [Guard Conditions].
- Strict XML Attribute Escaping including double-quotes (&quot;).
- Strict UTF-8 without BOM.
"""

import os
import sys
import xml.sax.saxutils as saxutils

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def xml_escape(text):
    return saxutils.escape(str(text), {'"': '&quot;'})

# Typography and Styling Constants (100% Monochrome B&W)
STYLE_TITLE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;"
STYLE_SUBTITLE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;fontStyle=2;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;"

STYLE_ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;fontFamily=Arial,Helvetica,sans-serif;fontColor=#000000;align=center;"
STYLE_BOUNDARY = "shape=umlBoundary;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;fontFamily=Arial,Helvetica,sans-serif;fontColor=#000000;align=center;"
STYLE_CONTROL = "shape=umlControl;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;fontFamily=Arial,Helvetica,sans-serif;fontColor=#000000;align=center;"
STYLE_ENTITY = "shape=umlEntity;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;fontFamily=Arial,Helvetica,sans-serif;fontColor=#000000;align=center;"

STYLE_LIFELINE = "endArrow=none;dashed=1;html=1;rounded=0;strokeColor=#000000;strokeWidth=1.2;"
STYLE_ACTIVATION = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.2;"

STYLE_CALL = "endArrow=block;endFill=1;html=1;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;fontStyle=1;verticalAlign=bottom;labelBackgroundColor=#FFFFFF;"
STYLE_RETURN = "endArrow=open;dashed=1;endFill=0;html=1;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;fontStyle=2;verticalAlign=bottom;labelBackgroundColor=#FFFFFF;"
STYLE_CREATE = "endArrow=open;dashed=1;endFill=0;html=1;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;fontStyle=1;verticalAlign=bottom;labelBackgroundColor=#FFFFFF;"

STYLE_FRAME_ALT = "shape=umlFrame;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1.5;width=45;height=22;fontStyle=1;fontSize=11;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;"
STYLE_DIVIDER = "line;strokeWidth=1.2;dashed=1;labelBackgroundColor=none;strokeColor=#000000;html=1;"
STYLE_GUARD = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontStyle=3;fontColor=#000000;fontFamily=Arial,Helvetica,sans-serif;"


class BwSequenceDiagram:
    def __init__(self, name="Sequence-1", width=1800, height=1050):
        self.name = name
        self.width = width
        self.height = height
        self.cells = []
        self.seq = 2
        self.lifelines = {}

    def next_id(self):
        cid = f"cell_{self.seq}"
        self.seq += 1
        return cid

    def add_title(self, title_text, subtitle_text="Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo"):
        cid_t = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid_t}" value="{xml_escape(title_text)}" style="{STYLE_TITLE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="40" y="24" width="1200" height="30" as="geometry" />\n'
            f'</mxCell>'
        )
        cid_s = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid_s}" value="{xml_escape(subtitle_text)}" style="{STYLE_SUBTITLE}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="40" y="52" width="1200" height="20" as="geometry" />\n'
            f'</mxCell>'
        )

    def add_participant(self, p_id, label, p_type, center_x, top_y=90, bottom_y=950):
        cid_head = self.next_id()
        cid_line = self.next_id()

        if p_type == "actor":
            w, h = 45, 75
            style = STYLE_ACTOR
            hx = center_x - w // 2
            hy = top_y
            line_start_y = top_y + h + 20
        elif p_type == "boundary":
            w, h = 45, 45
            style = STYLE_BOUNDARY
            hx = center_x - w // 2
            hy = top_y
            line_start_y = top_y + h + 25
        elif p_type == "control":
            w, h = 45, 45
            style = STYLE_CONTROL
            hx = center_x - w // 2
            hy = top_y
            line_start_y = top_y + h + 25
        elif p_type == "entity":
            w, h = 45, 45
            style = STYLE_ENTITY
            hx = center_x - w // 2
            hy = top_y
            line_start_y = top_y + h + 25
        else:
            w, h = 100, 40
            style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.5;fontStyle=1;fontSize=11;"
            hx = center_x - w // 2
            hy = top_y
            line_start_y = top_y + h

        self.cells.append(
            f'<mxCell id="{cid_head}" value="{xml_escape(label)}" style="{style}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{hx}" y="{hy}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )

        self.cells.append(
            f'<mxCell id="{cid_line}" style="{STYLE_LIFELINE}" edge="1" parent="1">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'    <mxPoint x="{center_x}" y="{line_start_y}" as="sourcePoint" />\n'
            f'    <mxPoint x="{center_x}" y="{bottom_y}" as="targetPoint" />\n'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )

        self.lifelines[p_id] = {
            "center_x": center_x,
            "head_id": cid_head,
            "line_id": cid_line,
            "p_type": p_type,
            "top_y": top_y,
            "line_start_y": line_start_y,
            "bottom_y": bottom_y
        }
        return p_id

    def add_activation(self, p_id, y_start, y_end):
        cid = self.next_id()
        cx = self.lifelines[p_id]["center_x"]
        w = 12
        h = y_end - y_start
        x = cx - w // 2
        self.cells.append(
            f'<mxCell id="{cid}" value="" style="{STYLE_ACTIVATION}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y_start}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        return cid

    def add_call(self, from_id, to_id, y, message):
        cid = self.next_id()
        cx_from = self.lifelines[from_id]["center_x"]
        cx_to = self.lifelines[to_id]["center_x"]

        if cx_from < cx_to:
            x_start = cx_from + 6
            x_end = cx_to - 6
        else:
            x_start = cx_from - 6
            x_end = cx_to + 6

        self.cells.append(
            f'<mxCell id="{cid}" value="{xml_escape(message)}" style="{STYLE_CALL}" edge="1" parent="1">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'    <mxPoint x="{x_start}" y="{y}" as="sourcePoint" />\n'
            f'    <mxPoint x="{x_end}" y="{y}" as="targetPoint" />\n'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def add_return(self, from_id, to_id, y, message):
        cid = self.next_id()
        cx_from = self.lifelines[from_id]["center_x"]
        cx_to = self.lifelines[to_id]["center_x"]

        if cx_from < cx_to:
            x_start = cx_from + 6
            x_end = cx_to - 6
        else:
            x_start = cx_from - 6
            x_end = cx_to + 6

        self.cells.append(
            f'<mxCell id="{cid}" value="{xml_escape(message)}" style="{STYLE_RETURN}" edge="1" parent="1">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'    <mxPoint x="{x_start}" y="{y}" as="sourcePoint" />\n'
            f'    <mxPoint x="{x_end}" y="{y}" as="targetPoint" />\n'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def add_self_call(self, p_id, y, message, height=25):
        cid = self.next_id()
        cx = self.lifelines[p_id]["center_x"]
        x_start = cx + 6
        x_loop = cx + 36

        style = "edgeStyle=orthogonalEdgeStyle;html=1;align=left;spacingLeft=5;endArrow=block;endFill=1;rounded=0;strokeColor=#000000;strokeWidth=1.3;fontSize=10;fontFamily=Arial,Helvetica,sans-serif;fontStyle=1;labelBackgroundColor=#FFFFFF;"
        self.cells.append(
            f'<mxCell id="{cid}" value="{xml_escape(message)}" style="{style}" edge="1" parent="1">\n'
            f'  <mxGeometry relative="1" as="geometry">\n'
            f'    <mxPoint x="{x_start}" y="{y}" as="sourcePoint" />\n'
            f'    <mxPoint x="{x_start}" y="{y + height}" as="targetPoint" />\n'
            f'    <Array as="points">\n'
            f'      <mxPoint x="{x_loop}" y="{y}" />\n'
            f'      <mxPoint x="{x_loop}" y="{y + height}" />\n'
            f'    </Array>\n'
            f'  </mxGeometry>\n'
            f'</mxCell>'
        )
        return cid

    def add_alt_frame(self, x, y, w, h, if_guard, else_guard=None, divider_y=None):
        cid_f = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid_f}" value="alt" style="{STYLE_FRAME_ALT}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'</mxCell>'
        )
        cid_g1 = self.next_id()
        self.cells.append(
            f'<mxCell id="{cid_g1}" value="{xml_escape(if_guard)}" style="{STYLE_GUARD}" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{x + 8}" y="{y + 24}" width="{w - 20}" height="20" as="geometry" />\n'
            f'</mxCell>'
        )

        if else_guard and divider_y:
            cid_div = self.next_id()
            self.cells.append(
                f'<mxCell id="{cid_div}" style="{STYLE_DIVIDER}" vertex="1" parent="1">\n'
                f'  <mxGeometry x="{x}" y="{divider_y}" width="{w}" height="10" as="geometry" />\n'
                f'</mxCell>'
            )
            cid_g2 = self.next_id()
            self.cells.append(
                f'<mxCell id="{cid_g2}" value="{xml_escape(else_guard)}" style="{STYLE_GUARD}" vertex="1" parent="1">\n'
                f'  <mxGeometry x="{x + 8}" y="{divider_y + 10}" width="{w - 20}" height="20" as="geometry" />\n'
                f'</mxCell>'
            )

    def to_xml(self):
        cells_xml = "\n        ".join(self.cells)
        esc_name = xml_escape(self.name)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-31T18:00:00.000Z" agent="Mozilla/5.0" version="24.0.0" type="device">
  <diagram id="saigon_condao_sequence" name="{esc_name}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width}" pageHeight="{self.height}" math="0" shadow="0">
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
# SD-01: QUY TRÌNH ĐẶT PHÒNG TRỰC TUYẾN & KHÓA PHÒNG CHỐNG TRÙNG (HOLD LOCK 15P)
# ==============================================================================
def build_sd_01_online_booking():
    sd = BwSequenceDiagram(name="SD-01 Quy Trinh Dat Phong Va Khoa Phong 15P", width=1750, height=1050)
    sd.add_title("SD-01: BIỂU ĐỒ TRÌNH TỰ ĐẶT PHÒNG TRỰC TUYẾN & KHÓA PHÒNG CHỐNG TRÙNG (BCE PATTERN)",
                 "Ca sử dụng: Khách hàng đặt phòng B2C, Khóa phòng chống trùng 15 phút, Thanh toán VNPAY/MoMo và Sinh mã PNR")

    # 1. Lifelines
    sd.add_participant("cust", "Khách hàng\n(Customer)", "actor", center_x=80, bottom_y=970)
    sd.add_participant("ui", ":BookingUI", "boundary", center_x=260, bottom_y=970)
    sd.add_participant("b_svc", ":BookingService", "control", center_x=470, bottom_y=970)
    sd.add_participant("r_inv", ":Room_Inventory", "entity", center_x=690, bottom_y=970)
    sd.add_participant("p_mod", ":PaymentGatewayModal", "boundary", center_x=910, bottom_y=970)
    sd.add_participant("p_svc", ":PaymentService", "control", center_x=1130, bottom_y=970)
    sd.add_participant("b_mst", ":Booking_Master", "entity", center_x=1340, bottom_y=970)
    sd.add_participant("b_ngt", ":Booking_Nights", "entity", center_x=1540, bottom_y=970)
    sd.add_participant("gw", "Cổng thanh toán\n(VNPAY/MoMo)", "actor", center_x=1680, bottom_y=970)

    # 2. Activations
    sd.add_activation("cust", 190, 930)
    sd.add_activation("ui", 190, 480)
    sd.add_activation("b_svc", 220, 450)
    sd.add_activation("r_inv", 250, 410)
    sd.add_activation("p_mod", 490, 620)
    sd.add_activation("p_svc", 520, 780)
    sd.add_activation("gw", 580, 670)
    sd.add_activation("b_svc", 700, 890)
    sd.add_activation("b_mst", 730, 770)
    sd.add_activation("b_ngt", 790, 820)
    sd.add_activation("r_inv", 840, 870)
    sd.add_activation("ui", 880, 930)

    # 3. Messages
    sd.add_call("cust", "ui", 190, "1: Chọn loại phòng, ngày đến/đi, số khách & bấm Đặt phòng")
    sd.add_call("ui", "b_svc", 220, "2: holdLockRooms(roomTypeId, checkIn, checkOut, customerId)")
    sd.add_call("b_svc", "r_inv", 250, "3: checkAvailability(roomTypeId, checkIn, checkOut)")
    sd.add_return("r_inv", "b_svc", 280, "3.1: status (AVAILABLE / LOCKED)")

    # Khung Alt
    sd.add_alt_frame(
        x=200, y=300, w=1500, h=640,
        if_guard="[Phòng còn trống & Chưa bị giữ chỗ]",
        else_guard="[Hết phòng hoặc phòng đang bị giữ chỗ trong 15 phút]",
        divider_y=420
    )

    # Nhánh Else
    sd.add_return("b_svc", "ui", 440, "3.2a: throw RoomAlreadyLockedError('Phòng đang bị giữ chỗ')")
    sd.add_return("ui", "cust", 460, "Hiển thị thông báo: Phòng đang có người giữ chỗ, vui lòng thử lại sau!")

    # Nhánh If
    sd.add_call("b_svc", "r_inv", 330, "4: acquireHoldLock(roomTypeId, dates, expireSeconds=900)")
    sd.add_return("r_inv", "b_svc", 360, "4.1: return lockId, expiresAt (Lock 15 phút)")
    sd.add_return("b_svc", "ui", 390, "4.2: return holdSuccess(lockId, timeout=900s)")
    sd.add_return("ui", "cust", 410, "Hiển thị đếm ngược 15:00 & Mở biểu mẫu thanh toán")

    sd.add_call("cust", "p_mod", 490, "5: Bấm 'Xác nhận & Thanh toán ngay'")
    sd.add_call("p_mod", "p_svc", 520, "6: createPaymentUrl(lockId, amount, method='VNPAY')")
    sd.add_call("p_svc", "gw", 550, "7: requestPaymentGateway(orderInfo, amount, returnUrl)")
    sd.add_return("gw", "p_mod", 580, "7.1: redirectPaymentGatewayPage(paymentUrl)")
    sd.add_call("cust", "gw", 610, "8: Quét mã VNPAY-QR / Xác thực OTP ngân hàng")
    sd.add_return("gw", "cust", 640, "8.1: Thông báo giao dịch trừ tiền thành công")

    sd.add_call("gw", "p_svc", 670, "9: verifyPaymentWebhook(transId, code='00', secureHash)")
    sd.add_call("p_svc", "b_svc", 700, "10: confirmBookingAfterPayment(lockId, transId)")

    sd.add_call("b_svc", "b_mst", 730, "11: createBookingRecord(PNR, customerId, status='CONFIRMED')")
    sd.add_return("b_mst", "b_svc", 760, "11.1: return bookingId, PNR")

    sd.add_call("b_svc", "b_ngt", 790, "12: createBookingNights(bookingId, checkIn, checkOut, price)")
    sd.add_return("b_ngt", "b_svc", 820, "12.1: return nightsCreated")

    sd.add_call("b_svc", "r_inv", 840, "13: releaseHoldLockAndDeductInventory(lockId, roomTypeId)")
    sd.add_return("r_inv", "b_svc", 870, "13.1: return inventoryDeducted")

    sd.add_self_call("b_svc", 875, "14: sendConfirmationEmail(PNR, email)")

    sd.add_return("b_svc", "ui", 900, "15: return bookingSuccess(PNR, receiptUrl)")
    sd.add_return("ui", "cust", 930, "Hiển thị Voucher xác nhận đặt phòng & Mã PNR thành công")

    return sd


# ==============================================================================
# SD-02: QUY TRÌNH TIẾP NHẬN & LÀM THỦ TỤC NHẬN PHÒNG (CHECK-IN & ROOM ALLOCATION)
# ==============================================================================
def build_sd_02_check_in():
    sd = BwSequenceDiagram(name="SD-02 Quy Trinh Check-In Va Gan Phong", width=1650, height=950)
    sd.add_title("SD-02: BIỂU ĐỒ TRÌNH TỰ LÀM THỦ TỤC NHẬN PHÒNG (CHECK-IN & ROOM ALLOCATION)",
                 "Ca sử dụng: Nhân viên Lễ tân tra cứu PNR, Quét CCCD khách, Kiểm tra phòng CLEAN, Đổi sang OCCUPIED & Kích hoạt thẻ từ")

    # 1. Lifelines
    sd.add_participant("rec", "Nhân viên Lễ tân\n(Receptionist)", "actor", center_x=80, bottom_y=880)
    sd.add_participant("ui_gantt", ":FrontDeskGanttUI", "boundary", center_x=280, bottom_y=880)
    sd.add_participant("ui_modal", ":CheckInModal", "boundary", center_x=500, bottom_y=880)
    sd.add_participant("ctl_ci", ":CheckInController", "control", center_x=730, bottom_y=880)
    sd.add_participant("svc_alloc", ":RoomAllocationService", "control", center_x=970, bottom_y=880)
    sd.add_participant("en_mst", ":Booking_Master", "entity", center_x=1190, bottom_y=880)
    sd.add_participant("en_room", ":Physical_Rooms", "entity", center_x=1390, bottom_y=880)
    sd.add_participant("en_guest", ":Guest_Profiles", "entity", center_x=1560, bottom_y=880)

    # 2. Activations
    sd.add_activation("rec", 180, 850)
    sd.add_activation("ui_gantt", 180, 310)
    sd.add_activation("ctl_ci", 210, 300)
    sd.add_activation("en_mst", 240, 280)

    sd.add_activation("ui_modal", 340, 840)
    sd.add_activation("ctl_ci", 370, 820)
    sd.add_activation("en_guest", 400, 430)
    sd.add_activation("svc_alloc", 460, 560)
    sd.add_activation("en_room", 480, 540)
    sd.add_activation("en_mst", 660, 700)
    sd.add_activation("en_room", 720, 760)

    # 3. Messages
    sd.add_call("rec", "ui_gantt", 180, "1: Tra cứu mã PNR hoặc SĐT khách hàng")
    sd.add_call("ui_gantt", "ctl_ci", 210, "2: getBookingForCheckIn(PNR)")
    sd.add_call("ctl_ci", "en_mst", 240, "3: findBookingByPNR(PNR)")
    sd.add_return("en_mst", "ctl_ci", 270, "3.1: return bookingData (Loại phòng, ngày, trạng thái)")
    sd.add_return("ctl_ci", "ui_gantt", 300, "3.2: return bookingDetails")

    sd.add_call("rec", "ui_modal", 340, "4: Mở hộp thoại Check-in, quét/nhập CCCD khách lưu trú")
    sd.add_call("ui_modal", "ctl_ci", 370, "5: submitCheckIn(bookingId, guestIdentityData)")
    sd.add_call("ctl_ci", "en_guest", 400, "6: saveGuestProfile(guestIdentityData, cccdNumber)")
    sd.add_return("en_guest", "ctl_ci", 430, "6.1: return guestId")

    sd.add_call("ctl_ci", "svc_alloc", 460, "7: allocatePhysicalRoom(roomTypeId)")
    sd.add_call("svc_alloc", "en_room", 480, "8: findAvailableCleanRoom(roomTypeId)")
    sd.add_return("en_room", "svc_alloc", 510, "8.1: return roomList (Status & Cleanliness)")

    # Khung Alt
    sd.add_alt_frame(
        x=650, y=530, w=850, h=250,
        if_guard="[Có phòng vật lý trạng thái CLEAN & Trống]",
        else_guard="[Không có phòng sạch - Cần đợi Buồng phòng]",
        divider_y=610
    )

    # Nhánh Else
    sd.add_return("svc_alloc", "ctl_ci", 630, "8.2a: throw NoCleanRoomAvailableException('Chưa có phòng sạch')")

    # Nhánh If
    sd.add_return("svc_alloc", "ctl_ci", 560, "8.2b: return selectedRoomNumber = '302'")
    sd.add_call("ctl_ci", "en_mst", 660, "9: assignRoomToBooking(bookingId, roomNumber='302', status='CHECKED_IN')")
    sd.add_return("en_mst", "ctl_ci", 690, "9.1: return updateSuccess")

    sd.add_call("ctl_ci", "en_room", 720, "10: updateStatus(roomNumber='302', status='OCCUPIED')")
    sd.add_return("en_room", "ctl_ci", 750, "10.1: return statusUpdated")

    sd.add_self_call("ctl_ci", 760, "11: issueRfidKeycard(roomNumber='302', validUntil)")

    sd.add_return("ctl_ci", "ui_modal", 810, "12: return checkInSuccess(roomNumber, keycardActive=true)")
    sd.add_return("ui_modal", "rec", 840, "In phiếu nhận phòng, giao chìa khóa & Cập nhật màu phòng trên Gantt")

    return sd


# ==============================================================================
# SD-03: QUY TRÌNH GHI NHẬN TIÊU DÙNG DỊCH VỤ PHÁT SINH (MINIBAR, F&B, TOUR)
# ==============================================================================
def build_sd_03_extra_services():
    sd = BwSequenceDiagram(name="SD-03 Ghi Nhan Dich Vu Phat Sinh", width=1600, height=920)
    sd.add_title("SD-03: BIỂU ĐỒ TRÌNH TỰ GHI NHẬN TIÊU DÙNG DỊCH VỤ PHÁT SINH (BCE PATTERN)",
                 "Ca sử dụng: Nhân viên nhập order minibar/giặt ủi, Tra cứu đơn giá catalog, Tính thuế phí & Cập nhật vào công nợ phòng")

    # 1. Lifelines
    sd.add_participant("staff", "Nhân viên Lễ tân / Phục vụ\n(Staff)", "actor", center_x=80, bottom_y=850)
    sd.add_participant("ui_order", ":ServiceOrderUI", "boundary", center_x=300, bottom_y=850)
    sd.add_participant("svc_folio", ":FolioBillingService", "control", center_x=570, bottom_y=850)
    sd.add_participant("en_mst", ":Booking_Master", "entity", center_x=840, bottom_y=850)
    sd.add_participant("en_item", ":Service_Items", "entity", center_x=1080, bottom_y=850)
    sd.add_participant("en_cons", ":Service_Consumptions", "entity", center_x=1300, bottom_y=850)
    sd.add_participant("en_inv", ":Invoices", "entity", center_x=1500, bottom_y=850)

    # 2. Activations
    sd.add_activation("staff", 180, 810)
    sd.add_activation("ui_order", 180, 800)
    sd.add_activation("svc_folio", 210, 770)
    sd.add_activation("en_mst", 240, 280)
    sd.add_activation("en_item", 440, 480)
    sd.add_activation("en_cons", 560, 600)
    sd.add_activation("en_inv", 670, 720)

    # 3. Messages
    sd.add_call("staff", "ui_order", 180, "1: Nhập số phòng '302' và bấm Tra cứu hóa đơn phòng")
    sd.add_call("ui_order", "svc_folio", 210, "2: validateOccupiedRoom(roomNumber='302')")
    sd.add_call("svc_folio", "en_mst", 240, "3: getActiveBookingByRoom('302')")
    sd.add_return("en_mst", "svc_folio", 270, "3.1: return bookingInfo (status='CHECKED_IN')")
    sd.add_return("svc_folio", "ui_order", 300, "3.2: return roomValid(bookingId, guestName)")

    # Khung Alt
    sd.add_alt_frame(
        x=220, y=320, w=1340, h=480,
        if_guard="[Khách đang lưu trú hợp lệ tại phòng]",
        else_guard="[Phòng trống hoặc khách đã Check-out]",
        divider_y=380
    )

    # Nhánh Else
    sd.add_return("ui_order", "staff", 400, "Báo lỗi: Phòng hiện không có khách lưu trú!")

    # Nhánh If
    sd.add_call("staff", "ui_order", 350, "4: Chọn mặt hàng (2 Nước ngọt, 1 Giặt ủi) & Bấm Ghi nợ")
    sd.add_call("ui_order", "svc_folio", 420, "5: postServiceConsumption(bookingId, itemsList)")
    sd.add_call("svc_folio", "en_item", 440, "6: getItemPricesAndTax(itemIds)")
    sd.add_return("en_item", "svc_folio", 470, "6.1: return itemPrices, vatRate=10%")

    sd.add_self_call("svc_folio", 490, "7: calculateTotal(qty * unitPrice * 1.10)")

    sd.add_call("svc_folio", "en_cons", 560, "8: createConsumptionRecords(bookingId, items, totalAmount)")
    sd.add_return("en_cons", "svc_folio", 590, "8.1: return consumptionIds")

    sd.add_call("svc_folio", "en_inv", 670, "9: accumulateRoomFolio(bookingId, additionalAmount)")
    sd.add_return("en_inv", "svc_folio", 710, "9.1: return newFolioBalance")

    sd.add_return("svc_folio", "ui_order", 750, "10: return postSuccess(consumptionIds, newBalance)")
    sd.add_return("ui_order", "staff", 780, "In Phiếu ký nhận dịch vụ (Voucher) và cập nhật số dư công nợ")

    return sd


# ==============================================================================
# SD-04: QUY TRÌNH LÀM THỦ TỤC TRẢ PHÒNG & QUYẾT TOÁN HÓA ĐƠN (CHECK-OUT & INVOICING)
# ==============================================================================
def build_sd_04_check_out():
    sd = BwSequenceDiagram(name="SD-04 Quy Trinh Check-Out Va Quyet Toan", width=1750, height=980)
    sd.add_title("SD-04: BIỂU ĐỒ TRÌNH TỰ LÀM THỦ TỤC TRẢ PHÒNG & QUYẾT TOÁN (CHECK-OUT & INVOICING)",
                 "Ca sử dụng: Lễ tân nhận kết quả kiểm phòng, Tính tổng tiền (Phòng + Dịch vụ - Cọc), Quyết toán hóa đơn VAT & Đổi trạng thái sang DIRTY")

    # 1. Lifelines
    sd.add_participant("rec", "Nhân viên Lễ tân\n(Receptionist)", "actor", center_x=80, bottom_y=920)
    sd.add_participant("hk", "Nhân viên Buồng phòng\n(Housekeeper)", "actor", center_x=250, bottom_y=920)
    sd.add_participant("ui_bill", ":CheckOutBillingUI", "boundary", center_x=450, bottom_y=920)
    sd.add_participant("ctl_co", ":CheckOutController", "control", center_x=680, bottom_y=920)
    sd.add_participant("svc_inv", ":InvoiceSettlementService", "control", center_x=930, bottom_y=920)
    sd.add_participant("en_mst", ":Booking_Master", "entity", center_x=1160, bottom_y=920)
    sd.add_participant("en_inv", ":Invoices", "entity", center_x=1350, bottom_y=920)
    sd.add_participant("en_pay", ":Payments", "entity", center_x=1520, bottom_y=920)
    sd.add_participant("en_room", ":Physical_Rooms", "entity", center_x=1680, bottom_y=920)

    # 2. Activations
    sd.add_activation("rec", 180, 890)
    sd.add_activation("hk", 220, 270)
    sd.add_activation("ui_bill", 180, 880)
    sd.add_activation("ctl_co", 290, 860)
    sd.add_activation("svc_inv", 320, 840)
    sd.add_activation("en_mst", 350, 390)
    sd.add_activation("en_inv", 410, 450)
    sd.add_activation("en_pay", 590, 630)
    sd.add_activation("en_inv", 670, 710)
    sd.add_activation("en_mst", 740, 780)
    sd.add_activation("en_room", 800, 840)

    # 3. Messages
    sd.add_call("rec", "ui_bill", 180, "1: Khách báo trả phòng, Lễ tân gửi yêu cầu kiểm tra phòng '302'")
    sd.add_call("ui_bill", "hk", 210, "2: Thông báo yêu cầu kiểm tra phòng '302'")
    sd.add_return("hk", "ui_bill", 250, "2.1: Phản hồi kết quả: Minibar tiêu thụ 1 bia, phòng không hư hại")

    sd.add_call("rec", "ui_bill", 290, "3: Bấm 'Tính tổng quyết toán công nợ'")
    sd.add_call("ui_bill", "svc_inv", 320, "4: calculateFinalSettlement(bookingId)")
    sd.add_call("svc_inv", "en_mst", 350, "5: getBookingChargesAndDeposit(bookingId)")
    sd.add_return("en_mst", "svc_inv", 380, "5.1: return roomCharges, depositPaid")

    sd.add_call("svc_inv", "en_inv", 410, "6: getExtraServicesTotal(bookingId)")
    sd.add_return("en_inv", "svc_inv", 440, "6.1: return extraServiceCharges")

    sd.add_self_call("svc_inv", 460, "7: calculateBalance(room + extra - deposit)")
    sd.add_return("svc_inv", "ui_bill", 500, "8: return settlementSummary(totalDue, breakdown)")

    sd.add_call("rec", "ui_bill", 540, "9: Chọn phương thức (Tiền mặt/Quẹt thẻ POS) & Bấm Quyết toán")
    sd.add_call("ui_bill", "svc_inv", 570, "10: executeSettlement(bookingId, paymentMethod, amountPaid)")

    sd.add_call("svc_inv", "en_pay", 600, "11: recordPayment(bookingId, paymentMethod, amountPaid)")
    sd.add_return("en_pay", "svc_inv", 630, "11.1: return paymentId")

    sd.add_call("svc_inv", "en_inv", 670, "12: finalizeInvoice(bookingId, status='PAID', is_settled=1)")
    sd.add_return("en_inv", "svc_inv", 700, "12.1: return invoiceNumber, vatInvoicePdf")

    sd.add_call("svc_inv", "ctl_co", 730, "13: completeCheckOut(bookingId, roomNumber='302')")
    sd.add_call("ctl_co", "en_mst", 750, "14: updateBookingStatus(bookingId, status='CHECKED_OUT')")
    sd.add_return("en_mst", "ctl_co", 780, "14.1: return bookingUpdated")

    sd.add_call("ctl_co", "en_room", 800, "15: setRoomStatus(roomNumber='302', status='DIRTY')")
    sd.add_return("en_room", "ctl_co", 830, "15.1: return roomStatusDirty")

    sd.add_return("ctl_co", "ui_bill", 860, "16: return checkOutSuccess(invoicePdfUrl)")
    sd.add_return("ui_bill", "rec", 890, "In Hóa đơn tài chính VAT đưa khách & Phòng 302 tự động chuyển sang màu đỏ (DIRTY)")

    return sd


# ==============================================================================
# SD-05: QUY TRÌNH CẬP NHẬT TIẾN ĐỘ VỆ SINH BUỒNG PHÒNG (HOUSEKEEPING WORKFLOW)
# ==============================================================================
def build_sd_05_housekeeping():
    sd = BwSequenceDiagram(name="SD-05 Quy Trinh Don Buong Phong", width=1650, height=950)
    sd.add_title("SD-05: BIỂU ĐỒ TRÌNH TỰ VẬN HÀNH DỌN DẸP BUỒNG PHÒNG (HOUSEKEEPING WORKFLOW)",
                 "Ca sử dụng: Buồng phòng nhận phòng DIRTY, Cập nhật CLEANING, Kiểm tra hoàn tất chuyển sang CLEAN & Đồng bộ Lễ tân")

    # 1. Lifelines
    sd.add_participant("hk", "Nhân viên Buồng phòng\n(Housekeeper)", "actor", center_x=80, bottom_y=880)
    sd.add_participant("ui_mob", ":HousekeepingMobileUI", "boundary", center_x=310, bottom_y=880)
    sd.add_participant("svc_clean", ":RoomCleaningService", "control", center_x=590, bottom_y=880)
    sd.add_participant("en_room", ":Physical_Rooms", "entity", center_x=870, bottom_y=880)
    sd.add_participant("en_log", ":Cleaning_Logs", "entity", center_x=1140, bottom_y=880)
    sd.add_participant("ui_gantt", ":FrontDeskGanttUI", "boundary", center_x=1420, bottom_y=880)
    sd.add_participant("rec", "Nhân viên Lễ tân\n(Observer)", "actor", center_x=1580, bottom_y=880)

    # 2. Activations
    sd.add_activation("hk", 180, 850)
    sd.add_activation("ui_mob", 180, 840)
    sd.add_activation("svc_clean", 210, 810)
    sd.add_activation("en_room", 240, 280)
    sd.add_activation("en_room", 390, 430)
    sd.add_activation("en_log", 450, 490)
    sd.add_activation("en_room", 650, 690)
    sd.add_activation("en_log", 710, 750)
    sd.add_activation("ui_gantt", 770, 830)
    sd.add_activation("rec", 800, 830)

    # 3. Messages
    sd.add_call("hk", "ui_mob", 180, "1: Mở app di động, bấm 'Lấy danh sách phòng bẩn cần dọn'")
    sd.add_call("ui_mob", "svc_clean", 210, "2: getDirtyRoomsList(floorId)")
    sd.add_call("svc_clean", "en_room", 240, "3: queryRooms(status='DIRTY')")
    sd.add_return("en_room", "svc_clean", 270, "3.1: return dirtyRoomsList")
    sd.add_return("svc_clean", "ui_mob", 300, "3.2: return roomCards (Phòng 302, 305)")

    sd.add_call("hk", "ui_mob", 340, "4: Đến phòng 302, bấm 'Bắt đầu dọn phòng'")
    sd.add_call("ui_mob", "svc_clean", 370, "5: startCleaning(roomNumber='302', staffId)")
    sd.add_call("svc_clean", "en_room", 390, "6: updateStatus(roomNumber='302', status='CLEANING')")
    sd.add_return("en_room", "svc_clean", 420, "6.1: return statusUpdated")

    sd.add_call("svc_clean", "en_log", 450, "7: createCleaningLog(roomNumber='302', staffId, startTime=now)")
    sd.add_return("en_log", "svc_clean", 480, "7.1: return logId")
    sd.add_return("svc_clean", "ui_mob", 510, "8: return cleaningStarted(logId)")

    sd.add_call("hk", "ui_mob", 550, "9: Hoàn tất lau dọn & Thay ga nệm, bấm 'Báo cáo hoàn thành'")

    # Khung Alt
    sd.add_alt_frame(
        x=220, y=580, w=1400, h=250,
        if_guard="[Phòng đạt chuẩn vệ sinh & Đầy đủ tiện nghi]",
        else_guard="[Phát hiện hư hỏng vật tư - Chuyển sang Bảo trì]",
        divider_y=630
    )

    # Nhánh Else
    sd.add_return("ui_mob", "hk", 610, "Ghi nhận hỏng hóc, chuyển phòng sang 'MAINTENANCE' & Gọi kỹ thuật")

    # Nhánh If
    sd.add_call("ui_mob", "svc_clean", 630, "10: markRoomAsClean(roomNumber='302', logId, quality='PASSED')")
    sd.add_call("svc_clean", "en_room", 650, "11: updateStatus(roomNumber='302', status='AVAILABLE', is_clean=1)")
    sd.add_return("en_room", "svc_clean", 680, "11.1: return statusClean")

    sd.add_call("svc_clean", "en_log", 710, "12: closeCleaningLog(logId, endTime=now, result='CLEAN')")
    sd.add_return("en_log", "svc_clean", 740, "12.1: return logClosed")

    sd.add_call("svc_clean", "ui_gantt", 770, "13: notifyRoomStatusChanged(roomNumber='302', status='CLEAN')")
    sd.add_return("ui_gantt", "rec", 800, "Đổi màu phòng 302 sang Xanh lục (Clean) - Sẵn sàng đón khách Check-in!")

    sd.add_return("svc_clean", "ui_mob", 820, "14: return roomCleanSuccess()")
    sd.add_return("ui_mob", "hk", 840, "Thông báo: Đã hoàn tất vệ sinh phòng 302!")

    return sd


# ==============================================================================
# HTML MASTER VIEWER & INDIVIDUAL HTML GENERATOR
# ==============================================================================
def generate_viewers(dest_dir, diagrams_dict):
    items_html = []
    for filename, diag in diagrams_dict.items():
        xml_content = diag.to_xml()
        esc_xml = xml_escape(xml_content)
        title = diag.name
        html_single = filename.replace('.drawio', '.html')

        single_path = os.path.join(dest_dir, html_single)
        single_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Saigon Condao Resort Sequence Diagrams</title>
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
        <small class="text-white-50">Quy chuẩn OOAD Tiêu chuẩn Đồ án Điểm 10.0 • Kiến trúc BCE • 100% Monochrome Black & White</small>
        <div class="mt-2">
            <a href="viewer_sequence.html" class="btn btn-sm btn-outline-light me-2">&laquo; Quay lại Master Sequence Viewer</a>
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
                <h5 class="mb-0 fw-bold"><i class="bi bi-diagram-2-fill me-2"></i>{title}</h5>
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
                <span><strong>Kiến trúc:</strong> BCE Pattern (Boundary - Control - Entity) • Activation Bars • Combined Fragments [Alt]</span>
                <span>Tệp nguồn: <code>{filename}</code></span>
            </div>
        </div>
        """)

    master_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hồ Sơ Biểu Đồ Trình Tự BCE - Resort Sài Gòn Côn Đảo</title>
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
        <h2 class="fw-bold tracking-wide">HỒ SƠ THIẾT KẾ BIỂU ĐỒ TRÌNH TỰ (SEQUENCE DIAGRAMS - BCE ARCHITECTURE)</h2>
        <p class="mb-1 text-white-50">Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo (Saigon - Condao Resort)</p>
        <div class="mt-2">
            <span class="badge bg-light text-black me-2 px-3 py-2">100% Monochrome Black & White</span>
            <span class="badge bg-light text-black me-2 px-3 py-2">Kiến trúc 3 lớp BCE (Boundary - Control - Entity)</span>
            <span class="badge bg-light text-black px-3 py-2">Chuẩn UML 2.x Vạch kích hoạt & Khung Alt</span>
        </div>
    </div>

    <div class="container-fluid px-5">
        {''.join(items_html)}
    </div>

    <footer class="text-center py-4 text-muted border-top mt-5 bg-white">
        <p class="mb-1"><strong>Hệ Thống Phân Tích Thiết Kế Hướng Đối Tượng (OOAD Sequence Standard)</strong></p>
        <small>Lead System Architect & Senior Lecturer Review Board | Saigon - Condao Islands Resort Platform</small>
    </footer>
</body>
</html>
"""
    viewer_path = os.path.join(dest_dir, "viewer_sequence.html")
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(master_html)
    print(f"[OK] Đã tạo Master HTML Sequence Viewer: {viewer_path}")


def main():
    dest_dirs = [
        os.path.join(os.getcwd(), 'diagrams', 'sequence_bce'),
        r'c:\HocC\Daily\sequence_bce'
    ]

    diagrams = {
        'SD_01_Dat_Phong_Truc_Tuyen_Va_Khoa_Phong_15P.drawio': build_sd_01_online_booking(),
        'SD_02_Thu_Tuc_Nhan_Phong_Check_In.drawio': build_sd_02_check_in(),
        'SD_03_Ghi_Nhan_Tieu_Dung_Dich_Vu_Phat_Sinh.drawio': build_sd_03_extra_services(),
        'SD_04_Thu_Tuc_Tra_Phong_Va_Quyet_Toan_Check_Out.drawio': build_sd_04_check_out(),
        'SD_05_Cap_Nhat_Tien_Do_Ve_Sinh_Buong_Phong.drawio': build_sd_05_housekeeping(),
    }

    for ddir in dest_dirs:
        os.makedirs(ddir, exist_ok=True)
        print(f"\n>>> Đang xuất bản vào thư mục: {ddir}")
        for fname, d in diagrams.items():
            fpath = os.path.join(ddir, fname)
            d.save(fpath)
        generate_viewers(ddir, diagrams)

    print("\n[HOÀN TẤT] Toàn bộ 5 file Sequence Diagram .drawio và HTML Viewers đã được tạo thành công!")


if __name__ == '__main__':
    main()
