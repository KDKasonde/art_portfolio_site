from flask import render_template

from art_portfolio_site.website.home import bp


@bp.route('/', methods=['GET'])
def homepage():
    return render_template("home/homepage.html")
