"""API handling the Oauth authentications of the users using ORCID.

Implementative details
----------------------
The API is implemented using authlib's OAuth 2.0 framework.
"""
from typing import Dict, Optional
import os
from flask import redirect, session
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.orcid import make_orcid_blueprint, LocalProxy
from requests import Response
import requests

# from flask_login import logout_user
from ..application import app
from ..models import User


class PublicORCIDAPI:
    """Define the ORCID API class."""

    def __init__(self) -> None:
        """Initialize the ORCID API."""
        reponse: Response = requests.post(
            "https://orcid.org/oauth/token",
            data={
                "client_id": os.environ.get("ORCID_CLIENT_ID"),
                "client_secret": os.environ.get("ORCID_CLIENT_SECRET"),
                "grant_type": "client_credentials",
                "scope": "/read-public",
            },
            timeout=10,
        )

        if not reponse.ok:
            raise RuntimeError(
                f"Failed to get ORCID public access token, status: {reponse.status_code}."
            )

        self._read_public_access_token: Dict[str, str] = reponse.json()

    @property
    def access_token(self):
        """Return the access token."""
        return self._read_public_access_token["access_token"]

    @property
    def token_type(self):
        """Return the token type."""
        return self._read_public_access_token["token_type"]

    @property
    def refresh_token(self):
        """Return the refresh token."""
        return self._read_public_access_token["refresh_token"]

    @property
    def expires_in(self):
        """Return the expiration time."""
        return self._read_public_access_token["expires_in"]

    @property
    def scope(self):
        """Return the scope."""
        return self._read_public_access_token["scope"]


class PublicORCIDUserData:
    """Define the Public ORCID User Data class."""

    def __init__(self, user_orcid_id: str, api: PublicORCIDAPI) -> None:
        """Initialize the Public ORCID User Data"""
        response: Response = requests.get(
            f"https://pub.orcid.org/v2.1/{user_orcid_id}/personal-details",
            headers={
                "Content-Type": "application/orcid+json",
                "Authorization": f"Bearer {api.access_token}",
            },
            timeout=10,
        )

        if not response.ok:
            raise RuntimeError(
                f"Failed to get ORCID User Data associated to {user_orcid_id}, status: {response.status_code}"
            )

        self._orcid_record: Dict[str, str] = response.json()

    @property
    def given_name(self) -> Optional[str]:
        """Return the given name."""
        if "name" not in self._orcid_record:
            return None
        if "given-names" in self._orcid_record["name"]:
            return self._orcid_record["name"]["given-names"].get("value", None)
        return None

    @property
    def family_name(self) -> Optional[str]:
        """Return the family name."""
        if "name" not in self._orcid_record:
            return None
        if "family-name" in self._orcid_record["name"]:
            return self._orcid_record["name"]["family-name"].get("value", None)
        return None

    @property
    def biography(self) -> Optional[str]:
        """Return the biography."""
        if "biography" in self._orcid_record:
            return self._orcid_record["biography"].get("value", None)
        return None


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

blueprint: LocalProxy = make_orcid_blueprint(
    client_id=os.environ.get("ORCID_CLIENT_ID"),
    client_secret=os.environ.get("ORCID_CLIENT_SECRET"),
    scope="/authenticate",
    authorized_url="/login/orcid/callback",
)

blueprint.public_api = PublicORCIDAPI()

app.register_blueprint(
    blueprint,
)


@oauth_authorized.connect_via(blueprint)
def orcid_logged_in(orcid_blueprint: LocalProxy, token):
    """Internal route to handle the ORCID OAuth callback."""
    app.logger.info("Logging attempt")
    if not token:
        app.logger.info("Failed to log in.")
        return False

    # get the orcid id information
    # ORCID API calls require that the orcid id be in the request, so that needs
    # to be extracted from the token prior to making any requests
    orcid_user_id = token["orcid"]

    try:
        user_data = PublicORCIDUserData(orcid_user_id, orcid_blueprint.public_api)
    except RuntimeError:
        return False

    _user = User.from_orcid(
        orcid=orcid_user_id,
        first_name=user_data.given_name,
        last_name=user_data.family_name,
        description=user_data.biography,
    )

    return redirect("/upload")


# @oauth_authorized.connect
# def redirect_to_next_url(orcid_blueprint: LocalProxy, token):
#     """Redirect to the next URL."""
#     return token


@oauth_error.connect
def orcid_error(
    orcid_blueprint: LocalProxy, error: str, error_description: str, error_uri: str
):
    """Internal route to handle the ORCID OAuth callback."""
    print("in oauth_error")
    print(error)
    print(error_description)
    print(error_uri)

    session["orcid_status"] = error


# Logout route to clear the session
@app.route("/logout")
def logout():
    """Logout route to clear the session."""
    User.logout()
    return redirect("/")
