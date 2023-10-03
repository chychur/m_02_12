from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, validator


class PhoneNumberValidator:
    @classmethod
    def validate_phone_number(cls, phone: str) -> str:
        cleaned_phone_number = ''.join(filter(str.isdigit, phone))
        if len(cleaned_phone_number) <= 13:
            return cleaned_phone_number
        else:
            raise ValueError("Phone number must contain less than or exactly 13 digits")


# validation  input data contacts
class ContactModel(BaseModel):
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    birthday: date
    email: EmailStr = Field(max_length=150)
    phone: str = Field(max_length=150)
    address: str = Field(max_length=150)

    @validator("phone")
    def validate_phone_number_length(cls, phone):
        return PhoneNumberValidator.validate_phone_number(phone)


# validation  output data contacts
class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
