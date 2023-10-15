from flask import render_template, request, redirect, url_for, abort
import os
from pathlib import Path
from mdurocherart.high_quality_view.models import check_image_exist
from mdurocherart.high_quality_view import bp


@bp.route("/", methods=["GET"])
def homepage():
    image = request.args.get('image')
    exists = check_image_exist(image)
    if exists is not True:
        return abort(400)
    return render_template("high_quality_view/homepage.html", image=image)


@bp.route("/getImage", methods=["GET"])
def get_image():
    image = request.args.get('image_id')
    exists = check_image_exist(image)
    if exists is not True:
        return abort(400)

    return redirect(url_for("high_quality_view.homepage", image=image), code=301)
