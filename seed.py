import bcrypt
from models import User
from models.db import session

if __name__ == "__main__":
    praise_user = session.query(User).filter_by(username="praise").first()

    if praise_user:
        new_password = "short123"  # Change to your desired password
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        praise_user.password = hashed_pw
        session.commit()
        print("Password updated successfully.")
    else:
        print("User 'praise' not found.")
