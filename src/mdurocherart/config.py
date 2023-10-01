import os
from dotenv import find_dotenv, load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent.parent.joinpath('.env')

load_dotenv(dotenv_path)


class Config(object):
    """Base config, uses staging database server."""
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
    COUCHDB_DATABASE = os.getenv('COUCHDB_DATABASE')
    COUCHDB_USERNAME = os.getenv('COUCHDB_USERNAME')
    COUCHDB_PASSWORD = os.getenv('COUCHDB_PASSWORD')
    COUCHDB_HOST = os.getenv('COUCHDB_HOST', default='127.0.0.1')
    COUCHDB_PORT = os.getenv('COUCHDB_PORT', default=5984)


class ProductionConfig(Config):
    """Production config class"""


class DevelopmentConfig(Config):
    """Development config class"""



class TestingConfig(Config):
    """Testing config class"""
    MAIL_SERVER = os.getenv('MAIL_SERVER', default='localhost')
    MAIL_PORT = os.getenv('MAIL_PORT', default=1025)


def get_config(env: str):
    if env == 'prod':
        return ProductionConfig
    elif env == 'dev':
        return DevelopmentConfig
    elif env == 'test':
        return TestingConfig
    else:
        raise ValueError
