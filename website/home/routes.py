from flask import render_template

from website.home import bp


@bp.route('/', methods=['GET'])
def homepage():
    return render_template("home/homepage.html")
