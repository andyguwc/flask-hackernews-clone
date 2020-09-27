# -*- coding: utf-8 -*-
"""Post models."""
import datetime as dt

from flask_hackernews_clone.database import (
    Column,
    SearchableMixin,
    PkModel,
    db,
    reference_col,
    relationship,
)
from flask_hackernews_clone.extensions import bcrypt


class Post(SearchableMixin, PkModel):
    """Post"""
    __searchable__ = ["body"]

    __tablename__ = "posts"
    title = Column(db.String(80))
    body = Column(db.Text)
    author_id = Column(db.Integer, db.ForeignKey("users.id"))
