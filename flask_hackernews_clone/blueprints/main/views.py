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
    abort,
    g
)
from flask_login import current_user, login_required, login_user

from flask_hackernews_clone.blueprints.main.forms import (
    EditPostForm,
    LoginForm,
    PostForm,
)
from flask_hackernews_clone.blueprints.main.models import Post
from flask_hackernews_clone.blueprints.user.models import User
from flask_hackernews_clone.extensions import login_manager
from flask_hackernews_clone.utils import flash_errors
from flask_hackernews_clone.search.forms import SearchForm

blueprint = Blueprint("main", __name__, static_folder="static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.before_app_request
def before_request():
    """Make SearchForm available on all pages
    """
    if current_user.is_authenticated:
        g.search_form = SearchForm()


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
            redirect_url = request.args.get("next") or url_for(
                "user.user_home", username=current_user.username
            )
            return redirect(redirect_url)
        else:
            flash_errors(form)
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    return render_template(
        "main/home.html", form=form, posts=posts, pagination=pagination
    )


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    """Create new post."""
    form = PostForm()
    if form.validate_on_submit():
        Post.create(
            title=form.title.data,
            body=form.body.data,
            author=current_user._get_current_object(),
        )
        flash("You just posted!", "success")
        return redirect(url_for("user.user_home", username=current_user.username))
    return render_template("main/create_post.html", form=form)


@blueprint.route("/post/<int:id>")
def post(id):
    """View a post by id
    """
    post = Post.query.get_or_404(id)
    return render_template("main/home.html", posts=[post])


@blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """Edit a post by id
    """
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = EditPostForm()
    if form.validate_on_submit():
        post.update(
            title=form.title.data,
            body=form.body.data,
        )
        flash("Your post has been updated", "success")
        return redirect(url_for("main.post", id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template("main/edit_post.html", form=form)
    

@blueprint.route("/search")
@login_required
def search():
    """Search for posts
    """
    if not g.search_form.validate():
        return redirect(url_for("main.home"))
    page = request.args.get("page", 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config["POSTS_PER_PAGE"])
    next_url = url_for("main.search", q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config["POSTS_PER_PAGE"] else None
    prev_url = url_for("main.search", q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template("main/search.html", posts=posts, next_url=next_url, prev_url=prev_url)

