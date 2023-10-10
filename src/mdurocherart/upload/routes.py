from flask import render_template, request, jsonify, current_app, redirect, url_for
from mdurocherart.upload import bp
from mdurocherart.upload.models import put_image
from mdurocherart.login_manager import login_required, login_user
from pathlib import Path
import os
from random import shuffle


@bp.route("/", methods=["GET"])
def home():
    return render_template("upload/login.html")


@bp.route("/homepage", methods=["GET"])
@login_required
def homepage():
    return render_template("upload/homepage.html", logged_in=True)


@bp.route("/loggedin", methods=['GET'])
@login_required
def testing():
    return jsonify(success=True)


@bp.route("/login", methods=["POST"])
def login():
    data = request.form.to_dict()
    if current_app.login_manager.verify(username=data['current-username'], password=data['current-password'].encode('utf-8')):
        login_user()
        return redirect(url_for('upload.homepage'), code=301)
    else:
        return redirect(url_for('upload.home'), code=301)


@bp.route("/interactive_view", methods=["GET"])
@login_required
def interactive_view():
    gallery_folder = Path(__file__).parent.parent.joinpath("static", "assets", "gallery_jpg")
    image_list = os.listdir(gallery_folder)
    shuffle(image_list)
    return render_template("upload/available_images.html", image_list=image_list, logged_in=True)


@bp.route("/get_image_details", methods=["GET"])
@login_required
def get_image_details():
    image = request.args.get('image_id')

    raise NotImplementedError
    return


@bp.route("/add_new_image", methods=['GET'])
@login_required
def add_new_image():
    return render_template('upload/add_new_image.html')

@bp.route("/upload_image", methods=["POST"])
@login_required
def upload_image():
    data = request.form.to_dict()
    image_file = request.files['img']

    image = put_image(
        image=image_file,
        name=data['name'],
        description='testing upload',
        art_style='fake'
    )
    return jsonify(success=True)

