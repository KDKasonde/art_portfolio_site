from flask import Flask


def create_website():

    website = Flask(__name__)

    from website.home import bp as home
    website.register_blueprint(home)

    from website.about import bp as about
    website.register_blueprint(about, url_prefix="/about")

    return website
