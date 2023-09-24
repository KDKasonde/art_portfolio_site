import smtpd
import asyncore


class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(self, host, port):
        smtpd.SMTPServer(localaddr=(host, port), remoteaddr=None)


if __name__ == "__main__":
    smtp_server = FakeSMTPServer(host='localhost', port=1025)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
