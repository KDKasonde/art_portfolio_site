import os
from flask import Blueprint

bp = Blueprint("upload", __name__)

from mdurocherart.upload import routes