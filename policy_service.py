import sqlite3
import datetime
from config import DB_PATH

def create_policy(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Calculate expiry and renewal dates
    now = datetime.datetime.now()
    expiry_date = (now + datetime.timedelta(days=365)).strftime("%d/%m/%Y")
    renewal_date = (now + datetime.timedelta(days=335)).strftime("%d/%m/%Y") # 30 days before expiry

    cursor.execute(
        "INSERT INTO Policies (policy_number, customer_name, dob, vehicle_make, vehicle_year, coverage, premium, status, expiry_date, renewal_date) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (
            data["policy_number"],
            data["customer_name"],
            data["dob"],
            data["vehicle_make"],
            int(data["vehicle_year"]),
            data["coverage"],
            data["premium"],
            "Active",
            expiry_date,
            renewal_date
        )
    )

    conn.commit()
    conn.close()

def update_policy_status(policy_number, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE Policies SET status = ? WHERE policy_number = ?", (status, policy_number))
    conn.commit()
    conn.close()

def extend_renewal_date(policy_number, days=365):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT expiry_date FROM Policies WHERE policy_number = ?", (policy_number,))
    result = cursor.fetchone()
    if result:
        current_expiry = datetime.datetime.strptime(result[0], "%d/%m/%Y")
        new_expiry = (current_expiry + datetime.timedelta(days=days)).strftime("%d/%m/%Y")
        cursor.execute("UPDATE Policies SET expiry_date = ?, status = 'Active' WHERE policy_number = ?", (new_expiry, policy_number))
        conn.commit()
    conn.close()
