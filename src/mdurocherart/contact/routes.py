from flask import render_template, request, jsonify

from mdurocherart.contact import bp
from mdurocherart.contact.models import send_email, format_email, send_email_with_attachments


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("contact/homepage.html")


@bp.route("/process_contact", methods=["POST"])
def process_contact():
    req = request.form.to_dict()
    image_file = request.files['input-upload']
    email_obj = format_email(req, image_file)
    if email_obj.subject == 'quote':
        status = send_email_with_attachments(email_obj)
    else:
        status = send_email(email_obj)
    return jsonify(success=True)
