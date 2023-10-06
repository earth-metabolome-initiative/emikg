"""Submodule providing instance of orcid authentication using authlib."""
# We store in system variables the client id and secret.
import os
from .oauth import oauth

orcid = oauth.register(
    name="orcid",
    client_id=os.environ["YOUR_ORCID_CLIENT_ID"],
    client_secret=os.environ["YOUR_ORCID_CLIENT_SECRET"],
    access_token_url="https://orcid.org/oauth/token",
    access_token_params=None,
    authorize_url="https://orcid.org/oauth/authorize",
    authorize_params=None,
    api_base_url="https://pub.orcid.org/v3.0",
    client_kwargs=None,
)