# -*- coding: utf-8 -*-
from flask import current_app

from flask_hackernews_clone.extensions import celery


@celery.task
def make_file(fname, content):
    """Test task to ensure celery works. 
    Visit http://localhost:5000/makefile/foot.txt/bar
    Should produce a local file in main directory
    """
    # Further test using current app context
    app = current_app._get_current_object()
    
    with open(fname, "w") as f:
        f.write(content)
        f.write(f"Post per page {app.config['POSTS_PER_PAGE']}")

