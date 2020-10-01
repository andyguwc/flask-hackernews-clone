# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ImageForm(FlaskForm):
    image_file = FileField(validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField("Submit")