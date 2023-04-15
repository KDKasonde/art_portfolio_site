from flask import render_template, request, redirect, url_for
import os
from pathlib import Path

from website.high_quality_view import bp


@bp.route("/", methods=["GET"])
def homepage():
    image = request.args.get('image_id')
    gallery_folder = Path(__file__).parent.parent.joinpath("static", "assets", "gallery_jpg")
    image_list = os.listdir(gallery_folder)
    for image_file in image_list:
        if image == image_file.split(".")[0]:
            return redirect(url_for("high_quality_view.homepage", image=image))

    return render_template("high_quality_view/homepage.html")