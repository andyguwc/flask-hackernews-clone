# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flask_hackernews_clone.blueprints.main.models import Post
from flask_hackernews_clone.blueprints.user.forms import EditProfileForm
from flask_hackernews_clone.blueprints.user.models import User

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="static")


@blueprint.route("/<username>")
@login_required
def user_home(username):
    """List user posts."""
    user = User.query.filter_by(username=username).first()
    if not user.id == current_user.id:
        redirect(url_for("user.user_home", username=current_user.username))
    posts = current_user.posts.order_by(Post.created_at.desc()).all()
    return render_template("users/user_home.html", posts=posts)


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
        return redirect(url_for("user.user_home"))

    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.about.data = current_user.about
    return render_template("users/edit_profile.html", form=form)
