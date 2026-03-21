"""
Bài toán: Kiểm tra điều kiện tuyển Nghĩa vụ Quân sự (NVQS) - em đã rút gọn để đơn giản hơn

Đầu vào (4 biến):
    age          (int)   : tuổi ứng viên
    bmi          (float) : chỉ số BMI = cân nặng / (chiều cao m)²
    vision       (float) : độ cận (≤ 0)
    health_class (int)   : phân loại sức khỏe theo Bộ Y tế (1–6)

Miền xác định (domain):
    18  <= age          <= 25
    10.0 <= bmi         <= 40.0
    -20.0 <= vision     <= 0.0
    health_class        thuộc {1, 2, 3, 4, 5, 6}

Điều kiện ĐẠT (tất cả phải đúng):
    C1: 18 <= age <= 25
    C2: 18.0 <= bmi <= 30.0
    C3: |vision| < 1.5  
    C4: health_class thuộc {1, 2, 3}

Đầu ra:
    "DAT"        thỏa tất cả 4 điều kiện
    "KHONG_DAT"  ít nhất một điều kiện không thỏa
    ValueError   đầu vào ngoài miền xác định
"""

# Miền xác định
AGE_MIN, AGE_MAX             = 18, 25
BMI_DOMAIN_MIN               = 10.0         
BMI_DOMAIN_MAX               = 40.0
VISION_MIN, VISION_MAX       = -20.0, 0.0
HEALTH_CLASS_VALID           = {1, 2, 3, 4, 5, 6}

# Điều kiện đạt 
BMI_PASS_MIN, BMI_PASS_MAX   = 18.0, 30.0
VISION_LIMIT                 = 1.5
HEALTH_CLASS_PASS            = {1, 2, 3}


def validate_inputs(age, bmi, vision, health_class):
    errors = []
    if not (AGE_MIN <= age <= AGE_MAX):
        errors.append(f"age={age} nằm ngoài [{AGE_MIN}, {AGE_MAX}]")
    if not (BMI_DOMAIN_MIN <= bmi <= BMI_DOMAIN_MAX):
        errors.append(f"bmi={bmi} nằm ngoài [{BMI_DOMAIN_MIN}, {BMI_DOMAIN_MAX}]")
    if not (VISION_MIN <= vision <= VISION_MAX):
        errors.append(f"vision={vision} nằm ngoài [{VISION_MIN}, {VISION_MAX}]")
    if health_class not in HEALTH_CLASS_VALID:
        errors.append(f"health_class={health_class} không thuộc {HEALTH_CLASS_VALID}")
    if errors:
        raise ValueError("Đầu vào không hợp lệ: " + "; ".join(errors))


def check_eligibility(age, bmi, vision, health_class) -> str:

    validate_inputs(age, bmi, vision, health_class)

    c1 = AGE_MIN <= age <= AGE_MAX                 
    c2 = BMI_PASS_MIN <= round(bmi, 4) <= BMI_PASS_MAX
    c3 = abs(vision) < VISION_LIMIT
    c4 = health_class in HEALTH_CLASS_PASS

    return "DAT" if (c1 and c2 and c3 and c4) else "KHONG_DAT"