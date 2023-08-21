from flask import render_template

from mdurocherart.contact import bp


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("contact/homepage.html")