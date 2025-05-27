from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from models.db import Base, session
import bcrypt  # For hashing passwords

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)  # Enough length for hashed password
    
    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        return username

    @validates('password')
    def validate_password(self, key, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        return password

    @classmethod
    def create(cls, username, email, password):
        # Hash the password before storing
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = cls(username=username, email=email, password=hashed_pw)
        session.add(user)
        session.commit()
        return user

    def delete(self):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
