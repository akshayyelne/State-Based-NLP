import sqlite3
import random
import logging
from datetime import datetime
from config import DB_PATH


# ======================================
# CLAIM FSM
# ======================================
def handle_claim(state, slots, entities, user_input):

    # ==========================
    # COLLECT POLICY NUMBER
    # ==========================
    if state == "COLLECT_POLICY":

        if "policy_number" not in entities:
            return state, "Please provide a valid policy number."

        policy = entities["policy_number"]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT status FROM Policies WHERE policy_number=?",
                (policy,)
            )
            result = cursor.fetchone()

        if result and result[0] == "Active":
            slots["policy_number"] = policy
            logging.info(f"Policy verified for claim: {policy}")
            return "COLLECT_DATE", "Policy verified. Provide incident date (DD/MM/YYYY)."

        return state, "Invalid or inactive policy."

    # ==========================
    # COLLECT INCIDENT DATE
    # ==========================
    elif state == "COLLECT_DATE":

        if "incident_date" not in entities:
            return state, "Provide date in DD/MM/YYYY."

        slots["incident_date"] = entities["incident_date"]
        return "COLLECT_TYPE", "What type of incident occurred?"

    # ==========================
    # COLLECT INCIDENT TYPE
    # ==========================
    elif state == "COLLECT_TYPE":

        slots["incident_type"] = user_input.strip()
        return "COLLECT_DESC", "Please describe the incident."

    # ==========================
    # COLLECT DESCRIPTION + INSERT
    # ==========================
    elif state == "COLLECT_DESC":

        slots["description"] = user_input.strip()

        # Defensive slot validation
        required_fields = [
            "policy_number",
            "incident_date",
            "incident_type",
            "description"
        ]

        for field in required_fields:
            if not slots.get(field):
                return "END", "Session error. Please restart claim process."

        claim_id = f"CLM{random.randint(1000,9999)}"

        # Risk Classification
        high_risk_types = ["theft", "fraud", "fire"]
        incident_type = slots["incident_type"].lower()

        if incident_type in high_risk_types:
            status = "Investigation"
            risk_flag = "HIGH"
        else:
            status = "Under Review"
            risk_flag = "LOW"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Claims
                (claim_id, policy_number, date, type, description,
                 status, amount, assigned_officer, risk_flag, last_updated)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    claim_id,
                    slots["policy_number"],
                    slots["incident_date"],
                    slots["incident_type"],
                    slots["description"],
                    status,
                    None,               # amount (future use)
                    None,               # assigned officer
                    risk_flag,
                    timestamp
                )
            )
            conn.commit()

        logging.info(
            f"Claim submitted: {claim_id} | "
            f"Status: {status} | Risk: {risk_flag}"
        )

        return (
            "END",
            f"Claim submitted successfully!\n\n"
            f"Claim ID: {claim_id}\n"
            f"Status: {status}\n"
            f"Risk Level: {risk_flag}"
        )

    # ==========================
    # CHECK CLAIM STATUS
    # ==========================
    elif state == "CHECK_STATUS":

        if "claim_id" not in entities:
            return state, "Please provide a valid claim ID (e.g., CLM1234)."

        claim_id = entities["claim_id"]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT status FROM Claims WHERE claim_id=?",
                (claim_id,)
            )
            result = cursor.fetchone()

        if not result:
            return state, "Claim not found. Please check the claim ID and try again."

        status = result[0]
        slots["claim_id"] = claim_id

        return (
            "CLAIM_STATUS_ACTION",
            f"Claim {claim_id} is currently: {status}.\n\n"
            f"Would you like to activate or deactivate this claim? "
            f"(Type 'activate', 'deactivate', or 'no')"
        )

    # ==========================
    # HANDLE CLAIM STATUS ACTION
    # ==========================
    elif state == "CLAIM_STATUS_ACTION":

        choice = user_input.strip().lower()
        claim_id = slots.get("claim_id")

        if choice == "activate":
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE Claims SET status='Active' WHERE claim_id=?", (claim_id,))
                conn.commit()
            return "END", f"Claim {claim_id} has been successfully activated."

        elif choice == "deactivate":
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE Claims SET status='Inactive' WHERE claim_id=?", (claim_id,))
                conn.commit()
            return "END", f"Claim {claim_id} has been successfully deactivated."

        elif choice == "no":
            return "END", "No changes made. Is there anything else I can help you with?"

        else:
            return state, "Please type 'activate', 'deactivate', or 'no'."

    # ==========================
    # FALLBACK
    # ==========================
    return state, "Unexpected state. Please try again."