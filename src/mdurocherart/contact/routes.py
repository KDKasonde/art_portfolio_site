from flask import render_template, request, jsonify, abort, redirect, url_for, flash
from mdurocherart.contact import bp
from mdurocherart.contact.models import send_email, format_email, send_email_with_attachments
from mdurocherart.utils import _validate_file


@bp.route("/", methods=["GET"])
def homepage():
    return render_template("contact/homepage.html")


@bp.route("/process_contact", methods=["POST"])
def process_contact():
    req = request.form.to_dict()
    image_file = request.files['input-upload']
    accept_file, status = _validate_file(image_file)
    if not accept_file:
        flash('Please only attach png or jpeg files.')
        return redirect(url_for('contact.homepage'))
    email_obj = format_email(req, image_file)
    if email_obj.subject == 'quote':
        status = send_email_with_attachments(email_obj)
    else:
        status = send_email(email_obj)
    if status is not True:
        flash('There seems to be an with error your request, please try again later!')
        return redirect(url_for('contact.homepage'))
    flash('Thank you for reaching out!')
    return redirect(url_for('contact.homepage'))
