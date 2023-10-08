from flask import render_template, request, jsonify, current_app, redirect, url_for
from mdurocherart.upload import bp
from mdurocherart.login_manager import login_required, login_user


@bp.route("/", methods=["GET"])
def home():
    return render_template("upload/login.html")


@bp.route("/loggedin", methods=['GET'])
@login_required
def testing():
    return jsonify(success=True)

@bp.route("/login", methods=["POST"])
def login():
    data = request.form.to_dict()
    if current_app.login_manager.verify(username=data['current-username'], password=data['current-password'].encode('utf-8')):
        login_user()
    else:
        return redirect(url_for('upload.home'), code=301)
    return jsonify(success=True)


@bp.route("/homepage", methods=["GET"])
@login_required
def process_contact():
    return jsonify(success=True)
