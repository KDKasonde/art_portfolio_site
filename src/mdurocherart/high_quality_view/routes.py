from flask import render_template, request, abort
from mdurocherart.high_quality_view import bp
from mdurocherart.utils import pull_image, check_image_exist


@bp.route("/high_quality_view", methods=["GET"])
def get_image():
    image_id = request.args.get('image_id')
    exists = check_image_exist(image_id)
    if exists is not True:
        return abort(404)
    status, image_info = pull_image(image_id=image_id)
    if status != 200:
        return abort(status)
    if image_info:
        return render_template('high_quality_view/homepage.html', image_info=image_info, image_id=image_id)
    return abort(404)
