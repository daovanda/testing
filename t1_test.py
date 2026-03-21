"""
KIỂM THỬ HỘP ĐEN: BÀI TOÁN TUYỂN NGHĨA VỤ QUÂN SỰ
4 biến đầu vào: age, bmi, vision, health_class

Kỹ thuật A: Kiểm thử giá trị biên
Kỹ thuật B: Kiểm thử bảng quyết định
"""

import pytest
from t1 import check_eligibility

NOM_AGE    = 21
NOM_BMI    = 22.0    # BMI bình thường, 18–30 → ĐẠT
NOM_VISION = -0.5    # cận nhẹ, |v| < 1.5 → ĐẠT
NOM_HC     = 2       # sức khỏe loại 1, 2, 3 → ĐẠT


# A. KIỂM THỬ GIÁ TRỊ BIÊN 

class TestBVA_Age:

    def test_age_min(self):
        """age=18 (min) → ĐẠT"""
        assert check_eligibility(18, NOM_BMI, NOM_VISION, NOM_HC) == "DAT"

    def test_age_min_plus(self):
        """age=19 (min+) → ĐẠT"""
        assert check_eligibility(19, NOM_BMI, NOM_VISION, NOM_HC) == "DAT"

    def test_age_nom(self):
        """age=21 (nom) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, NOM_HC) == "DAT"

    def test_age_max_minus(self):
        """age=24 (max-) → ĐẠT"""
        assert check_eligibility(24, NOM_BMI, NOM_VISION, NOM_HC) == "DAT"

    def test_age_max(self):
        """age=25 (max) → ĐẠT"""
        assert check_eligibility(25, NOM_BMI, NOM_VISION, NOM_HC) == "DAT"

    # BVA mạnh – ngoài miền xác định
    def test_age_min_minus(self):
        """age=17 (min-) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(17, NOM_BMI, NOM_VISION, NOM_HC)

    def test_age_max_plus(self):
        """age=26 (max+) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(26, NOM_BMI, NOM_VISION, NOM_HC)


class TestBVA_BMI:

    def test_bmi_min(self):
        """bmi=18.0 (min điều kiện đạt) → ĐẠT"""
        assert check_eligibility(NOM_AGE, 18.0, NOM_VISION, NOM_HC) == "DAT"

    def test_bmi_min_plus(self):
        """bmi=18.5 (min+) → ĐẠT"""
        assert check_eligibility(NOM_AGE, 18.5, NOM_VISION, NOM_HC) == "DAT"

    def test_bmi_nom(self):
        """bmi=22.0 (nom) → ĐẠT"""
        assert check_eligibility(NOM_AGE, 22.0, NOM_VISION, NOM_HC) == "DAT"

    def test_bmi_max_minus(self):
        """bmi=29.5 (max-) → ĐẠT"""
        assert check_eligibility(NOM_AGE, 29.5, NOM_VISION, NOM_HC) == "DAT"

    def test_bmi_max(self):
        """bmi=30.0 (max điều kiện đạt) → ĐẠT"""
        assert check_eligibility(NOM_AGE, 30.0, NOM_VISION, NOM_HC) == "DAT"

    # Trong miền nhưng không thỏa điều kiện đạt
    def test_bmi_below_pass(self):
        """bmi=17.0 (gầy, trong miền nhưng < 18.0) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, 17.0, NOM_VISION, NOM_HC) == "KHONG_DAT"

    def test_bmi_above_pass(self):
        """bmi=31.0 (béo phì, trong miền nhưng > 30.0) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, 31.0, NOM_VISION, NOM_HC) == "KHONG_DAT"

    # BVA mạnh – ngoài miền xác định
    def test_bmi_out_low(self):
        """bmi=9.9 (ngoài miền xác định) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(NOM_AGE, 9.9, NOM_VISION, NOM_HC)

    def test_bmi_out_high(self):
        """bmi=40.1 (ngoài miền xác định) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(NOM_AGE, 40.1, NOM_VISION, NOM_HC)


class TestBVA_Vision:

    def test_vision_zero(self):
        """vision=0.0 (không cận, max) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, 0.0, NOM_HC) == "DAT"

    def test_vision_max_minus(self):
        """vision=-1.49 (max-, cận biên đạt) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, -1.49, NOM_HC) == "DAT"

    def test_vision_nom(self):
        """vision=-0.75 (nom) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, -0.75, NOM_HC) == "DAT"

    def test_vision_at_threshold(self):
        """vision=-1.5 (|v|=1.5, không thỏa điều kiện <) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, -1.5, NOM_HC) == "KHONG_DAT"

    def test_vision_beyond_threshold(self):
        """vision=-2.0 (cận nặng) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, -2.0, NOM_HC) == "KHONG_DAT"

    def test_vision_min(self):
        """vision=-20.0 (min, cận rất nặng, trong miền) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, -20.0, NOM_HC) == "KHONG_DAT"

    # BVA mạnh – ngoài miền
    def test_vision_positive(self):
        """vision=+0.5 (dương, ngoài miền) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(NOM_AGE, NOM_BMI, 0.5, NOM_HC)


class TestBVA_HealthClass:

    def test_hc_1(self):
        """health_class=1 (min) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 1) == "DAT"

    def test_hc_2(self):
        """health_class=2 (nom đạt) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 2) == "DAT"

    def test_hc_3_boundary_pass(self):
        """health_class=3 (biên trên nhóm ĐẠT) → ĐẠT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 3) == "DAT"

    def test_hc_4_boundary_fail(self):
        """health_class=4 (biên dưới nhóm KHÔNG ĐẠT) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 4) == "KHONG_DAT"

    def test_hc_5(self):
        """health_class=5 → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 5) == "KHONG_DAT"

    def test_hc_6(self):
        """health_class=6 (max, kém nhất) → KHONG_DAT"""
        assert check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 6) == "KHONG_DAT"

    # BVA mạnh – ngoài miền
    def test_hc_zero(self):
        """health_class=0 (ngoài miền) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 0)

    def test_hc_seven(self):
        """health_class=7 (ngoài miền) → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(NOM_AGE, NOM_BMI, NOM_VISION, 7)


# B. KIỂM THỬ BẢNG QUYẾT ĐỊNH (Decision Table Testing)

class TestDecisionTable:

    # R1: Tất cả đúng → ĐẠT
    def test_R1_all_conditions_true(self):
        """R1: C1=T C2=T C3=T C4=T → DAT"""
        assert check_eligibility(20, 22.0, -0.5, 2) == "DAT"

    # R2: C4 sai (health_class xấu)
    def test_R2_bad_health(self):
        """R2: C1=T C2=T C3=T C4=F → KHONG_DAT"""
        assert check_eligibility(20, 22.0, -0.5, 5) == "KHONG_DAT"

    # R3: C3 sai (cận nặng)
    def test_R3_bad_vision(self):
        """R3: C1=T C2=T C3=F C4=T → KHONG_DAT"""
        assert check_eligibility(20, 22.0, -2.0, 2) == "KHONG_DAT"

    # R4: C3 và C4 đều sai
    def test_R4_bad_vision_and_health(self):
        """R4: C1=T C2=T C3=F C4=F → KHONG_DAT"""
        assert check_eligibility(20, 22.0, -2.0, 6) == "KHONG_DAT"

    # R5: C2 sai (gầy), C3 và C4 đúng
    def test_R5_bmi_low_others_ok(self):
        """R5: C1=T C2=F(gầy) C3=T C4=T → KHONG_DAT"""
        assert check_eligibility(20, 15.0, -0.5, 2) == "KHONG_DAT"

    # R6: C2 sai (gầy), C4 sai
    def test_R6_bmi_low_bad_health(self):
        """R6: C1=T C2=F C3=T C4=F → KHONG_DAT"""
        assert check_eligibility(20, 15.0, -0.5, 4) == "KHONG_DAT"

    # R7: C2 sai (béo), C3 sai
    def test_R7_bmi_high_bad_vision(self):
        """R7: C1=T C2=F(béo) C3=F C4=T → KHONG_DAT"""
        assert check_eligibility(20, 35.0, -3.0, 1) == "KHONG_DAT"

    # R8: C2, C3, C4 đều sai
    def test_R8_three_conditions_fail(self):
        """R8: C1=T C2=F C3=F C4=F → KHONG_DAT"""
        assert check_eligibility(20, 35.0, -5.0, 6) == "KHONG_DAT"

    # R9: C1 sai (age ngoài miền) → ValueError
    def test_R9_age_out_of_domain(self):
        """R9: age ngoài miền → ValueError"""
        with pytest.raises(ValueError):
            check_eligibility(30, 22.0, -0.5, 2)

    # R10: C1=T, C2=T, nhưng C3 và C4 sai
    def test_R10_age_bmi_ok_rest_fail(self):
        """R10: C1=T C2=T C3=F C4=F → KHONG_DAT"""
        assert check_eligibility(22, 25.0, -3.0, 5) == "KHONG_DAT"

    # R11: C2 sai bất kể C3, C4
    def test_R11_bmi_always_fail(self):
        """R11: BMI=31 (>30) → KHONG_DAT dù C3, C4 đúng"""
        assert check_eligibility(22, 31.0, -0.5, 2) == "KHONG_DAT"

    # R12: BMI đúng, vision đúng, health sai
    def test_R12_only_health_fail(self):
        """R12: C1=T C2=T C3=T C4=F(health=4) → KHONG_DAT"""
        assert check_eligibility(21, 20.0, -1.0, 4) == "KHONG_DAT"

    # R13: BMI đúng, vision sai
    def test_R13_only_vision_fail(self):
        """R13: C1=T C2=T C3=F(vision=-1.5) C4=T → KHONG_DAT"""
        assert check_eligibility(21, 20.0, -1.5, 2) == "KHONG_DAT"

    # Ca bổ sung: tất cả ở biên dưới → ĐẠT 
    def test_all_lower_boundaries(self):
        """age=18, bmi=18.0, vision=0.0, hc=1 (biên dưới nhóm đạt) → ĐẠT"""
        assert check_eligibility(18, 18.0, 0.0, 1) == "DAT"

    # Ca bổ sung: tất cả ở biên trên → ĐẠT 
    def test_all_upper_boundaries(self):
        """age=25, bmi=30.0, vision=-1.49, hc=3 (biên trên nhóm đạt) → ĐẠT"""
        assert check_eligibility(25, 30.0, -1.49, 3) == "DAT"