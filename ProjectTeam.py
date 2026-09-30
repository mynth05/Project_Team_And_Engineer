#/****************
# Mã sinh viên: 202418992
# Họ tên: Phạm Thị Minh Thuý
#/****************
"""
Lớp ProjectTeam: nhóm dự án.

Quan hệ KẾT TẬP (aggregation) với Employee: nhóm chỉ giữ THAM CHIẾU tới các
Employee, không sở hữu chúng. Nhân sự tồn tại độc lập và có thể thuộc nhiều nhóm.
Hủy nhóm chỉ xóa danh sách tham chiếu, không hủy đối tượng Employee.

Bất biến được duy trì:
    1. Mã nhân sự không rỗng                        (Employee)
    2. Lương cơ bản không âm                        (Employee)
    3. Không có hai thành viên cùng mã trong nhóm   (add_member)
    4. Trưởng nhóm luôn thuộc danh sách thành viên  (constructor, add_member, change_leader)
    5. Một nhân sự không xuất hiện hai lần trong nhóm
"""
from typing import List, Optional

from Employee import Employee, require_non_empty


class ProjectTeam:

    # Hai constructor gộp thành một nhờ tham số leader mặc định None:
    #   ProjectTeam(code, name)
    #   ProjectTeam(code, name, leader)
    def __init__(self, project_code: str, project_name: str,
                 leader: Optional[Employee] = None):
        self._project_code = require_non_empty(project_code, "Mã dự án")
        self._project_name = require_non_empty(project_name, "Tên dự án")
        self._leader: Optional[Employee] = None            # liên kết không sở hữu
        self._members: List[Employee] = []                 # danh sách liên kết không sở hữu

        if leader is not None:
            self._check_employee(leader)
            self._members.append(leader)                   # trưởng nhóm tự vào danh sách
            self._leader = leader
        print(f"  [+] Tạo ProjectTeam: {self._project_code} - {self._project_name}")

    # ---------------- Getter ----------------
    @property
    def project_code(self) -> str:
        return self._project_code

    @property
    def project_name(self) -> str:
        return self._project_name

    @property
    def leader(self) -> Optional[Employee]:
        return self._leader

    @property
    def members(self) -> tuple:
        """Trả về bản sao bất biến để bên ngoài không phá được bất biến của nhóm."""
        return tuple(self._members)

    # ---------------- Hàm nội bộ ----------------
    @staticmethod
    def _check_employee(employee) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Tham số phải là đối tượng Employee (hoặc lớp con)")

    def _find(self, employee_id: str) -> Optional[Employee]:
        for m in self._members:
            if m.id == employee_id:
                return m
        return None

    # ---------------- "Nạp chồng" addMember ----------------
    def add_member(self, employee: Employee, make_leader: bool = False) -> bool:
        """
        add_member(employee)                     : thêm thành viên
        add_member(employee, make_leader=True)   : thêm và đặt làm trưởng nhóm
        Trả về False nếu nhân sự đã có trong nhóm (trùng mã) - khi đó không thay đổi gì.
        Trưởng nhóm cũ (nếu có) vẫn là thành viên.
        """
        self._check_employee(employee)
        if not isinstance(make_leader, bool):
            raise TypeError("make_leader phải là bool")

        if self.contains(employee.id):          # không thêm trùng (theo mã)
            return False

        self._members.append(employee)
        if make_leader:
            self._leader = employee
        return True

    def remove_member(self, employee_id: str) -> bool:
        """Xóa thành viên. Từ chối (False) nếu không tìm thấy hoặc đó là trưởng nhóm hiện tại."""
        member = self._find(employee_id)
        if member is None:
            return False
        if member is self._leader:              # phải đổi trưởng nhóm trước
            return False
        self._members.remove(member)
        return True

    def change_leader(self, employee: Employee) -> bool:
        """
        Đổi trưởng nhóm. Nếu chưa là thành viên thì tự thêm vào nhóm.
        Trả về False nếu: đã là trưởng nhóm, hoặc trùng mã với một thành viên khác.
        """
        self._check_employee(employee)
        existing = self._find(employee.id)
        if existing is not None and existing is not employee:
            return False                        # cùng mã nhưng là đối tượng khác
        if employee is self._leader:
            return False
        if existing is None:
            self._members.append(employee)      # giữ bất biến: trưởng nhóm thuộc nhóm
        self._leader = employee
        return True

    def contains(self, employee_id: str) -> bool:
        return self._find(employee_id) is not None

    def calculate_total_monthly_cost(self) -> float:
        # Gọi đa hình: mỗi loại nhân sự tự tính chi phí của mình
        return sum(m.calculate_monthly_cost() for m in self._members)

    def display_team(self) -> None:
        print(f"  ===== Dự án {self._project_code}: {self._project_name} =====")
        if self._leader is None:
            print("  Trưởng nhóm: (chưa có)")
        else:
            print(f"  Trưởng nhóm: {self._leader.full_name} ({self._leader.id})")
        print(f"  Số thành viên: {len(self._members)}")
        for i, m in enumerate(self._members, 1):
            tag = " [TRƯỞNG NHÓM]" if m is self._leader else ""
            print(f"   #{i}{tag}")
            m.display_info()                    # gọi đa hình

    # ---------------- Destructor ----------------
    def __del__(self):
        # Chỉ hủy cấu trúc danh sách nội bộ; KHÔNG hủy các đối tượng Employee
        if getattr(self, "_members", None) is not None:
            print(f"  [-] Hủy ProjectTeam: {self._project_code} "
                  f"(chỉ giải phóng danh sách liên kết, {len(self._members)} nhân sự vẫn còn)")
            self._members.clear()
            self._leader = None