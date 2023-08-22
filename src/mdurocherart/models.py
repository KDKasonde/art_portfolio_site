from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Email(BaseModel):
    email: EmailStr = Field(...)
    subject: str = Field(...)
    body: str = Field(...)
    name: Optional[str]
