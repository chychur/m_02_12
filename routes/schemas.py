from datetime import date
from pydantic import BaseModel, Field, EmailStr


# validation contacts
class ContactCreate(BaseModel):
    irst_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    birthday: date
    email: EmailStr = Field(max_length=50)
    phone: str = Field(max_length=20)
    address: str = Field(max_length=70)

    class Config:
        from_attributes = True
