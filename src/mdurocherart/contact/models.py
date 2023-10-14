from flask_mailman import EmailMessage
from flask import current_app
from mdurocherart.models import Email, QuotationEmail
from typing import Dict, Optional
from werkzeug.datastructures.file_storage import FileStorage


def get_mail_server_connection():
    return current_app.config.get('MAIL_CLIENT').get_connection()


def send_email(user_message: Email) -> bool:
    """
    This function takes an Email object then returns a bool to signify
    whether the email has been successfully sent to the destination.
    Parameters
    ----------
    user_message: Email
        This object contains, the sender email, subject and message

    Returns
    -------
    bool
        Signifying the success or failure of the email being sent
        (This is actually the number one emails sent, but we want to send one
        at a time)
    """
    with get_mail_server_connection() as conn:
        msg = EmailMessage(
            subject=user_message.subject,
            body=user_message.body,
            reply_to=[user_message.email],
            from_email=user_message.email,
            to=[current_app.config.get('MAIL_USERNAME')],
            headers={'Message-ID': 'Automated'},
            connection=conn
        )

        success = msg.send()
    return bool(success)


def format_email(request_payload: Dict[str, str], image: Optional[FileStorage] = None) -> Email:

    if request_payload['input-subject'] == 'quote':
        format_quote(request_payload, image)
    else:
        email_obj = Email(
            **request_payload
        )

    return email_obj


def format_quote(payload: Dict[str, str], image: FileStorage):
    email_object = QuotationEmail(
        name=payload['input-name'],
        email=payload['input-email'],
        subject=payload['input-subject'],
        body=payload['input-message'],
        art_style=payload['input-style'],
        background=payload['input-background'],
        image=image
    )
    return email_object
