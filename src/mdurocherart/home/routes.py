from flask import render_template, abort
from random import shuffle
from mdurocherart.home import bp
from mdurocherart.utils import get_images


@bp.route('/', methods=['GET'])
def homepage():
    status, image_list = get_images()
    if status != 200:
        return abort(404)
    shuffle(image_list)
    return render_template("home/homepage.html", image_list=image_list)
