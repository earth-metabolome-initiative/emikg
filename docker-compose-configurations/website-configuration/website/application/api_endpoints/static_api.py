"""Endpoints for static files."""

import os

from flask import send_from_directory

from ..application import app


@app.route('/static/css/<path:path>')
def send_css(path: str):
    """Send css files."""
    return send_from_directory(os.path.join('static', 'css'), path)


@app.route('/static/js/<path:path>')
def send_js(path: str):
    """Send js files."""
    return send_from_directory(os.path.join('static', 'js'), path)


@app.route('/static/img/<path:path>')
def send_img(path: str):
    """Send img files."""
    return send_from_directory(os.path.join('static', 'img'), path)