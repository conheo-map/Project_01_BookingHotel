"""
Domain Entity Models - Saigon - Condao Booking Platform.
100% synchronized with Trang-13 (Domain Class Diagram) in Tong_Hop_Bieu_Do.drawio.
"""

from .account import Role, Account, StaffProfile, CustomerProfile
from .room import RoomType, PhysicalRoom, RoomHoldLock
from .booking import Booking, BookingNight
from .finance import ServiceItem, ServiceConsumption, FolioInvoice, PaymentTransaction
from .operations import HousekeepingLog, MaintenanceTicket

__all__ = [
    'Role',
    'Account',
    'StaffProfile',
    'CustomerProfile',
    'RoomType',
    'PhysicalRoom',
    'RoomHoldLock',
    'Booking',
    'BookingNight',
    'ServiceItem',
    'ServiceConsumption',
    'FolioInvoice',
    'PaymentTransaction',
    'HousekeepingLog',
    'MaintenanceTicket'
]
