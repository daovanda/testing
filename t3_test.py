import pytest
from t1 import check_eligibility


class TestAllUses:

    def test_TC1_CP_ERR(self):
        """
        TC1 | Complete path: CP-ERR
        L1 → L2(raise ValueError)

        Du-pairs phủ:
          age  (L1, L2) c-use
          bmi  (L1, L2) c-use
          vision (L1, L2) c-use
          hc   (L1, L2) c-use

        Input : age=30 (ngoài [18,25]) → validate_inputs raise ValueError
        Expected: ValueError
        """
        with pytest.raises(ValueError):
            check_eligibility(30, 22.0, -0.5, 2)

    def test_TC2_CP_DAT(self):
        """
        TC2 | Complete path: CP-DAT
        L1 → L2(ok) → L3 → L4 → L5 → L6 → L7(T → "DAT")

        Du-pairs phủ:
          age    (L1, L3) c-use  → age dùng tính c1
          bmi    (L1, L4) c-use  → bmi dùng tính c2
          vision (L1, L5) c-use  → vision dùng tính c3
          hc     (L1, L6) c-use  → hc dùng tính c4
          c1     (L3, L7-T) p-use → c1=True tham gia biểu thức True
          c2     (L4, L7-T) p-use → c2=True
          c3     (L5, L7-T) p-use → c3=True
          c4     (L6, L7-T) p-use → c4=True

        Input : age=21, bmi=22.0, vision=-0.5, health_class=2
                c1=True, c2=True, c3=True, c4=True → DAT
        Expected: "DAT"
        """
        assert check_eligibility(21, 22.0, -0.5, 2) == "DAT"

    def test_TC3_CP_F_C2(self):
        """
        TC3 | Complete path: CP-F-C2
        L1 → L2(ok) → L3 → L4 → L5 → L6 → L7(F → "KHONG_DAT")
        với c2 = False

        Du-pairs phủ:
          c1  (L3, L7-F) p-use → c1=True nhưng biểu thức tổng = False
          c2  (L4, L7-F) p-use → c2=False kéo toàn biểu thức thành False

        Input : age=21, bmi=15.0 (< 18.0 → c2=False), vision=-0.5, hc=2
        Expected: "KHONG_DAT"
        """
        assert check_eligibility(21, 15.0, -0.5, 2) == "KHONG_DAT"

    def test_TC4_CP_F_C3(self):
        """
        TC4 | Complete path: CP-F-C3
        L1 → L2(ok) → L3 → L4 → L5 → L6 → L7(F → "KHONG_DAT")
        với c3 = False

        Du-pairs phủ:
          c3  (L5, L7-F) p-use → c3=False kéo toàn biểu thức thành False

        Input : age=21, bmi=22.0, vision=-2.0 (|vision|=2.0 ≥ 1.5 → c3=False), hc=2
        Expected: "KHONG_DAT"
        """
        assert check_eligibility(21, 22.0, -2.0, 2) == "KHONG_DAT"

    def test_TC5_CP_F_C4(self):
        """
        TC5 | Complete path: CP-F-C4
        L1 → L2(ok) → L3 → L4 → L5 → L6 → L7(F → "KHONG_DAT")
        với c4 = False

        Du-pairs phủ:
          c4  (L6, L7-F) p-use → c4=False kéo toàn biểu thức thành False

        Input : age=21, bmi=22.0, vision=-0.5, hc=5 (∉ {1,2,3} → c4=False)
        Expected: "KHONG_DAT"
        """
        assert check_eligibility(21, 22.0, -0.5, 5) == "KHONG_DAT"
