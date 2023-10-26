"""API handling the Oauth authentications of the users using ORCID.

Implementative details
----------------------
The API is implemented using authlib's OAuth 2.0 framework.
"""
import os
from flask import redirect, session, flash
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.orcid import make_orcid_blueprint
from requests import Response
from flask_dance.consumer.requests import OAuth2Session

# from flask_login import logout_user
from ..application import app
from ..models import User


class JsonOath2Session(OAuth2Session):
    def __init__(self, *args, **kwargs):
        """
          custom json session to ensure we are getting back json from orchid
        """
        super(JsonOath2Session, self).__init__(*args, **kwargs)
        self.headers["Content-Type"] = "application/orcid+json"
        self.headers["Authorization"] = f"Bearer {self.token['access_token']}"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

blueprint = make_orcid_blueprint(
    client_id=os.environ.get("ORCID_CLIENT_ID"),
    client_secret=os.environ.get("ORCID_CLIENT_SECRET"),
    scope="/authenticate",
    authorized_url="/login/orcid/callback",
    session_class=JsonOath2Session
)

app.register_blueprint(
    blueprint,
)


@oauth_authorized.connect_via(blueprint)
def orcid_logged_in(orcid_blueprint, token):
    """Internal route to handle the ORCID OAuth callback."""
    app.logger.info("Logging attempt")
    if not token:
        app.logger.info("Failed to log in.")
        return False

    # get the orcid id information
    # ORCID API calls require that the orcid id be in the request, so that needs
    # to be extracted from the token prior to making any requests
    orcid_user_id = token['orcid']

    response: Response = orcid_blueprint.session.get(
        f"{orcid_user_id}/record",
    )

    if not response.ok:
        app.logger.info(
            "Failed to get ORCID User Data associated to %s, status: %s, url: %s, header: %s, access token: %s", orcid_user_id, response.status_code, response.url, response.headers, token['access_token']
        )
        return False

    orcid_record = response.json()

    orcid_person = orcid_record['person']
    email = orcid_person["emails"]["email"][0]["email"]
    first_name = orcid_person['name']['given-names']['value']
    last_name = orcid_person['name']['family-name']['value']

    _user = User.from_orcid(
        orcid=orcid_user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    return redirect("/upload")


# @oauth_authorized.connect
# def redirect_to_next_url(orcid_blueprint, token):
#     """Redirect to the next URL."""
#     return token


@oauth_error.connect
def orcid_error(orcid_blueprint, error, error_description, error_uri):
    print("in oauth_error")
    print(error)
    print(error_description)
    print(error_uri)

    session['orcid_status'] = error


# Logout route to clear the session
@app.route("/logout")
def logout():
    """Logout route to clear the session."""
    User.logout()
    return redirect("/")
