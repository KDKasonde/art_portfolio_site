from flask import Blueprint

bp = Blueprint("home", __name__)

from website.home import routes # noqa
