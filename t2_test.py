"""
KIỂM THỬ HỘP TRẮNG ĐỘ PHỦ NHÁNH C2
Bài toán: Kiểm tra điều kiện tuyển Nghĩa vụ Quân sự

"""

import pytest
from t1 import check_eligibility

# Giá trị nominal – tất cả 4 điều kiện ĐẠT 
NOM_AGE    = 21       # C1: 18 ≤ 21 ≤ 25       → True
NOM_BMI    = 22.0     # C2: 18.0 ≤ 22.0 ≤ 30.0 → True
NOM_VISION = -0.5     # C3: |-0.5| = 0.5 < 1.5  → True
NOM_HC     = 2        # C4: 2 ∈ {1,2,3}         → True


class TestBranchCoverage:
    """
    6 ca kiểm thử tối thiểu phủ 100% nhánh C2 (6 đường đi độc lập).
    """

    def test_TC1_E_err(self):
        """
        TC1 | Đường đi: E-err
        Mô tả : Đầu vào ngoài miền xác định → validate_inputs raise ValueError
        Input : age=30 (ngoài [18,25])
        Path  : N0 →(E-err)→ ValueError
        Expected: ValueError
        """
        with pytest.raises(ValueError):
            check_eligibility(30, NOM_BMI, NOM_VISION, NOM_HC)

    def test_TC2_C1_False(self):
        """
        TC2 | Đường đi: E-ok → C1-F
        Mô tả : C1 = False (age không thỏa 18 ≤ age ≤ 25)
        Input : age=17, bmi=22.0, vision=-0.5, health_class=2
        Path  : N0 →(E-ok)→ N1 →(C1-F)→ KHONG_DAT
        Expected: KHONG_DAT

        Ghi chú: Để kiểm tra đường đi C1-F trong CFG, cần bỏ qua
        validate_inputs. Ta gọi trực tiếp logic sau validate bằng cách
        dùng mock, hoặc ghi nhận rằng nhánh này bị chặn bởi validate.
        Theo phân tích CFG, nhánh C1-F tồn tại và được ghi nhận.
        """
        # age=17 bị ValueError bởi validate → nhánh C1-F bị chặn trước
        # Gọi trực tiếp phần logic sau validate để phủ nhánh C1-F:
        from unittest.mock import patch
        with patch('t1.validate_inputs', return_value=None):
            result = check_eligibility(17, NOM_BMI, NOM_VISION, NOM_HC)
        assert result == "KHONG_DAT"

    def test_TC3_C2_False(self):
        """
        TC3 | Đường đi: E-ok → C1-T → C2-F
        Mô tả : C1=True, C2=False (bmi ngoài [18.0,30.0])
        Input : age=21, bmi=15.0, vision=-0.5, health_class=2
        Path  : N0 →(E-ok)→ N1 →(C1-T)→ N2 →(C2-F)→ KHONG_DAT
        Expected: KHONG_DAT
        """
        assert check_eligibility(NOM_AGE, 15.0, NOM_VISION, NOM_HC) == "KHONG_DAT"

    def test_TC4_C3_False(self):
        """
        TC4 | Đường đi: E-ok → C1-T → C2-T → C3-F
        Mô tả : C1=True, C2=True, C3=False (|vision| ≥ 1.5)
        Input : age=21, bmi=22.0, vision=-2.0, health_class=2
        Path  : N0 →(E-ok)→ N1 →(C1-T)→ N2 →(C2-T)→ N3 →(C3-F)→ KHONG_DAT
        Expected: KHONG_DAT
        """
        assert check_eligibility(NOM_AGE, NOM_BMI, -2.0, NOM_HC) == "KHONG_DAT"

    def test_TC5_C4_False(self):
        """
        TC5 | Đường đi: E-ok → C1-T → C2-T → C3-T → C4-F
        Mô tả : C1=True, C2=True, C3=True, C4=False (health_class ∉ {1,2,3})
        Input : age=21, bmi=22.0, vision=-0.5, health_class=5
        Path  : N0 →(E-ok)→ N1 →(C1-T)→ N2 →(C2-T)→ N3 →(C3-T)→ N4 →(C4-F)→ KHONG_DAT
        Expected: KHONG_DAT
        """
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 5) == "KHONG_DAT"

    def test_TC6_C4_True(self):
        """
        TC6 | Đường đi: E-ok → C1-T → C2-T → C3-T → C4-T
        Mô tả : Tất cả C1=True, C2=True, C3=True, C4=True → ĐẠT
        Input : age=21, bmi=22.0, vision=-0.5, health_class=2
        Path  : N0 →(E-ok)→ N1 →(C1-T)→ N2 →(C2-T)→ N3 →(C3-T)→ N4 →(C4-T)→ DAT
        Expected: DAT
        """
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, NOM_HC) == "DAT"
