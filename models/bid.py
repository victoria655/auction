from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timedelta
from models.db import Base

def default_expiration():
    return datetime.utcnow() + timedelta(hours=24)

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    
    status = Column(String(20), default="Ongoing")  # e.g., Ongoing, Won, Lost
    
    expires_at = Column(DateTime, nullable=False, default=default_expiration)
    
    highest_bid_amount = Column(Float, nullable=True)

    user = relationship("User", backref="bids")
    item = relationship("Item", backref="bids")

    def __repr__(self):
        return (f"<Bid(amount={self.amount}, user_id={self.user_id}, "
                f"status={self.status}, expires_at={self.expires_at})>")

    @classmethod
    def create(cls, session: Session, amount: float, user_id: int, item_id: int, 
               duration_hours: int = 24):
        """
        Create a new bid with an expiration time and add it to the session.
        """
        expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
        bid = cls(
            amount=amount,
            user_id=user_id,
            item_id=item_id,
            expires_at=expires_at,
            status="ongoing"  
        )
        session.add(bid)
        session.commit()
        return bid

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session: Session, bid_id: int):
        return session.query(cls).filter_by(id=bid_id).first()

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

    def update_status(self, session: Session):
        """
        Check if the bid expired, update status accordingly:
        - If expired and highest bidder => Won
        - If expired and not highest bidder => Lost and record highest winning bid
        """
        now = datetime.utcnow()
        if now >= self.expires_at:
            highest_bid = session.query(Bid)\
                                 .filter_by(item_id=self.item_id)\
                                 .order_by(Bid.amount.desc())\
                                 .first()
            if highest_bid and highest_bid.id == self.id:
                self.status = "Won"
                self.highest_bid_amount = self.amount
            else:
                self.status = "Lost"
                self.highest_bid_amount = highest_bid.amount if highest_bid else None
            session.commit()
