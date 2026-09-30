#/****************
# Mã sinh viên: 202418992
# Họ tên: Phạm Thị Minh Thuý
#/****************
from Employee import Employee
from SoftwareEngineer import SoftwareEngineer
from ProjectTeam import ProjectTeam


def step(n: int, text: str) -> None:
    print(f"\n--- Bước {n}: {text} ---")


def expect_error(label: str, func) -> None:
    """Chạy func và in ra lỗi mong đợi (dùng cho test trường hợp biên)."""
    try:
        func()
        print(f"  [SAI] {label}: lẽ ra phải báo lỗi")
    except (ValueError, TypeError) as e:
        print(f"  [OK] {label} -> bị từ chối: {e}")


def second_team_demo(e1: Employee, s1: SoftwareEngineer) -> None:
    """Bước 13-14: phạm vi cục bộ của hàm thay cho khối lệnh { } của C++."""
    step(13, "Tạo nhóm thứ hai, thêm nhân sự đã có ở nhóm thứ nhất")
    team2 = ProjectTeam("PRJ02", "Ứng dụng di động", s1)      # s1 làm trưởng nhóm
    print("  team2.add_member(e1) ->", team2.add_member(e1))
    team2.display_team()
    print(f"  e1 thuộc nhóm 2: {team2.contains(e1.id)} (đồng thời vẫn thuộc nhóm 1)")
    step(14, "Kết thúc khối lệnh cục bộ -> nhóm thứ hai bị hủy")
    # Hết hàm: team2 ra khỏi phạm vi và bị hủy ngay (CPython đếm tham chiếu)


def main() -> None:
    step(1, "Tạo hai Employee bằng hai constructor khác nhau")
    e1 = Employee("E001", "Nguyễn Văn An")                    # constructor 2 tham số
    e2 = Employee("E002", "Trần Thị Bình", 12_000_000)        # constructor 3 tham số
    e1.display_info()
    e2.display_info()

    step(2, "Tạo hai SoftwareEngineer bằng hai constructor khác nhau")
    s1 = SoftwareEngineer("S001", "Lê Văn Cường", "Python")                  # 3 tham số
    s2 = SoftwareEngineer("S002", "Phạm Thị Dung", 20_000_000, "C#", 3_000_000)  # 5 tham số
    s1.display_info()
    s2.display_info()

    step(3, "Tăng lương một nhân sự bằng số tiền cố định")
    e1.increase_salary(8_000_000)
    print(f"  Lương e1 sau khi tăng 8.000.000: {e1.base_salary:,.0f}")

    step(4, "Tăng lương một nhân sự khác theo phần trăm")
    e2.increase_salary(10, True)
    print(f"  Lương e2 sau khi tăng 10%: {e2.base_salary:,.0f}")
    s2.increase_salary(1_000_000, False)                      # byPercentage=False -> cố định
    print(f"  Lương s2 sau khi tăng cố định 1.000.000 (by_percentage=False): {s2.base_salary:,.0f}")

    step(5, "Tạo nhóm dự án không có trưởng nhóm")
    team = ProjectTeam("PRJ01", "Hệ thống quản lý nhân sự")
    print("  Trưởng nhóm hiện tại:", team.leader)

    step(6, "Thêm một nhân sự bằng addMember(employee)")
    print("  add_member(e1) ->", team.add_member(e1))
    print("  add_member(e2) ->", team.add_member(e2))

    step(7, "Thêm một kỹ sư bằng addMember(employee, True) làm trưởng nhóm")
    print("  add_member(s2, True) ->", team.add_member(s2, True))
    print("  Trưởng nhóm:", team.leader.full_name)

    step(8, "Thử thêm lại một thành viên đã tồn tại")
    print("  add_member(e1) lần 2 ->", team.add_member(e1))
    trung_ma = Employee("E001", "Người khác trùng mã")
    print("  add_member(nhân sự khác nhưng trùng mã E001) ->", team.add_member(trung_ma))
    print("  Số thành viên vẫn là:", len(team.members))

    step(9, "Hiển thị danh sách bằng lời gọi đa hình")
    team.display_team()

    step(10, "Tính tổng chi phí nhân sự hằng tháng")
    print(f"  Tổng chi phí/tháng: {team.calculate_total_monthly_cost():,.0f}")

    step(11, "Thử xóa trưởng nhóm hiện tại -> phải bị từ chối")
    print("  remove_member('S002') ->", team.remove_member("S002"))
    print("  S002 còn trong nhóm:", team.contains("S002"))

    step(12, "Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm")
    print("  change_leader(s1) ->", team.change_leader(s1), "(s1 chưa ở trong nhóm nên được tự thêm)")
    print("  Trưởng nhóm mới:", team.leader.full_name)
    print("  remove_member('S002') ->", team.remove_member("S002"))
    team.display_team()

    second_team_demo(e1, s1)

    step(15, "Nhân sự của nhóm thứ hai vẫn tồn tại sau khi nhóm bị hủy")
    print("  e1 vẫn tồn tại, thông tin:")
    e1.display_info()
    print("  s1 vẫn tồn tại, thông tin:")
    s1.display_info()
    print("  Nhóm 1 vẫn chứa e1:", team.contains(e1.id), "| chứa s1:", team.contains(s1.id))

    # ------------------------------------------------------------------
    print("\n=========== CÁC TRƯỜNG HỢP BIÊN ===========")
    d = Employee()
    print(f"  Employee() mặc định -> {d.id} / {d.full_name} / {d.base_salary}")
    expect_error("Mã rỗng", lambda: Employee("", "Ten"))
    expect_error("Họ tên toàn khoảng trắng", lambda: Employee("E9", "   "))
    expect_error("Lương âm", lambda: Employee("E9", "Ten", -1))
    expect_error("Tăng lương giá trị 0", lambda: e1.increase_salary(0))
    expect_error("Tăng lương giá trị âm", lambda: e1.increase_salary(-5, True))
    expect_error("Ngôn ngữ chính rỗng", lambda: SoftwareEngineer("S9", "Ten", ""))
    expect_error("Phụ cấp âm", lambda: SoftwareEngineer("S9", "Ten", 1000, "Java", -1))
    expect_error("Sai số lượng tham số SoftwareEngineer", lambda: SoftwareEngineer("S9", "Ten", 1, 2))
    expect_error("Mã dự án rỗng", lambda: ProjectTeam("", "Ten"))
    expect_error("Thêm đối tượng không phải Employee", lambda: team.add_member("abc"))

    print("  remove_member('KHONGCO') ->", team.remove_member("KHONGCO"))
    print("  change_leader(s1) khi s1 đã là trưởng nhóm ->", team.change_leader(s1))
    print("  change_leader(nhân sự trùng mã E001) ->", team.change_leader(trung_ma))

    solo = ProjectTeam("PRJ03", "Nhóm một người", e2)          # constructor có trưởng nhóm
    print("  Nhóm có trưởng nhóm khi khởi tạo, thành viên:", len(solo.members))
    print("  remove_member(trưởng nhóm duy nhất) ->", solo.remove_member("E002"))
    rong = ProjectTeam("PRJ04", "Nhóm rỗng")
    rong.display_team()
    print(f"  Tổng chi phí nhóm rỗng: {rong.calculate_total_monthly_cost():,.0f}")

    print("\n=========== KẾT THÚC CHƯƠNG TRÌNH (các đối tượng bị hủy) ===========")


if __name__ == "__main__":
    main()