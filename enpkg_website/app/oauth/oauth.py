"""Submodule providing instance of oauth using authlib."""
from authlib.integrations.flask_client import OAuth
from ..app import app

oauth = OAuth(app)