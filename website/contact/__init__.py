from flask import Blueprint

bp = Blueprint("contact", __name__)

from website.contact import routes
