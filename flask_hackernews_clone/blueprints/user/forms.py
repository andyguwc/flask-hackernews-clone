# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class EditProfileForm(FlaskForm):
    first_name = StringField("First name", validators=[Length(0, 30)])
    last_name = StringField("Last name", validators=[Length(0, 30)])
    about = TextAreaField("About me")
    submit = SubmitField("Submit")
