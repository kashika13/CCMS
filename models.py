from db import get_db_connection
from datetime import date
import random

def register_user(name, phone, email, password):
    conn = get_db_connection()
    user_id = name[:3].lower() + str(random.randint(10, 100))
    today = date.today()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (name, phone, email, registration_date, user_id, password)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (name, phone, email, today, user_id, password))
    conn.commit()
    conn.close()
    return user_id  # Return the generated user ID

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def allocate_cabin(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return "This user doesn't exist."

    # Check if all cabins are full (assuming 7 cabins are available per day)
    cursor.execute("SELECT COUNT(*) FROM cabins WHERE allocation_date = CURRENT_DATE")
    count = cursor.fetchone()[0]

    if count >= 7:
        conn.close()
        return "All cabins are occupied for today."

    # Insert a new record in the cabins table for cabin allocation
    cursor.execute("INSERT INTO cabins (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

    return "Cabin allocated successfully."


def generate_bill(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute("SELECT name, email FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        return None, "This user doesn't exist."

    # Generate random usage hours and calculate bill
    usage_hours = random.randint(1, 7)
    bill_amount = usage_hours * 100

    # Create a dictionary for user info
    user_info = {
        "name": user[0],  # Assuming name is at index 0
        "email": user[1],  # Assuming email is at index 1
        "hours_used": usage_hours
    }

    return user_info, bill_amount

def get_priority_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get users who have been allocated cabins the most
    cursor.execute('''SELECT u.name, u.user_id, COUNT(c.user_id) as visit_count
                      FROM users u
                      LEFT JOIN cabins c ON u.user_id = c.user_id
                      GROUP BY u.user_id
                      ORDER BY visit_count DESC''')
    priority_users = cursor.fetchall()
    conn.close()

    # Format the result as a list of dictionaries for easier access
    return [{"name": user[0], "user_id": user[1], "visit_count": user[2]} for user in priority_users]
