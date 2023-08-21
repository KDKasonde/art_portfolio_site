from flask import render_template, current_app
from pathlib import Path
from random import shuffle
import os
from mdurocherart.home import bp


@bp.route('/', methods=['GET'])
def homepage():
    gallery_folder = Path(__file__).parent.parent.joinpath("static", "assets", "gallery_jpg")
    image_list = os.listdir(gallery_folder)
    shuffle(image_list)
    return render_template("home/homepage.html", image_list=image_list)
