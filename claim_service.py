import sqlite3
from datetime import datetime
from config import DB_PATH


def insert_claim(data):

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
                data["claim_id"],
                data["policy_number"],
                data["incident_date"],
                data["incident_type"],
                data["description"],
                "Submitted",
                None,
                None,
                "LOW",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()