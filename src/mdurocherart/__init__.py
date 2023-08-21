from flask import Flask


def create_app():

    mdurocherart = Flask(__name__)

    from mdurocherart.home import bp as home
    mdurocherart.register_blueprint(home)

    from mdurocherart.about import bp as about
    mdurocherart.register_blueprint(about, url_prefix="/about")

    from mdurocherart.high_quality_view import bp as high_quality_view
    mdurocherart.register_blueprint(high_quality_view, url_prefix="/high_quality_view")

    from mdurocherart.contact import bp as contact
    mdurocherart.register_blueprint(contact, url_prefix="/contact")

    return mdurocherart
