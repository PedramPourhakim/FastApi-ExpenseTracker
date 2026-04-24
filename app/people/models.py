from core.database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class PersonModel(Base):
    __tablename__ = "people"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(128), nullable=True)
    creation_date = Column(DateTime, default=func.now())

    expenses = relationship("ExpenseModel", backref="person")
    users = relationship("UserModel", backref="person")

    def __repr__(self):
        return (
            f"Person(id={self.id}, first_name={self.first_name}, last_name={self.last_name} ,"
            f"creation_date={self.creation_date}, expenses={self.expenses})"
        )
