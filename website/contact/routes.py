from flask import render_template

from website.contact import bp


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("contact/homepage.html")