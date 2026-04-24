from pydantic import field_serializer
from expenses.schemas import *
from typing import List


class BasePersonSchema(BaseModel):
    first_name: str = Field(
        ..., description="The first name of the person", max_length=50
    )
    last_name: str = Field(
        ..., description="The last name of the person", max_length=128
    )

    @staticmethod
    @field_serializer("first_name")
    def serialize_first_name(value):
        return value.title()


class CreatePersonSchema(BasePersonSchema):
    pass


class UpdatePersonSchema(BasePersonSchema):
    pass


class ResponsePersonSchema(BasePersonSchema):
    id: str = Field(..., description="Unique identifier of the person")
    creation_date: datetime = Field(..., description="Date of creation of the person")
    expenses: List[ResponseExpenseSchema]
