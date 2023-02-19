from flask import Blueprint

bp = Blueprint("about", __name__)

from art_portfolio_site.website.about import routes
