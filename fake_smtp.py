import smtpd
import asyncore


class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(self, host, port):
        smtpd.SMTPServer(host, port)


if __name__ == "__main__":
    smtp_server = FakeSMTPServer(host='localhost', port=25)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
