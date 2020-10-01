# -*- coding: utf-8 -*-
"""Image Thumnail Maker."""
import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    send_from_directory,
    abort,
    jsonify
)
from werkzeug.utils import secure_filename
from celery import current_app

from flask_hackernews_clone.blueprints.uploader.forms import ImageForm
from flask_hackernews_clone import settings
from flask_hackernews_clone.tasks.thumbnail import make_thumbnails

blueprint = Blueprint("uploader", __name__)


@blueprint.route("/upload/", methods=["GET", "POST"])
def upload_image():
    """Upload images
    """
    form = ImageForm()
    if form.validate_on_submit():
        # validate submitted image and save to local path
        f = form.image_file.data
        filename = secure_filename(f.filename)
        file_path = os.path.join(settings.IMAGES_DIR, filename)
        f.save(file_path)
        # apply thumnail transformation asynchronously
        task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])
        task_id = task.id
        task_status = task.status 
        return render_template("uploader/upload.html", task_id=task_id)
    return render_template("uploader/upload.html", form=form)


@blueprint.route("/upload_progress/<task_id>")
def upload_progress(task_id):
    """View task status
    """
    return render_template("uploader/upload_progress.html", task_id=task_id)


@blueprint.route("/status/<task_id>")
def task_status(task_id):
    """View task status
    """
    task = current_app.AsyncResult(task_id)
    response_data = {'task_status': task.status, 'task_id': task.id}

    if task.status == 'SUCCESS':
        response_data['results'] = task.get()
    return jsonify(response_data)

    
@blueprint.route("/media/images/<filename>")
def uploads(filename):
    """View uploads
    """
    return send_from_directory(settings.IMAGES_DIR, filename)