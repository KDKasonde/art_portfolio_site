from flask import Blueprint

bp = Blueprint("home", __name__)

from mdurocherart.home import routes # noqa
