from flask import render_template
from pathlib import Path
from random import shuffle
import os
from website.home import bp


@bp.route('/', methods=['GET'])
def homepage():
    gallery_folder = Path(__file__).parent.parent.joinpath("static/assets/gallery/")
    image_list = os.listdir(gallery_folder)
    shuffle(image_list)
    return render_template("home/homepage.html", image_list=image_list)
