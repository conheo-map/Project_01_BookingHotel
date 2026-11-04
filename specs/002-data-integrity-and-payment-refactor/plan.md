# Implementation Plan: Data Integrity, Folio Billing & Payment Refactoring

**Branch**: `002-data-integrity-and-payment-refactor` | **Date**: 2026-11-04 | **Spec**: [specs/002-data-integrity-and-payment-refactor/spec.md](spec.md)

---

## 1. Technical Context

* **Ngôn ngữ**: Python 3.10+ / SQLite 3 WAL Mode
* **Mục tiêu**: Xóa bỏ Transitive Dependency ở Payments, xây dựng cơ chế tự động đồng bộ Folio Invoices (Single Source of Truth), chuẩn hóa DDL Unicode.

---

## 2. Technical Design & Architecture

### A. Tự động đồng bộ Folio Billing (`services/checkout_service.py`)
Xây dựng hàm:
```python
def recalculate_folio_invoice(cursor, booking_id: int) -> Dict[str, int]:
  # 1. Tính room_subtotal = SUM(night_price) từ Booking_Nights
  # 2. Tính service_subtotal = SUM(quantity * unit_price) từ Extra_Services
  # 3. Lấy discount_amount, deposit_paid từ Booking_Master
  # 4. Tính tax_vat_amount = (room_subtotal + service_subtotal - discount) * 10%
  # 5. Tính final_amount = (room_subtotal + service_subtotal - discount + tax) - deposit_paid
  # 6. UPDATE Invoices SET total_amount = final_amount WHERE booking_id = ?
```

### B. Liên kết chặt chẽ `Payments` với `Invoices`
Trong hàm `process_checkout` và `create_online_booking`:
- Khi lưu `Payments`: Truy vấn `invoice_id` từ bảng `Invoices` theo `booking_id`.
- Lưu `invoice_id` vào `Payments.invoice_id`, bảo đảm 100% các khoản thanh toán đều có hóa đơn đối soát.

### C. Chuẩn hóa DDL Unicode trong `schema_refactored_3nf.sql`
- Sửa `full_name` trong `Staff_Profiles` thành `nvarchar(100)`
- Cập nhật ràng buộc ngoại `Payments.invoice_id REFERENCES Invoices(invoice_id)`
