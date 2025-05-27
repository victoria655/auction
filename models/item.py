from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Session
from models.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    starting_price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", backref="items")

    def __repr__(self):
        return f"<Item(name={self.name}, price={self.starting_price})>"

    @classmethod
    def create(cls, session: Session, name: str, description: str, starting_price: float, owner_id: int):
        item = cls(name=name, description=description, starting_price=starting_price, owner_id=owner_id)
        session.add(item)
        session.commit()
        return item

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session: Session, item_id: int):
        return session.query(cls).filter_by(id=item_id).first()

    def delete(self, session: Session):
        session.delete(self)
        session.commit()
