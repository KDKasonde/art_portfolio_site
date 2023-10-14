from flask import current_app
from typing import Dict
from pathlib import Path
from PIL import Image
from io import BytesIO
import os
from werkzeug.datastructures.file_storage import FileStorage


DOCUMENT = "images"
PULL_IMAGE_VIEW = 'pull_image_view'
IMAGE_GALLERY = Path(__file__).parent.parent.joinpath('static', 'assets')
PNG_FILE_ENDING = ['png']
JPEG_FILE_ENDINGS = ['jpg', 'jpeg']


def pull_image(image_id: str) -> Dict[str, str]:

    try:
        response = current_app.couchdb.get_view(document=DOCUMENT, view=PULL_IMAGE_VIEW, keys=image_id)

    except Exception as e:
        return 500, response
    values = response['rows'][0]['value']
    return 200, values


def update_image_document(image_id: str, name: str, description: str, art_style: str, location: str):
    try:
        data = {
                'piece_name': name,
                'piece_description': description,
                'style': art_style,
                'image_id': image_id,
                'location': location
        }

        response = current_app.couchdb.put_document(
            document_id=image_id,
            data=data
        )
    except Exception:
        return 500, response
    return 200, response


def put_image(image: FileStorage, name: str, description: str, art_style: str):
    image_file_name = _generate_image_filename()
    status, save_paths = _save_images(image=image, image_name=image_file_name)
    if status == 400:
        return 400
    couchdb_status, couchdb_response = update_image_document(
        image_id=image_file_name,
        name=name,
        description=description,
        art_style=art_style,
        location=image_file_name
    )
    if couchdb_status != 200:
        os.remove(path=save_paths[0])
        os.remove(path=save_paths[1])
        return couchdb_status, couchdb_response
    return couchdb_status


def delete_image_document(image_id: str):
    png_image = IMAGE_GALLERY.joinpath('gallery', image_id+'.png')
    jpg_image = IMAGE_GALLERY.joinpath('gallery_jpg', image_id+'.jpg')
    try:
        status, response = current_app.couchdb.delete_document(document_id=image_id)
    except Exception:
        return 500, None
    os.remove(path=png_image)
    os.remove(path=jpg_image)

    return status, response


def _generate_image_filename():
    image_folder = IMAGE_GALLERY.joinpath('gallery')
    image_count = len(list(image_folder.glob("*")))
    return f"gallery_image_{image_count+1}"


def _save_images(image: FileStorage, image_name: str):
    try:
        file_ending = _check_file_ending(image.filename)

        if file_ending in PNG_FILE_ENDING:
            png_image = Image.open(image)
            jpg_image = _convert_png_to_jpg(png_image)
        else:
            jpg_image = Image.open(image)
            png_image = _convert_jpg_to_png(jpg_image)
        save_path_png= IMAGE_GALLERY.joinpath(f'gallery/{image_name}.png')
        save_path_jpg = IMAGE_GALLERY.joinpath(f'gallery_jpg/{image_name}.jpg')
        png_image.save(save_path_png)
        jpg_image.save(save_path_jpg)
    except ValueError:
        return 400, None
    return 200, [save_path_png, save_path_jpg]


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
