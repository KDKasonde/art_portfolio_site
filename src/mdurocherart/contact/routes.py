from flask import render_template, request, jsonify

from mdurocherart.contact import bp


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("contact/homepage.html")


@bp.route("/send_email", methods=["POST"])
def send_email():
    print(request.json)
    return jsonify(success=True)
