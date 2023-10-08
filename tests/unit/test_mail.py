import pytest

from mdurocherart.contact.models import send_email
from mdurocherart.models import Email


emails = [
    Email(
        email='tester@testing.com',
        subject='johnny bravo',
        body='Don\'t you think johnny bravo is buff',
        name='johnny bravo',
    ),
    Email(
        email='devloper@deving.com',
        subject='Courage the cowardly dog',
        body='Don\'t you think courage is courageous',
        name='Courage',
    ),
]

@pytest.mark.conn_required
@pytest.mark.parametrize("email", emails)
def test_send_mail(mail_client, email: Email):

    with mail_client.get_connection():

        assert send_email(email) == 1

