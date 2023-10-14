from pydantic import BaseModel, EmailStr, Field
from werkzeug.datastructures.file_storage import FileStorage


class Email(BaseModel):
    email: EmailStr = Field(...)
    subject: str = Field(...)
    body: str = Field(...)
    name: str


class QuotationEmail(Email):
    art_style: str
    background: str
    image_attachment: FileStorage

    class Config:
        arbitrary_types_allowed = True
