import sqlite3

def get_db_connection():
    conn = sqlite3.connect('ccms.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        name TEXT, 
                        phone TEXT, 
                        email TEXT, 
                        registration_date DATE, 
                        user_id TEXT PRIMARY KEY, 
                        password TEXT)''')

    # Create priority users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS priority_users (
                        user_id TEXT PRIMARY KEY, 
                        visits INTEGER)''')
    
    # Modify cabins table: allow multiple allocations by removing primary key constraint on user_id
    cursor.execute('''CREATE TABLE IF NOT EXISTS cabins (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Add auto-incrementing ID
                        user_id TEXT,
                        allocation_date DATE DEFAULT CURRENT_DATE)''')  # Track allocation date

    conn.commit()
    conn.close()
