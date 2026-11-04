# Tasks: Data Integrity, Folio Billing & Payment Refactoring

**Input**: Design documents from `/specs/002-data-integrity-and-payment-refactor/`
**Target Workspace**: `C:\HocC\Project_Booking - Sao chép\`
**Status**: 100% Completed & Verified

---

## Phase 1: Folio Invoices Auto-Synchronization (Single Source of Truth)

- [x] T001 Xây dựng hàm `recalculate_folio_invoice(cursor, booking_id)` trong `services/checkout_service.py` để tính toán tự động: Room + Service + Tax - Deposit
- [x] T002 Cập nhật hàm `add_extra_service()` trong `services/booking_service.py`: Tự động gọi `recalculate_folio_invoice()` ngay khi thêm dịch vụ minibar / ăn uống
- [x] T003 Cập nhật hàm `process_checkout()` trong `services/checkout_service.py`: Luôn kiểm tra đối soát với `recalculate_folio_invoice()` trước khi chốt thanh toán

---

## Phase 2: Transitive Dependency Elimination & Payment Linking

- [x] T004 Bổ sung cột `invoice_id` vào bảng `Payments`, thực hiện backfill dữ liệu lịch sử và cập nhật luồng lưu `Payments` trong `booking_service.py` và `checkout_service.py` để luôn ghi nhận `invoice_id`
- [x] T005 Xác thực ràng buộc tính nhất quán: `payment.booking_id` khớp hoàn toàn với `invoice.booking_id`, triệt tiêu 100% rủi ro phụ thuộc bắc cầu

---

## Phase 3: DDL Standardization & Automated Verification

- [x] T006 Cập nhật `schema_refactored_3nf.sql`: Đổi `Staff_Profiles.full_name` sang `nvarchar(100)`, chuẩn hóa liên kết `Payments(invoice_id)`
- [x] T007 Viết và chạy bộ kiểm thử tự động `test_data_integrity_and_payments.py`:
  - Kịch bản thêm dịch vụ minibar $\rightarrow$ Hóa đơn `Invoices` tự động tăng tiền
  - Kịch bản thanh toán cọc và quyết toán $\rightarrow$ Bản ghi `Payments` lưu đúng `invoice_id`, tổng tiền thanh toán khớp 100% với tổng hóa đơn
