#/****************
# Mã sinh viên: 202418992
# Họ tên: Phạm Thị Minh Thuý
#/****************

import math


# ----------------------------------------------------------------------
# Các hàm kiểm tra ràng buộc dùng chung cho toàn bộ chương trình
# ----------------------------------------------------------------------
def is_real_number(x) -> bool:
    """True nếu x là số thực hữu hạn (loại bool, NaN, inf)."""
    return (isinstance(x, (int, float)) and not isinstance(x, bool)
            and math.isfinite(x))


def require_non_empty(value, field_name: str) -> str:
    """Bất biến: chuỗi không rỗng (bỏ khoảng trắng hai đầu)."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} không được rỗng")
    return value.strip()


def require_non_negative(value, field_name: str) -> float:
    """Bất biến: số không âm."""
    if not is_real_number(value) or value < 0:
        raise ValueError(f"{field_name} phải là số không âm")
    return float(value)


def require_positive(value, field_name: str) -> float:
    """Ràng buộc: số phải dương (> 0)."""
    if not is_real_number(value) or value <= 0:
        raise ValueError(f"{field_name} phải là số dương")
    return float(value)


class Employee:
    """Nhân sự thông thường: mã, họ tên, lương cơ bản."""

    DEFAULT_ID = "UNKNOWN"
    DEFAULT_NAME = "Unnamed employee"
    DEFAULT_SALARY = 0.0

    # Ba constructor gộp thành một nhờ tham số mặc định:
    #   Employee()
    #   Employee(id, full_name)
    #   Employee(id, full_name, base_salary)
    def __init__(self, id: str = DEFAULT_ID, full_name: str = DEFAULT_NAME,
                 base_salary: float = DEFAULT_SALARY):
        # Kiểm tra hết ràng buộc trước khi gán để đối tượng không bao giờ ở trạng thái sai
        id = require_non_empty(id, "Mã nhân sự")
        full_name = require_non_empty(full_name, "Họ tên")
        base_salary = require_non_negative(base_salary, "Lương cơ bản")

        self._id = id
        self._full_name = full_name
        self._base_salary = base_salary
        print(f"  [+] Tạo Employee: {self._id} - {self._full_name}")

    # ---------------- Getter ----------------
    @property
    def id(self) -> str:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def base_salary(self) -> float:
        return self._base_salary

    # ---------------- "Nạp chồng" increaseSalary ----------------
    def increase_salary(self, value: float, by_percentage: bool = None) -> None:
        """
        increase_salary(amount)                    : tăng một số tiền cố định
        increase_salary(value, by_percentage=True) : tăng theo %
        increase_salary(value, by_percentage=False): tăng số tiền cố định
        """
        require_positive(value, "Giá trị tăng")
        if by_percentage is not None and not isinstance(by_percentage, bool):
            raise TypeError("by_percentage phải là bool")

        if by_percentage:                       # True -> theo phần trăm
            self._base_salary += self._base_salary * value / 100.0
        else:                                   # None hoặc False -> số tiền cố định
            self._base_salary += value

    # ---------------- Hành vi đa hình ----------------
    def calculate_monthly_cost(self) -> float:
        """Chi phí hằng tháng: mặc định bằng lương cơ bản."""
        return self._base_salary

    def display_info(self) -> None:
        print(f"    Employee | ID: {self._id} | Tên: {self._full_name} | "
              f"Lương CB: {self._base_salary:,.0f} | "
              f"Chi phí/tháng: {self.calculate_monthly_cost():,.0f}")

    # ---------------- Destructor: quan sát vòng đời ----------------
    def __del__(self):
        # getattr: phòng trường hợp __init__ ném lỗi trước khi gán thuộc tính
        if getattr(self, "_id", None) is not None:
            print(f"  [-] Hủy Employee: {self._id} - {self._full_name}")