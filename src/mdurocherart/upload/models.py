from flask import current_app
from json import loads
from typing import Dict
from pathlib import Path
from PIL import Image
from io import BytesIO
from werkzeug.datastructures.file_storage import FileStorage


DOCUMENT = "images"
PULL_IMAGE_VIEW = 'pull_image_view'
IMAGE_GALLERY = Path(__file__).parent.parent.joinpath('static', 'assets')
PNG_FILE_ENDING = ['png']
JPEG_FILE_ENDINGS = ['jpg', 'jpeg']


def pull_image(image_id: str) -> Dict[str, str]:
    image_info = current_app.COUCHDB.get_view(document=DOCUMENT, view=PULL_IMAGE_VIEW, keys=image_id)

    return loads(image_info)


def put_image(image: FileStorage, name: str, description: str, art_style: str):
    status = _save_images(image=image)
    if status == 400:
        return 400
    #TODO write couchdb put request and handling here
    return


def _save_images(image:FileStorage):
    try:
        file_ending = _check_file_ending(image.filename)

        if file_ending in PNG_FILE_ENDING:
            png_image = Image.open(image)
            # jpg_image = _convert_png_to_jpg(image)
        else:
            jpg_image = Image.open(image)
            png_image = _convert_jpg_to_png(image)

        png_image.save(IMAGE_GALLERY.joinpath('gallery/testing.png'))
        jpg_image.save(IMAGE_GALLERY.joinpath('gallery_jpg/testing.jpg'))
    except ValueError as e:
        return 400
    return 200


def _check_file_ending(filename: str):
    file_ending = filename.split('.')[-1]
    if file_ending.lower() not in JPEG_FILE_ENDINGS+PNG_FILE_ENDING:
        raise ValueError(f"incorrect file type has been pass was expecting PNG or JPEG instead got {file_ending}")
    return file_ending.lower()


def _convert_jpg_to_png(image):

    with BytesIO() as picture:
        image.save(picture, format='PNG')
        picture.seek(0)
        picture_png = Image.open(picture)
        picture_png.load()
    return picture_png


def _convert_png_to_jpg(image):
    rgb_image = image.convert(('RGB'))
    with BytesIO() as picture:
        rgb_image.save(picture, format='JPEG')
        picture.seek(0)
        picture_jpg = Image.open(picture)
        picture_jpg.load()
    return picture_jpg
