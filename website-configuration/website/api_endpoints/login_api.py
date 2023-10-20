"""API handling the Oauth authentications of the users using ORCID.

Implementative details
----------------------
The API is implemented using authlib's OAuth 2.0 framework.
"""
from flask import redirect
from ..application import app
from ..models import User
# from ..oauth import orcid  # Import your Authlib OAuth instance


@app.route('/login/orcid/callback')
def orcid_callback():
    """Internal route to handle the ORCID OAuth callback."""
    if User.is_authenticated():
        return redirect("/upload")
    # Exchange the authorization code for an access token
    # TODO! ADD SUPPORT FOR PROPER ORCID AUTHENTICATION
    # WHEN SWITCHING TO ONLINE VERSION.
    # token = orcid.authorize_access_token()

    # Retrieve the ORCID ID of the authenticated user
    # resp = orcid.get('orcid', token=token)
    # orcid_id = resp.json().get('orcid')
    orcid_id = "0000-0002-1825-0097"

    _user = User.from_orcid(orcid_id)

    return redirect("/upload")

# Login route to initiate ORCID OAuth
@app.route('/login/orcid', methods=['GET'])
def orcid_login():
    """Login route to initiate ORCID OAuth."""
    return redirect("/login/orcid/callback")

# Logout route to clear the session
@app.route('/logout')
def logout():
    """Logout route to clear the session."""
    User.logout()
    return redirect("/")