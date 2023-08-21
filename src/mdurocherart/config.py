import os


class Config(object):
    """Base config, uses staging database server."""


class ProductionConfig(Config):
    MAIL_SERVER = os.getenv('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', default=25)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default=True)
    MAIL_USE_SSL = os.getenv('MAIL_TIMEOUT', default=False)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_BACKEND = os.getenv('MAIL_BACKEND')
    MAIL_FILE_PATH = os.getenv('MAIL_FILE_PATH')
    MAIL_USE_LOCALTIME = os.getenv('MAIL_USE_LOCALTIME')

class DevelopmentConfig(Config):
    MAIL_SERVER = os.getenv('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', default=25)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default=True)
    MAIL_USE_SSL = os.getenv('MAIL_TIMEOUT', default=False)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_BACKEND = os.getenv('MAIL_BACKEND')
    MAIL_FILE_PATH = os.getenv('MAIL_FILE_PATH')
    MAIL_USE_LOCALTIME = os.getenv('MAIL_USE_LOCALTIME')


class TestingConfig(Config):
    MAIL_SERVER = os.getenv('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', default=25)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default=True)
    MAIL_USE_SSL = os.getenv('MAIL_TIMEOUT', default=False)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_BACKEND = os.getenv('MAIL_BACKEND')
    MAIL_FILE_PATH = os.getenv('MAIL_FILE_PATH')
    MAIL_USE_LOCALTIME = os.getenv('MAIL_USE_LOCALTIME')
