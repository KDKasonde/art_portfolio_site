import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_mailman import Mail
from werkzeug.utils import import_string
from mdurocherart.config import TestingConfig, get_config
from typing import Optional
from mdurocherart.db import CouchdbConnection
from mdurocherart.login_manager import LoginManager

load_dotenv(find_dotenv())


def create_app(env: Optional[str] = None):

    mdurocherart = Flask(__name__)

    if env is None:
        env = os.getenv('TARGET_ENV', default='dev')

    config_obj = get_config(env)
    cfg = import_string(f'mdurocherart.config.{config_obj.__name__}')
    mdurocherart.config.from_object(cfg)
    mdurocherart.secret_key = mdurocherart.config.get('SECRET_KEY')

    mail = Mail(mdurocherart)
    mdurocherart.config['MAIL_CLIENT'] = mail

    couchdb_conn = CouchdbConnection.from_flask_config(mdurocherart)
    mdurocherart.config['COUCHDB'] = couchdb_conn

    loginmanager = LoginManager(username=os.getenv("USERNAME"),
                                password=os.getenv("PASSWORD"),
                                rounds=15,
                                )
    loginmanager.init_app(flask_app=mdurocherart)

    from mdurocherart.home import bp as home
    mdurocherart.register_blueprint(home)

    from mdurocherart.about import bp as about
    mdurocherart.register_blueprint(about, url_prefix="/about")

    from mdurocherart.high_quality_view import bp as high_quality_view
    mdurocherart.register_blueprint(high_quality_view, url_prefix="/high_quality_view")

    from mdurocherart.contact import bp as contact
    mdurocherart.register_blueprint(contact, url_prefix="/contact")

    from mdurocherart.upload import bp as upload
    mdurocherart.register_blueprint(upload, url_prefix=f"/{os.getenv('UPLOAD_URL_PREFIX', default='test')}")

    return mdurocherart
