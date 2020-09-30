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
    abort
)
from werkzeug.utils import secure_filename

from flask_hackernews_clone.blueprints.uploader.forms import ImageForm 
from flask_hackernews_clone import settings

blueprint = Blueprint("uploader", __name__)


@blueprint.route("/upload/", methods=["GET", "POST"])
def upload_image():
    """Upload images
    """
    form = ImageForm()
    if form.validate_on_submit():
        f = form.image_file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(settings.IMAGES_DIR, filename))
        return redirect(url_for("main.home"))
    return render_template("uploader/upload.html", form=form)


@blueprint.route("/uploads/<filename>")
def uploads(filename):
    """View uploads
    """
    return send_from_directory(settings.IMAGES_DIR, filename)