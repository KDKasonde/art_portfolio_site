from pathlib import Path
import os
IMAGE_GALLERY = Path(__file__).parent.parent.joinpath('static', 'assets')


def check_image_exist(image: str) -> bool:
    image_folder = IMAGE_GALLERY.joinpath('gallery')
    image_list = list(image_folder.glob("*"))
    image_list = map(os.path.basename, image_list)
    image += '.png'
    if image in image_list:
        return True
    return False

