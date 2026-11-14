"""
Operations Domain Models: HousekeepingLog, MaintenanceTicket.
Tuân thủ 100% Trang-13 trong Tong_Hop_Bieu_Do.drawio.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from .room import PhysicalRoom
from .account import StaffProfile


class HousekeepingLog:
    """«Entity» HousekeepingLog - Nhật ký dọn dẹp và kiểm tra buồng phòng"""
    def __init__(
        self,
        log_id: int,
        physical_room: PhysicalRoom,
        task_type: str = 'DAILY_CLEAN',
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        inspection_result: str = 'PASSED',
        staff: Optional[StaffProfile] = None,
        notes: Optional[str] = None
    ):
        self.log_id = log_id
        self.physical_room = physical_room
        self.task_type = task_type.upper()
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.inspection_result = inspection_result.upper()
        self.staff = staff
        self.notes = notes

    def tiep_nhan_ca_don(self, staff: StaffProfile) -> None:
        """Ghi nhận nhân viên buồng tiếp nhận ca dọn, chuyển phòng sang IN_PROGRESS."""
        self.staff = staff
        self.start_time = datetime.now()
        self.physical_room.housekeeping_status = 'IN_PROGRESS'

    def hoan_tat_ca_don(self, result: str = 'PASSED') -> None:
        """Hoàn tất dọn phòng, nếu PASSED thì chuyển phòng sang CLEAN."""
        self.end_time = datetime.now()
        self.inspection_result = result.upper()
        if self.inspection_result == 'PASSED':
            self.physical_room.chuyen_sang_clean()

    def ghi_nhan_su_co(self, note: str) -> 'MaintenanceTicket':
        """Ghi nhận hỏng hóc trong phòng và tự động lập phiếu bảo trì."""
        self.notes = note
        self.inspection_result = 'FAILED'
        ticket = MaintenanceTicket(
            ticket_id=0,
            physical_room=self.physical_room,
            issue_description=f"Phát hiện khi dọn phòng: {note}",
            priority='HIGH',
            status='OPEN'
        )
        return ticket

    def to_dict(self) -> Dict[str, Any]:
        return {
            'log_id': self.log_id,
            'physical_room_id': self.physical_room.physical_room_id if self.physical_room else None,
            'room_number': self.physical_room.room_number if self.physical_room else None,
            'task_type': self.task_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'inspection_result': self.inspection_result,
            'staff_name': self.staff.full_name if self.staff else None,
            'notes': self.notes
        }


class MaintenanceTicket:
    """«Entity» MaintenanceTicket - Phiếu sự cố kỹ thuật và bảo trì trang thiết bị phòng"""
    def __init__(
        self,
        ticket_id: int,
        physical_room: PhysicalRoom,
        issue_description: str,
        priority: str = 'MEDIUM',
        status: str = 'OPEN',
        assigned_staff: Optional[StaffProfile] = None,
        created_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        resolution_report: Optional[str] = None
    ):
        self.ticket_id = ticket_id
        self.physical_room = physical_room
        self.issue_description = issue_description
        self.priority = priority.upper()
        self.status = status.upper()
        self.assigned_staff = assigned_staff
        self.created_at = created_at or datetime.now()
        self.resolved_at = resolved_at
        self.resolution_report = resolution_report

    def lap_phieu_bao_tri(self, desc: str, priority: str = 'MEDIUM') -> None:
        """Lập phiếu báo hỏng thiết bị và chuyển phòng sang MAINTENANCE nếu nghiêm trọng."""
        self.issue_description = desc
        self.priority = priority.upper()
        self.status = 'OPEN'
        if self.priority in ('HIGH', 'URGENT'):
            self.physical_room.housekeeping_status = 'MAINTENANCE'

    def phan_cong_ky_thuat(self, staff: StaffProfile) -> None:
        """Phân công nhân viên bảo trì xử lý sự cố."""
        self.assigned_staff = staff
        self.status = 'IN_PROGRESS'

    def hoan_tat_bao_tri(self, report: str) -> None:
        """Nghiệm thu bảo trì và đưa phòng trở lại quy trình dọn dẹp (DIRTY để kiểm tra lại)."""
        self.resolution_report = report
        self.status = 'RESOLVED'
        self.resolved_at = datetime.now()
        self.physical_room.chuyen_sang_dirty()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ticket_id': self.ticket_id,
            'physical_room_id': self.physical_room.physical_room_id if self.physical_room else None,
            'room_number': self.physical_room.room_number if self.physical_room else None,
            'issue_description': self.issue_description,
            'priority': self.priority,
            'status': self.status,
            'assigned_staff_name': self.assigned_staff.full_name if self.assigned_staff else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution_report': self.resolution_report
        }
