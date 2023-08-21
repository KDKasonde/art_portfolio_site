from flask import Blueprint

bp = Blueprint("high_quality_view", __name__)

from mdurocherart.high_quality_view import routes