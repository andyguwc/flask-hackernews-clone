# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flask_hackernews_clone.blueprints.user.forms import EditProfileForm

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Edit user profile."""
    form = EditProfileForm()
    if form.validate_on_submit():
        update_inputs = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "about": form.about.data,
        }
        current_user.update(**update_inputs)
        flash("Your profile is updated!", "success")
        return redirect(url_for("main.home"))

    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.about.data = current_user.about
    return render_template("users/edit_profile.html", form=form)
