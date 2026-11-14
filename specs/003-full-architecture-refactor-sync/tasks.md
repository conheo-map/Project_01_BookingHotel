# Tasks: Full 4-Tier Architecture Refactoring & OOAD Synchronization

**Feature**: `003-full-architecture-refactor-sync`  
**Spec Document**: `specs/003-full-architecture-refactor-sync/spec.md`  
**Plan Document**: `specs/003-full-architecture-refactor-sync/plan.md`  
**Status**: Ready for Execution

---

## Task List (Dependency Ordered)

### Phase 1: Database Tier 3NF & Schema Fixes
- [x] **Task 1.1**: Verify and apply 15 tables from `database/schema_saigon_condao_3nf.sql` into SQLite `HotelBooking.db`.
- [x] **Task 1.2**: Fix foreign key deletion order in test teardowns (`test_api_endpoints.py`, `test_services_smoke.py`) to eliminate `sqlite3.IntegrityError: FOREIGN KEY constraint failed`.
- [x] **Task 1.3**: Ensure `customer_id` is nullable in `Bookings` table for Walk-in support without dummy emails.

### Phase 2: Domain Entity Model Classes (.BackEnd/models/)
- [x] **Task 2.1**: Implement `Account`, `CustomerProfile`, `StaffProfile`, `Role` in `.BackEnd/models/account.py`.
- [x] **Task 2.2**: Implement `RoomType`, `PhysicalRoom`, `RoomHoldLock` in `.BackEnd/models/room.py`.
- [x] **Task 2.3**: Implement `Booking`, `BookingNight` in `.BackEnd/models/booking.py`.
- [x] **Task 2.4**: Implement `ServiceItem`, `ServiceConsumption`, `FolioInvoice`, `PaymentTransaction` in `.BackEnd/models/finance.py`.
- [x] **Task 2.5**: Implement `HousekeepingLog`, `MaintenanceTicket` in `.BackEnd/models/operations.py`.

### Phase 3: Service Layer Refactoring & Extension
- [x] **Task 3.1**: Extend `RoomHoldLockService` (`room_lock_service.py`) for 15-minute lock creation and atomic availability check `[Total - Sold - ActiveLocks]`.
- [x] **Task 3.2**: Implement `PaymentService` (`payment_service.py`) supporting VietQR generation, Webhook IPN handling with HTTP 200 return, and client polling endpoint.
- [x] **Task 3.3**: Refactor `RoomAllocationService` (`checkin_service.py`) to assign physical rooms to individual `BookingNight` records and enforce `CLEAN & VACANT` status.
- [x] **Task 3.4**: Implement `ServiceConsumptionService` to record extra charges during guest stay before invoice issuance.
- [x] **Task 3.5**: Refactor `CheckoutSettlementService` (`checkout_service.py`) to reconcile `Room + Services - Deposit = Balance`, issue VAT Invoice, and set room to `DIRTY`.
- [x] **Task 3.6**: Implement `HousekeepingService` (`housekeeping_service.py`) for room cleaning transitions (`DIRTY -> IN_PROGRESS -> CLEAN`) and automatic `MaintenanceTicket` creation.

### Phase 4: Route Handlers Thinning (Boundary Controllers)
- [x] **Task 4.1**: Refactor `booking_routes.py` to delegate 100% of business logic to services (< 20 lines per route handler).
- [x] **Task 4.2**: Add Webhook and status polling endpoints in `.BackEnd/routes/payment_routes.py` or `booking_routes.py`.
- [x] **Task 4.3**: Add Housekeeping and Maintenance reporting endpoints in `.BackEnd/routes/housekeeping_routes.py`.

### Phase 5: Frontend UI & Jinja2 Template Integration
- [x] **Task 5.1**: Register `format_vnd` template filter in `FrontEnd/app.py`.
- [x] **Task 5.2**: Fix frontend route mounting in `FrontEnd/app.py` for `/` and `/search` to resolve 404 test failures.
- [x] **Task 5.3**: Add 15:00 countdown timer and client polling script in checkout template.

### Phase 6: Full Verification & Automated Testing
- [x] **Task 6.1**: Run `pytest tests/` and verify all tests pass with 0 failures and 0 errors.
- [x] **Task 6.2**: Run E2E lifecycle test `test_e2e_full_lifecycle.py` verifying complete flow from hold-lock to checkout.
