import sqlite3

def add_password_column(db_path='auction.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if password column already exists
    cursor.execute("PRAGMA table_info(users);")
    columns = [info[1] for info in cursor.fetchall()]
    if 'password' in columns:
        print("Column 'password' already exists in 'users' table.")
    else:
        # Add the password column with a default empty string value
        cursor.execute("ALTER TABLE users ADD COLUMN password VARCHAR(128) NOT NULL DEFAULT '';")
        print("Added 'password' column to 'users' table.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_password_column()
