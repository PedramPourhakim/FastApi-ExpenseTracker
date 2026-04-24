from pydantic import BaseModel, Field, field_validator


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username of the user")
    password: str = Field(..., description="password of the user")


class UserRegisterSchema(UserLoginSchema):
    password_confirm: str = Field(..., description="confirm password of the user")
    person_id: str = Field(
        ..., description="Id of the person related to the user account"
    )

    @classmethod
    @field_validator("password_confirm")
    def check_passwords_match(cls, password_confirm, validation):
        print(password_confirm, validation.data.get("password"))
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("passwords  does not match")


class UserRefreshTokenSchema(BaseModel):
    refresh_token: str = Field(..., description="refresh token of the user")
