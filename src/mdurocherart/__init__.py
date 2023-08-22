import os

from flask import Flask
from werkzeug.utils import import_string
from mdurocherart.config import TestingConfig, get_config
from typing import Optional


def create_app(env: Optional[str] = None):

    mdurocherart = Flask(__name__)

    if env is None:
        env = os.getenv('TARGET_ENV', default='dev')

    config_obj = get_config(env)
    cfg = import_string(f'mdurocherart.config.{config_obj.__name__}')
    mdurocherart.config.from_object(cfg)

    from mdurocherart.home import bp as home
    mdurocherart.register_blueprint(home)

    from mdurocherart.about import bp as about
    mdurocherart.register_blueprint(about, url_prefix="/about")

    from mdurocherart.high_quality_view import bp as high_quality_view
    mdurocherart.register_blueprint(high_quality_view, url_prefix="/high_quality_view")

    from mdurocherart.contact import bp as contact
    mdurocherart.register_blueprint(contact, url_prefix="/contact")

    return mdurocherart
