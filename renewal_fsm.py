import sqlite3
import logging
from datetime import datetime, timedelta
from config import DB_PATH


def _parse_date(date_str):
    """Parse date from DD/MM/YYYY or YYYY-MM-DD format. Returns datetime or None."""
    if not date_str:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


# ======================================
# RENEWAL FSM
# ======================================
def handle_renewal(state, slots, entities, user_input):

    # ==========================
    # VERIFY POLICY
    # ==========================
    if state == "RENEW_VERIFY_POLICY":

        if "policy_number" not in entities:
            return state, "Please provide policy number (e.g., P12345)."

        policy_number = entities["policy_number"]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT customer_name, coverage, premium, status, expiry_date "
                "FROM Policies WHERE policy_number=?",
                (policy_number,)
            )
            result = cursor.fetchone()

        if not result:
            return state, "Policy not found. Please check the policy number and try again."

        customer_name, coverage, premium, status, expiry_date_str = result

        # Check policy status
        if status != "Active":
            return "END", (
                f"Policy {policy_number} is currently '{status}' and cannot be renewed. "
                f"Please activate it first."
            )

        # Check expiry date
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        expiry_dt = _parse_date(expiry_date_str)

        if expiry_dt is None:
            return "END", (
                "Could not read the expiry date for this policy. "
                "Please contact support."
            )

        if expiry_dt < today:
            return "END", (
                f"Policy {policy_number} expired on {expiry_date_str}. "
                f"Expired policies cannot be renewed through this channel. "
                f"Please contact support to reinstate your policy."
            )

        # Policy is valid — store details in slots
        slots["policy_number"] = policy_number
        slots["customer_name"] = customer_name
        slots["coverage"] = coverage
        slots["premium"] = premium
        slots["expiry_date"] = expiry_date_str

        days_left = (expiry_dt - today).days

        return (
            "RENEW_CONFIRM",
            f"Policy found for {customer_name}.\n"
            f"Coverage: {coverage}\n"
            f"Premium: ${premium}\n"
            f"Expiry Date: {expiry_date_str} ({days_left} day(s) remaining)\n\n"
            f"Type 'renew' to confirm renewal."
        )

    # ==========================
    # CONFIRM RENEWAL
    # ==========================
    elif state == "RENEW_CONFIRM":

        if user_input.strip().lower() != "renew":
            return state, "Type 'renew' to proceed, or 'cancel' to abort."

        policy_number = slots.get("policy_number")

        if not policy_number:
            return "END", "Session error. Please restart the renewal process."

        today = datetime.today()
        new_expiry = today + timedelta(days=365)
        new_expiry_str = new_expiry.strftime("%d/%m/%Y")
        renewal_date_str = today.strftime("%d/%m/%Y")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Policies SET status='Active', expiry_date=?, renewal_date=? "
                "WHERE policy_number=?",
                (new_expiry_str, renewal_date_str, policy_number)
            )
            conn.commit()

        logging.info(
            f"Policy renewed: {policy_number} | "
            f"New expiry: {new_expiry_str} | Renewed on: {renewal_date_str}"
        )

        return (
            "END",
            f"Policy {policy_number} renewed successfully!\n\n"
            f"New Expiry Date: {new_expiry_str}\n"
            f"Renewal Date: {renewal_date_str}"
        )

    # ==========================
    # FALLBACK
    # ==========================
    return state, "Unexpected state. Please try again."
