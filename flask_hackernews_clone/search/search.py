# -*- coding: utf-8 -*-
"""Implementing Search Backend (with Elasticsearch)."""

from flask import current_app

def add_to_index(index, model):
    """Add index for a SQLAlchemy model
    """
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Remove index
    """
    if not current_app.elasticsearch:
        return
    
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """
    Takes an index and a text to search for
    Use multi_match to search across multiple fields
    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']

# if __name__ == '__main__':
#     from flask_hackernews_clone.blueprints.main.models import Post
#     for post in Post.query.all():
#         add_to_index('posts', post)
#     query_index('posts', 'very interesting', 1, 100)