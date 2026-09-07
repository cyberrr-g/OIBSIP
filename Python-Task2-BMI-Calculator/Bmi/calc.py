CATEGORY_COLORS = {
    "Underweight": "#3498db",
    "Normal": "#2ecc71",
    "Overweight": "#f39c12",
    "Obese": "#e74c3c",
}


def calc_bmi(weight, height_cm):
    height_m = height_cm / 100.0
    return weight / (height_m ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
