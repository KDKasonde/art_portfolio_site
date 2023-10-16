from werkzeug.datastructures.file_storage import FileStorage
from flask import current_app
from typing import Tuple, Dict
from mdurocherart.constants import (
    DOCUMENT,
    PULL_IMAGE_VIEW,
    PULL_IMAGE_LOCATION,
    IMAGE_GALLERY,
    PNG_FILE_ENDING,
    JPEG_FILE_ENDINGS
)


def pull_image(image_id: str) -> Dict[str, str]:

    try:
        response = current_app.couchdb.get_view(document=DOCUMENT, view=PULL_IMAGE_VIEW, keys=image_id)

    except Exception as e:
        return 500, response
    rows = response['rows']
    if rows:
        values = response['rows'][0]['value']
    else:
        values = rows
    return 200, values


def get_images():
    try:
        response = current_app.couchdb.get_view(document=DOCUMENT, view=PULL_IMAGE_LOCATION)

    except Exception as e:
        return 500, response
    values = response['rows']
    images = list(map(add_jpg_file_extension, [x['value'] for x in values]))

    return 200, images


def add_jpg_file_extension(string: str) -> str:
    return string + '.jpg'


def _validate_file(uploaded_file: FileStorage) -> Tuple[bool, int]:
    """
    Function to ensure the file types given are accept able.
    Parameters
    ----------
    uploaded_files: FileStorage
    the files that have been received.

    Returns
    -------
    bool
    """
    filename = uploaded_file.filename
    split_filename = filename.split('.')

    if len(split_filename) != 2 or split_filename[-1].lower() not in current_app.config['ACCEPTED_FILE_TYPES']:
        return False, 404
