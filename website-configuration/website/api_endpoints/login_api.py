"""API handling the Oauth authentications of the users using ORCID.

Implementative details
----------------------
The API is implemented using authlib's OAuth 2.0 framework.
"""
import os
from flask import redirect, jsonify, session
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.orcid import make_orcid_blueprint

# from flask_login import logout_user
from ..application import app
from ..models import User


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

blueprint = make_orcid_blueprint(
    client_id=os.environ.get("ORCID_CLIENT_ID"),
    client_secret=os.environ.get("ORCID_CLIENT_SECRET"),
    scope="/authenticate",
    authorized_url="/login/orcid/callback",
    redirect_to="orcid_logged_in"
)

app.register_blueprint(
    blueprint,
)


@oauth_authorized.connect_via(blueprint)
def orcid_logged_in(orcid_blueprint, token):
    """Internal route to handle the ORCID OAuth callback."""
    # if not orcid_blueprint.authorized:
    #     return jsonify({"success": False, "error": "Authorization failed."})

    return token

    # Retrieve the ORCID ID of the authenticated user
    # resp = orcid.get('orcid', token=token)
    # orcid_id = resp.json().get('orcid')
    orcid_id = "0000-0002-1825-0097"

    _user = User.from_orcid(orcid_id)

    return redirect("/upload")


@oauth_authorized.connect
def redirect_to_next_url(orcid_blueprint, token):
    """Redirect to the next URL."""
    return token


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
