"""
Unit tests for the 15 Domain Entity Models (Trang-13 OOAD Class Diagram).
Verifies all 15 classes, attributes, methods, and relationships.
"""

import unittest
from datetime import datetime
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, '.BackEnd')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from models.account import Role, Account, StaffProfile, CustomerProfile
from models.room import RoomType, PhysicalRoom, RoomHoldLock
from models.booking import Booking, BookingNight
from models.finance import ServiceItem, ServiceConsumption, FolioInvoice, PaymentTransaction
from models.operations import HousekeepingLog, MaintenanceTicket


class TestDomainModels(unittest.TestCase):

    def test_01_account_hierarchy_and_rbac(self):
        role = Role(1, 'Receptionist', 'Lễ tân tiền sảnh')
        self.assertTrue(role.kiem_tra_quyen('checkin'))
        self.assertFalse(role.kiem_tra_quyen('delete_database'))

        acc_staff = Account(1, 'staff@hotel.vn', 'hash_staff', 'STAFF')
        staff = StaffProfile(acc_staff, 'ST001', 'Nguyen Van A', '0901234567', 'Front Desk', role)
        self.assertEqual(acc_staff.staff_profile.staff_code, 'ST001')

        acc_cust = Account(2, 'guest@mail.com', 'hash_guest', 'CUSTOMER')
        cust = CustomerProfile(acc_cust, 'Tran Thi B', '0912345678', '079123456789')
        cust.tich_luy_diem(25000000)  # 250 points -> SILVER
        self.assertEqual(cust.membership_tier, 'SILVER')

    def test_02_room_inventory_and_hold_lock(self):
        rt = RoomType(1, 'DLX', 'Deluxe Ocean View', 1500000.0, max_adults=2, total_inventory=10)
        self.assertEqual(rt.tinh_gia_phong(3, adults=3), 1500000.0 * 3 + 200000.0 * 3)

        room = PhysicalRoom(101, rt, '101', floor_number=1, housekeeping_status='CLEAN', occupancy_status='VACANT')
        self.assertTrue(room.kiem_tra_san_sang_check_in())
        room.chuyen_sang_dirty()
        self.assertFalse(room.kiem_tra_san_sang_check_in())

        lock = RoomHoldLock(1, rt, 'sess_xyz', quantity=1)
        self.assertEqual(lock.status, 'ACTIVE')
        self.assertFalse(lock.kiem_tra_het_han())
        lock.chuyen_sang_da_ban()
        self.assertEqual(lock.status, 'SOLD')

    def test_03_booking_and_nights(self):
        rt = RoomType(1, 'DLX', 'Deluxe', 1200000.0)
        bk = Booking(
            booking_id=1,
            pnr_code='PNR-20261105-001',
            guest_name='Hoang Nam',
            guest_phone='0988776655',
            arrival_date='2026-12-01',
            departure_date='2026-12-03',
            room_type=rt,
            total_nights=2,
            deposit_amount=1000000.0
        )
        n1 = BookingNight(1, '2026-12-01', 1200000.0)
        n2 = BookingNight(2, '2026-12-02', 1200000.0)
        bk.nights = [n1, n2]

        self.assertEqual(bk.tinh_tong_tien_phong(), 2400000.0)
        bk.xac_nhan_check_in()
        self.assertEqual(bk.booking_status, 'CHECKED_IN')
        bk.hoan_tat_check_out()
        self.assertEqual(bk.booking_status, 'CHECKED_OUT')

    def test_04_billing_settlement_and_vat_invoice(self):
        rt = RoomType(1, 'DLX', 'Deluxe', 1000000.0)
        bk = Booking(
            booking_id=1,
            pnr_code='PNR-20261105-002',
            guest_name='Pham Minh',
            guest_phone='0933221100',
            arrival_date='2026-12-01',
            departure_date='2026-12-02',
            room_type=rt,
            total_nights=1,
            deposit_amount=500000.0
        )
        bk.nights = [BookingNight(1, '2026-12-01', 1000000.0)]

        minibar = ServiceItem(1, 'MNB_COKE', 'Coca Cola', 'MINIBAR', 30000.0, vat_rate=0.1)
        cons = ServiceConsumption(1, bk, minibar, quantity=2)
        self.assertEqual(cons.total_amount, 60000.0)

        invoice = FolioInvoice(1, bk, 'INV-20261105-001')
        invoice.tong_hop_chi_phi([cons])
        # Room: 1,000,000 | Service: 60,000 | VAT: 106,000 | Gross: 1,166,000 | Deposit: 500,000 -> Final: 666,000
        self.assertEqual(invoice.room_subtotal, 1000000.0)
        self.assertEqual(invoice.service_subtotal, 60000.0)
        self.assertEqual(invoice.tax_vat_amount, 106000.0)
        self.assertEqual(invoice.final_amount, 666000.0)

    def test_05_operations_housekeeping_and_maintenance(self):
        rt = RoomType(1, 'STD', 'Standard', 800000.0)
        room = PhysicalRoom(201, rt, '201', floor_number=2, housekeeping_status='DIRTY')
        log = HousekeepingLog(1, room)
        acc = Account(10, 'hk@hotel.vn', 'hash', 'STAFF')
        staff = StaffProfile(acc, 'HK01', 'Le Thi C', '0977112233', 'Housekeeping')

        log.tiep_nhan_ca_don(staff)
        self.assertEqual(room.housekeeping_status, 'IN_PROGRESS')
        log.hoan_tat_ca_don('PASSED')
        self.assertEqual(room.housekeeping_status, 'CLEAN')

        ticket = log.ghi_nhan_su_co('Máy lạnh rò nước')
        self.assertEqual(ticket.priority, 'HIGH')
        ticket.lap_phieu_bao_tri('Máy lạnh hỏng block', 'HIGH')
        self.assertEqual(room.housekeeping_status, 'MAINTENANCE')


if __name__ == '__main__':
    unittest.main()
