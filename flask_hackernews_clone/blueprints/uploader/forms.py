# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired


class ImageForm(FlaskForm):
    image_file = FileField(validators=[FileRequired()])
    submit = SubmitField("Submit")