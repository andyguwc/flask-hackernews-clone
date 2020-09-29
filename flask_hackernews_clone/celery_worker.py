# -*- coding: utf-8 -*-
from flask_hackernews_clone.extensions import celery, init_celery
from flask_hackernews_clone.app import create_app

app = create_app(config_object="flask_hackernews_clone.settings")
init_celery(celery, app)
