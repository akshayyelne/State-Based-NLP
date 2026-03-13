from datetime import datetime
import re


# ==============================
# DATE OF BIRTH VALIDATION
# ==============================
def validate_dob(dob_str):
    """
    Validates DOB format and ensures user is at least 18 years old.
    Expected format: DD/MM/YYYY
    """
    try:
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
        today = datetime.now()

        # DOB cannot be in the future
        if dob > today:
            return False

        age = (today - dob).days // 365
        return age >= 18
    except ValueError:
        return False


def calculate_age(dob_str):
    """
    Returns calculated age from DOB string.
    Used by underwriting engine.
    """
    dob = datetime.strptime(dob_str, "%d/%m/%Y")
    today = datetime.now()
    return (today - dob).days // 365


# ==============================
# VEHICLE YEAR VALIDATION
# ==============================
def validate_vehicle_year(year_str):
    """
    Ensures vehicle year is numeric and within acceptable range.
    """
    try:
        year = int(year_str)
        current_year = datetime.now().year
        return 1980 <= year <= current_year
    except ValueError:
        return False


# ==============================
# CUSTOMER NAME VALIDATION
# ==============================
def validate_name(name_str):
    """
    Ensures name contains only letters and spaces and is at least 3 characters.
    """
    if not name_str or len(name_str.strip()) < 3:
        return False

    return bool(re.match(r"^[A-Za-z\s]+$", name_str.strip()))


# ==============================
# COVERAGE VALIDATION
# ==============================
def validate_coverage(coverage_str):
    """
    Validates allowed coverage types.
    """
    return coverage_str.lower() in ["basic", "premium"]


# ==============================
# POLICY NUMBER VALIDATION
# ==============================
def validate_policy_number(policy_str):
    """
    Valid format: P followed by 5 digits (e.g., P12345)
    """
    return bool(re.match(r"^P\d{5}$", policy_str))


# ==============================
# CLAIM ID VALIDATION
# ==============================
def validate_claim_id(claim_str):
    """
    Valid format: CLM followed by 4–6 digits (e.g., CLM1234)
    """
    return bool(re.match(r"^CLM\d{4,6}$", claim_str))


# ==============================
# GENERIC TEXT VALIDATION
# ==============================
def validate_non_empty(text):
    """
    Ensures text is not empty or whitespace.
    """
    return bool(text and text.strip())
