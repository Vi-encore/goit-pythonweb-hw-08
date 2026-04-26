from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=20)
    birthday: date
    additional_data: Optional[str] = Field(None, max_length=250)


class ContactModel(ContactBase):
    pass


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=5, max_length=20)
    birthday: date | None = None
    additional_data: str | None = None


class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
