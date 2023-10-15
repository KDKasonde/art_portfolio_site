from flask_mailman import EmailMessage, message
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


def send_email_with_attachments(user_message: QuotationEmail) -> bool:
    """
    This function takes an QuotationEmail object then returns a bool to signify
    whether the email has been successfully sent to the destination.
    Parameters
    ----------
    user_message: QuotationEmail
        This object contains, the sender email, subject, message
        and any attachments
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
            body=user_message.get_message(),
            reply_to=[user_message.email],
            from_email=user_message.email,
            to=[current_app.config.get('MAIL_USERNAME')],
            headers={'Message-ID': 'Automated'},
            connection=conn
        )
        msg.attach(user_message.get_mimeimage())

        success = msg.send()
    return bool(success)


def format_email(payload: Dict[str, str], image: Optional[FileStorage] = None) -> Email:

    if payload['input-subject'] == 'quote':
        email_obj = format_quote(payload, image)
    else:
        subject = payload['input-name'] + ' sent a message about ' + payload['input-subject']
        email_obj = Email(
            name=payload['input-name'],
            email=payload['input-email'],
            subject=subject,
            body=payload['input-message'],
        )

    return email_obj


def format_quote(payload: Dict[str, str], image: FileStorage):
    subject = "Quote request from " + payload['input-name']
    email_object = QuotationEmail(
        name=payload['input-name'],
        email=payload['input-email'],
        subject=subject,
        body=payload['input-message'],
        art_style=payload['input-style'],
        background=payload['input-background'],
        image=image
    )
    return email_object
