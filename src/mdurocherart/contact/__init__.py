from flask import Blueprint

bp = Blueprint("contact", __name__)

from mdurocherart.contact import routes
