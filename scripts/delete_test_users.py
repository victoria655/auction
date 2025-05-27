# scripts/delete_all_users.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db import session
from models.user import User

def delete_all_users():
    users = session.query(User).all()
    
    if not users:
        print("⚠️  No users found in the database.")
        return

    print(f"⚠️ WARNING: You are about to delete ALL {len(users)} users!")
    confirm = input("Type 'DELETE ALL' to confirm: ").strip()
    if confirm != "DELETE ALL":
        print("❌ Deletion canceled.")
        return

    for user in users:
        print(f"🗑️ Deleting: {user.username}")
        session.delete(user)

    session.commit()
    print("✅ All users deleted successfully.")

if __name__ == "__main__":
    delete_all_users()
