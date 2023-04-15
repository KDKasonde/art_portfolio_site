from flask import render_template

from website.high_quality_view import bp


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("high_quality_view/homepage.html")