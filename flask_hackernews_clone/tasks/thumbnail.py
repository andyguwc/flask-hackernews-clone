# -*- coding: utf-8 -*-
import os

from flask import current_app
from PIL import Image

from flask_hackernews_clone import settings
from flask_hackernews_clone.extensions import celery


@celery.task
def make_thumbnails(file_path, thumbnails=[]):
    """Take an image file directory and thumnail dimensions to generate a thumbnail image 
    """
    os.chdir(settings.IMAGES_DIR)
    path, file = os.path.split(file_path)
    file_name, ext = os.path.splitext(file)

    zip_file = f"{file_name}.zip"
    results = {'archive_path': f"{settings.MEDIA_URL}images/{zip_file}"}
    try:
        img = Image.open(file_path)
        zipper = ZipFile(zip_file, 'w')
        zipper.write(file)
        os.remove(file_path)
        for w, h in thumbnails:
            img_copy = img.copy()
            img_copy.thumbnail((w, h))
            thumbnail_file = f'{file_name}_{w}x{h}.{ext}'
            img_copy.save(thumbnail_file)
            zipper.write(thumbnail_file)
            os.remove(thumbnail_file)

        img.close()
        zipper.close()
    except IOError as e:
        print(e)

    return results
