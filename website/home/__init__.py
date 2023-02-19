from flask import Blueprint

bp = Blueprint("home", __name__)

from art_portfolio_site.website.home import routes # noqa
