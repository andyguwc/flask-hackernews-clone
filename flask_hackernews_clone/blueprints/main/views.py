# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user

from flask_hackernews_clone.blueprints.main.forms import LoginForm, EditPostForm, PostForm
from flask_hackernews_clone.blueprints.main.models import Post
from flask_hackernews_clone.blueprints.user.models import User
from flask_hackernews_clone.extensions import login_manager
from flask_hackernews_clone.utils import flash_errors

blueprint = Blueprint("main", __name__, static_folder="static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """
    Home page.
    Note user log in is also handled here
    """
    form = LoginForm()
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.user_home")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("main/home.html", form=form)


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    """Create new post."""
    form = PostForm()
    if form.validate_on_submit():
        Post.create(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        flash("You just posted!", "success")
        return redirect(url_for("user.user_home", username=current_user.username))
    return render_template("main/create_post.html", form=form)
