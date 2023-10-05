from flask import render_template, request, jsonify
from mdurocherart.upload import bp


@bp.route("/", methods=["GET"])
def login():
    return render_template("upload/login.html")


@bp.route("/process_contact", methods=["POST"])
def process_contact():
    return jsonify(success=True)
