from flask import render_template

from art_portfolio_site.website.about import bp


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("about/homepage.html")


