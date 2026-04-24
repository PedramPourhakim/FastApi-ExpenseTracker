from core.database import Base
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text
import uuid
from sqlalchemy.sql import func


# Each User Can have many expenses
# So the relationship between them are one to many
class ExpenseModel(Base):
    __tablename__ = "expenses"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    person_id = Column(String, ForeignKey("people.id"))

    description = Column(Text, nullable=True)
    amount = Column(Float, default=0)
    expense_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"Expense(id={self.id}, person_id={self.person_id}, description={self.description},"
            f"amount={self.amount}, expense_date={self.expense_date})"
        )
