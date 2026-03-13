import random
from services.premium_service import calculate_premium
from services.policy_service import create_policy

def handle_policy(state, slots, user_input):

    if state == "COLLECT_NAME":
        slots["customer_name"] = user_input.strip()
        return "COLLECT_DOB", "What is your date of birth (DD/MM/YYYY)?"

    elif state == "COLLECT_DOB":
        slots["dob"] = user_input.strip()
        return "COLLECT_VEHICLE_MAKE", "What is your vehicle make? (e.g., Toyota, Ford)"
        
    elif state == "COLLECT_VEHICLE_MAKE":
        slots["vehicle_make"] = user_input.strip()
        return "COLLECT_VEHICLE_YEAR", "What is your vehicle manufacturing year? (e.g., 2018)"

    elif state == "COLLECT_VEHICLE_YEAR":
        if not user_input.isdigit():
            return "COLLECT_VEHICLE_YEAR", "Please enter a valid year (e.g., 2018)."
        slots["vehicle_year"] = user_input
        return "SELECT_COVERAGE", "Select coverage type: Basic or Premium."

    elif state == "SELECT_COVERAGE":
        clean_input = user_input.strip().lower()
        if clean_input not in ["basic", "premium"]:
            return "SELECT_COVERAGE", "Invalid input. Please choose strictly 'Basic' or 'Premium'."
        
        slots["coverage"] = clean_input.capitalize()
        premium = calculate_premium(slots["coverage"], slots["vehicle_year"])
        slots["premium"] = premium
        return "CREATE_POLICY", f"Your quoted premium is ${premium}. Type 'confirm' to create the policy."

    elif state == "CREATE_POLICY":
        if user_input.lower() != "confirm":
            return "CREATE_POLICY", "Please type 'confirm' to proceed or 'cancel' to stop."

        policy_number = f"P{random.randint(10000,99999)}"
        slots["policy_number"] = policy_number
        create_policy(slots)

        return "END", f"Policy created successfully! Policy Number: {policy_number}"