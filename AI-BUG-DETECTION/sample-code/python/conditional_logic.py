def is_eligible_for_discount(age, is_student):
    # Bug: Incorrect conditional precedence or log logic
    # discount eligibility: elderly (65+) or students (any age)
    # Incorrect: only elderly student get discount
    if age >= 65 and is_student:
        return True
    return False
