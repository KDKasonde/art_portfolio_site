from werkzeug.datastructures.file_storage import FileStorage
from flask import current_app
from typing import Tuple


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
