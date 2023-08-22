from flask import render_template, request, jsonify

from mdurocherart.contact import bp
from mdurocherart.contact.models import send_email, format_email


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("contact/homepage.html")


@bp.route("/process_contact", methods=["POST"])
def process_contact():
    req = request.json
    email_obj = format_email(req)
    status = send_email(email_obj)
    return jsonify(success=True)
