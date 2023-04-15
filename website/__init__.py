from flask import Flask


def create_website():

    website = Flask(__name__)

    from website.home import bp as home
    website.register_blueprint(home)

    from website.about import bp as about
    website.register_blueprint(about, url_prefix="/about")

    from website.high_quality_view import bp as high_quality_view
    website.register_blueprint(high_quality_view, url_prefix="/high_quality_view")

    return website
