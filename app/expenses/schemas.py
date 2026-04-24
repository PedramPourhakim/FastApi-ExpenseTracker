from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BaseExpenseSchema(BaseModel):
    # user_id: str = Field(...,description="The Expense Belongs to who?, give me the Id of the user")
    description: Optional[str] = Field(
        description="The description of the expense",
        examples=["Buy book", "Buy peanuts"],
    )
    amount: float = Field(
        ..., description="The amount of the expense", gt=0, examples=[1000]
    )


class CreateExpenseSchema(BaseExpenseSchema):
    pass


class UpdateExpenseSchema(BaseExpenseSchema):
    pass


class ResponseExpenseSchema(BaseExpenseSchema):
    id: str = Field(..., description="Unique identifier of the person")
    expense_date: datetime = Field(
        ..., description="Date of the last update of the expense"
    )
