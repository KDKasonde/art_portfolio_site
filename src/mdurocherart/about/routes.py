from flask import render_template

from mdurocherart.about import bp


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("about/homepage.html")


