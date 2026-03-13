import sqlite3
from config import DB_PATH
from services.policy_service import update_policy_status


def handle_policy_status(state, slots, entities, user_input):

    # ==========================
    # ASK FOR POLICY NUMBER
    # ==========================
    if state == "CHECK_POLICY_STATUS":

        if "policy_number" not in entities:
            return state, "Please provide a valid policy number (e.g., P12345)."

        policy = entities["policy_number"]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT customer_name, status FROM Policies WHERE policy_number=?",
                (policy,)
            )
            result = cursor.fetchone()

        if not result:
            return state, "Policy not found. Please provide a valid policy number."

        customer_name, status = result
        slots["policy_number"] = policy

        return (
            "POLICY_STATUS_ACTION",
            f"Policy {policy} for {customer_name} is currently: {status}.\n\n"
            f"Would you like to activate or deactivate this policy? "
            f"(Type 'activate', 'deactivate', or 'no')"
        )

    # ==========================
    # HANDLE ACTION CHOICE
    # ==========================
    elif state == "POLICY_STATUS_ACTION":

        choice = user_input.strip().lower()
        policy = slots.get("policy_number")

        if choice == "activate":
            update_policy_status(policy, "Active")
            return "END", f"Policy {policy} has been successfully activated."

        elif choice == "deactivate":
            update_policy_status(policy, "Inactive")
            return "END", f"Policy {policy} has been successfully deactivated."

        elif choice == "no":
            return "END", "No changes made. Is there anything else I can help you with?"

        else:
            return state, "Please type 'activate', 'deactivate', or 'no'."

    return state, "Unexpected state. Please try again."
