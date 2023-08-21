from flask import Blueprint

bp = Blueprint("about", __name__)

from mdurocherart.about import routes
