from pydantic import BaseModel, EmailStr, Field


class Email(BaseModel):
    email: EmailStr = Field(...)
    subject: str = Field(...)
    body: str = Field(...)