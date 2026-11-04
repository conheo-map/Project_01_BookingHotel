# Feature Specification: Data Integrity, Folio Billing & Payment Refactoring

**Feature Branch**: `002-data-integrity-and-payment-refactor`
**Created**: 2026-11-04
**Status**: In-Progress
**Feature Directory**: `specs/002-data-integrity-and-payment-refactor`

---

## Executive Summary & Scope

Giai đoạn 2 của quá trình tái cấu trúc hệ thống nhằm giải quyết triệt để các rủi ro toàn vẹn dữ liệu kế toán và phụ thuộc bắc cầu được phát hiện trong quá trình kiểm toán CSDL:
1. **Khử rủi ro phụ thuộc bắc cầu ở bảng `Payments`**: Chuẩn hóa luồng thanh toán xoay quanh `invoice_id`, bảo đảm tính nhất quán toàn vẹn giữa `Payments`, `Invoices` và `Booking_Master`.
2. **Cơ chế Tự động Đồng bộ Hóa đơn (*Single Source of Truth for Folio Invoices*)**: Xây dựng hàm tái tính toán tự động `recalculate_folio_invoice(booking_id)` - bất cứ khi nào phát sinh tiêu dùng dịch vụ minibar, ăn uống (`add_extra_service`) hoặc thay đổi phòng, hóa đơn `Invoices` tự động cập nhật lại tổng tiền chính xác từng đồng, ngăn chặn 100% lỗi lệch sổ sách kế toán.
3. **Chuẩn hóa Kiểu dữ liệu & Unicode Tiếng Việt**: Chuẩn hóa toàn bộ DDL SQL Server/SQLite hỗ trợ `nvarchar(100)` cho họ tên nhân viên (`Staff_Profiles.full_name`), khách hàng, và mã ký tự ASCII cho các trường mã định danh.

---

## User Scenarios & Testing

### User Story 1 - Tự động cập nhật Hóa đơn khi phát sinh Dịch vụ (Priority: P1)
Khách đang lưu trú tại phòng phát sinh thêm dịch vụ (ví dụ: giặt ủi, minibar). Lễ tân ghi nhận dịch vụ vào hệ thống. Hệ thống lập tức cập nhật bản ghi dịch vụ và tự động tính lại tổng tiền trong Hóa đơn `Invoices` tương ứng:
$$\text{final\_amount} = \text{room\_subtotal} + \text{service\_subtotal} + \text{tax\_vat\_amount} - \text{deposit\_deducted}$$
Khi in hóa đơn Check-out, số tiền phải thu hoàn toàn khớp với chi tiết dịch vụ.

* **Acceptance Scenario**:
  1. **Given** Đơn đặt phòng có tiền phòng 2.000.000đ, đã cọc 1.000.000đ, **When** Lễ tân thêm 2 chai nước suối (40.000đ), **Then** Bảng kê dịch vụ tăng 40.000đ, Hóa đơn `Invoices.total_amount` tự động cập nhật thành 1.040.000đ còn lại cần thanh toán.

### User Story 2 - Thanh toán chuẩn hóa gắn với Hóa đơn (Priority: P1)
Khi khách thanh toán cọc hoặc thanh toán quyết toán Check-out, bản ghi `Payments` bắt buộc phải tham chiếu chính xác đến `invoice_id` tương ứng, loại bỏ tình trạng ghi nhận thanh toán mồ côi hoặc sai lệch đơn hàng.

* **Acceptance Scenario**:
  1. **Given** Hóa đơn `INV-20261104-001` thuộc `Booking #10`, **When** Thực hiện thanh toán quyết toán 1.040.000đ, **Then** Bản ghi `Payments` được tạo với `invoice_id` trỏ đúng vào `INV-20261104-001`, trạng thái thanh toán là `Completed`.

---

## Functional Requirements (FR)

* **FR-010**: Hệ thống MUST cung cấp hàm `recalculate_folio_invoice(cursor, booking_id)` để đồng bộ tức thì số tiền phòng, tiền dịch vụ, thuế và cấn trừ cọc vào bảng `Invoices`.
* **FR-011**: Hàm `add_extra_service()` MUST tự động kích hoạt `recalculate_folio_invoice()` ngay trong cùng một Transaction để đảm bảo tính nguyên tử (Atomicity).
* **FR-012**: Bảng `Payments` MUST lưu trữ `invoice_id` và xác thực tính hợp lệ với `booking_id` để loại bỏ phụ thuộc bắc cầu.
* **FR-013**: Toàn bộ DDL trong `schema_refactored_3nf.sql` MUST sử dụng `nvarchar(100)` cho `Staff_Profiles.full_name`.
