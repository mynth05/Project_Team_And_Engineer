#/****************
# Mã sinh viên: 202418992
# Họ tên: Phạm Thị Minh Thuý
#/****************
"""
Lớp SoftwareEngineer: kế thừa công khai từ Employee.
"""
from Employee import Employee, require_non_empty, require_non_negative


class SoftwareEngineer(Employee):
    """Kỹ sư phần mềm: thêm ngôn ngữ lập trình chính và phụ cấp kỹ thuật."""

    # Hai constructor gộp thành một bằng *args:
    #   SoftwareEngineer(id, full_name, primary_language)
    #   SoftwareEngineer(id, full_name, base_salary, primary_language, technical_allowance)
    def __init__(self, id: str, full_name: str, *args):
        if len(args) == 1:
            base_salary, primary_language, technical_allowance = 0.0, args[0], 0.0
        elif len(args) == 3:
            base_salary, primary_language, technical_allowance = args
        else:
            raise TypeError(
                "SoftwareEngineer(id, name, language) hoặc "
                "SoftwareEngineer(id, name, base_salary, language, allowance)")

        # Kiểm tra ràng buộc của lớp con trước khi khởi tạo lớp cha
        primary_language = require_non_empty(primary_language, "Ngôn ngữ chính")
        technical_allowance = require_non_negative(technical_allowance, "Phụ cấp kỹ thuật")

        super().__init__(id, full_name, base_salary)
        self._primary_language = primary_language
        self._technical_allowance = technical_allowance

    @property
    def primary_language(self) -> str:
        return self._primary_language

    @property
    def technical_allowance(self) -> float:
        return self._technical_allowance

    # Ghi đè: lương cơ bản + phụ cấp
    def calculate_monthly_cost(self) -> float:
        return self._base_salary + self._technical_allowance

    # Ghi đè hiển thị
    def display_info(self) -> None:
        print(f"    SoftwareEngineer | ID: {self._id} | Tên: {self._full_name} | "
              f"Lương CB: {self._base_salary:,.0f} | Ngôn ngữ: {self._primary_language} | "
              f"Phụ cấp: {self._technical_allowance:,.0f} | "
              f"Chi phí/tháng: {self.calculate_monthly_cost():,.0f}")

    # Destructor: in thông báo rồi gọi destructor lớp cha (Python không tự gọi)
    def __del__(self):
        if getattr(self, "_primary_language", None) is not None:
            print(f"  [-] Hủy SoftwareEngineer: {self._id} ({self._primary_language})")
        super().__del__()