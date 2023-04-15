from flask import Blueprint

bp = Blueprint("high_quality_view", __name__)

from website.high_quality_view import routes