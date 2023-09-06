"""API handling the Oauth authentications of the users using ORCID.

Implementative details
----------------------
The API is implemented using authlib's OAuth 2.0 framework.
"""
from flask import redirect, url_for

from ..app import app
from ..models import User
from ..oauth import orcid  # Import your Authlib OAuth instance


@app.route('/login/orcid/callback')
def orcid_callback():
    """Internal route to handle the ORCID OAuth callback."""
    # Exchange the authorization code for an access token
    token = orcid.authorize_access_token()

    # Retrieve the ORCID ID of the authenticated user
    resp = orcid.get('orcid', token=token)
    orcid_id = resp.json().get('orcid')

    _user = User.from_orcid(orcid_id)

    return redirect(url_for('dashboard'))  # Redirect to the profile page or another page

# Login route to initiate ORCID OAuth
@app.route('/login/orcid')
def orcid_login():
    """Login route to initiate ORCID OAuth."""
    return orcid.authorize_redirect(url_for('/login/orcid/callback', _external=True))

# Logout route to clear the session
@app.route('/logout')
def logout():
    """Logout route to clear the session."""
    User.logout()