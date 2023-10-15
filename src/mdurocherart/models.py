from pydantic import BaseModel, EmailStr, Field
from werkzeug.datastructures.file_storage import FileStorage
from email.mime.image import MIMEImage


class Email(BaseModel):
    email: EmailStr = Field(...)
    subject: str = Field(...)
    body: str = Field(...)
    name: str


class QuotationEmail(Email):
    art_style: str
    background: str
    image: FileStorage

    class Config:
        arbitrary_types_allowed = True

    def get_message(self) -> str:
        message_body = f"""{self.name} has requested a quotation from you!\nThey have specified the following:
Art style: {self.art_style}
Background: {self.background}
        
Check the attachments for any reference photos!
        
message from {self.name}:\n
"""
        return message_body + self.body

    def get_mimeimage(self) -> MIMEImage:
        extension = self.image.filename.split('.')[-1]
        mimeimage = MIMEImage(self.image.read(), _subtype=extension)
        mimeimage.add_header('Content-Disposition', 'attachment; filename=quote_image.{}'.format(extension))
        return mimeimage
