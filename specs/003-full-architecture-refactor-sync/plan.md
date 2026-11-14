# Implementation Plan: Full 4-Tier Architecture Refactoring & OOAD Synchronization

**Feature**: `003-full-architecture-refactor-sync`  
**Spec Document**: `specs/003-full-architecture-refactor-sync/spec.md`  
**Reference Diagram**: `C:\Users\Cuong\Downloads\Tong_Hop_Bieu_Do.drawio` (ERD, Trang-13 Domain Class, SD-01 to SD-05)  
**Status**: In Progress

---

## 1. Architecture Overview (4-Tier Target Model)

```
[ FRONTEND UI LAYER (Port 5001) ]
  ├── B2C Portal: Countdown 15:00 Timer, VietQR Modal, Client Polling (/api/payments/status)
  ├── FrontDesk Gantt: Real-time room status colors, Check-in Modal, Room Allocation Suggestion
  └── Housekeeping Mobile: Quick status toggle (DIRTY -> IN_PROGRESS -> CLEAN), Maintenance reporting
          │ HTTP JSON API
          ▼
[ BOUNDARY / ROUTE HANDLERS LAYER (Port 5000) ]
  ├── auth_routes.py (< 20 lines/handler)
  ├── room_routes.py (Query rooms, room types, availability)
  ├── booking_routes.py (Refactored down from 1200 lines to ~150 lines)
  ├── housekeeping_routes.py (Mobile status updates, maintenance ticket creation)
  └── payment_routes.py (Webhook/IPN listener, client polling handler)
          │ Method Invocations
          ▼
[ SERVICE LAYER (CORE BUSINESS LOGIC) ]
  ├── RoomHoldLockService (Concurrency lock, TTL 15 mins, Total - Sold - ActiveLocks)
  ├── PaymentService (VietQR string generation, Webhook IPN, HMAC-SHA512 verification, HTTP 200)
  ├── RoomAllocationService (CLEAN & VACANT physical room search algorithm)
  ├── ServiceConsumptionService (Post extra charges: minibar, laundry, F&B to active stay)
  ├── CheckoutSettlementService (Triple reconciliation: Room + Services - Deposit = Balance, VAT invoice)
  └── HousekeepingService (Room lifecycle: OCCUPIED -> DIRTY -> IN_PROGRESS -> CLEAN / MAINTENANCE)
          │ ORM / Data Mapping
          ▼
[ DOMAIN ENTITY & REPOSITORY LAYER ]
  └── 15 Domain Models (.BackEnd/models/):
      Account, CustomerProfile, StaffProfile, Role, RoomType, PhysicalRoom,
      RoomHoldLock, Booking, BookingNight, ServiceItem, ServiceConsumption,
      FolioInvoice, PaymentTransaction, HousekeepingLog, MaintenanceTicket
          │ SQLite WAL Mode (Foreign Keys Enforced)
          ▼
[ DATABASE TIER (15 TABLES 3NF) ]
  └── database/schema_saigon_condao_3nf.sql
```

---

## 2. Phase-by-Phase Technical Strategy

### Phase 1: Database Tier 3NF Realignment & Migration
1. Align SQLite database `HotelBooking.db` with `database/schema_saigon_condao_3nf.sql` (15 tables).
2. Fix Foreign Key cascading rules and deletion order in teardowns (`Payments` -> `Invoices` -> `Service_Consumptions` -> `Booking_Nights` -> `Bookings`).
3. Ensure Nullable `customer_id` in `Bookings` for Walk-in support.

### Phase 2: Domain Entity Model Classes (.BackEnd/models/)
1. Create Python OOP classes in `.BackEnd/models/` for all 15 entities.
2. Encapsulate business validation and state transitions directly in Entity methods.

### Phase 3: Service Layer Refactoring & Extension
1. Update `room_lock_service.py` to match SD-01 (`expiresAt = now + 15m`, atomic availability check).
2. Create/Refactor `payment_service.py`: Webhook IPN processing, transaction logging into `PaymentTransaction`, HTTP 200 OK return, and status polling.
3. Refactor `checkin_service.py` (`RoomAllocationService`): Room allocation per night in `BookingNight`, enforce `CLEAN` requirement.
4. Enhance `checkout_service.py`: Add Minibar intake before settlement, enforce formula: $\text{Balance} = \text{Room} + \text{Services} - \text{Deposit}$.
5. Create `housekeeping_service.py`: State machine for room hygiene and maintenance ticket dispatching.

### Phase 4: Route Handlers Thinning (Slenderizing Controllers)
1. Rewrite `booking_routes.py` to route all logic through Service methods.
2. Add endpoints:
   - `POST /api/rooms/hold-lock`: Create 15-minute lock.
   - `POST /api/payments/webhook`: External VNPAY webhook listener.
   - `GET /api/payments/status/<lock_id>`: Client polling endpoint.
   - `POST /api/housekeeping/status`: Room clean status toggle.
   - `POST /api/housekeeping/maintenance`: Report broken facility.

### Phase 5: Frontend UI & Jinja2 Template Integration
1. Register `format_vnd` Jinja2 filter in `FrontEnd/app.py`.
2. Connect Homepage `/` and `/search` route handlers properly.
3. Verify all 20 tests pass with 0 failures and 0 errors.

---

## 3. Risk Mitigation & Verification Plan

| Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Foreign Key Deletion Constraint Violation** | Test teardowns fail with `sqlite3.IntegrityError` | Order deletion from child tables to parent tables (`Payments` -> `Invoices` -> `Booking_Nights` -> `Bookings`). |
| **Race Condition on 15-Min Lock** | Multiple bookings for same room | Use SQLite `BEGIN IMMEDIATE TRANSACTION` during availability check and lock insert. |
| **Webhook Delivery Latency** | UI hangs waiting for result | Client Polling with 15-minute timeout fallback to release lock. |
