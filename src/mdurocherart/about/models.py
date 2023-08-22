from flask_mailman import EmailMessage
from flask import current_app
from mdurocherart.models import Email


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
    msg = EmailMessage(
        subject=user_message.subject,
        body=user_message.body,
        reply_to=[user_message.email],
        from_email=user_message.email,
        to=[current_app.config.get('MAIL_USERNAME')],
        headers={'Message-ID': 'Automated'}
    )

    success = msg.send()
    return bool(success)


def format_email() -> Email:
    pass
    return
