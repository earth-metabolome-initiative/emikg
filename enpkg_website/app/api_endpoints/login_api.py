"""API handling the Oauth authentications of the users using ORCID.

Implementative details
----------------------
The API is implemented using authlib's OAuth 2.0 framework.
"""
from flask import redirect, url_for, session, request
from ..app import app
from ..models import User
from ..oauth import orcid # Import your Authlib OAuth instance


# ORCID OAuth callback route
@app.route('/orcid/callback')
def orcid_callback():
    # Exchange the authorization code for an access token
    token = orcid.authorize_access_token()

    # Retrieve the ORCID ID of the authenticated user
    resp = orcid.get('orcid', token=token)
    orcid_id = resp.json().get('orcid')

    # Check if the user exists in your database
    user = User.query.filter_by(orcid=orcid_id).first()

    if not user:
        # If the user doesn't exist, you can create a new user in your database
        # Example:
        # user = User(orcid=orcid_id)
        # db.session.add(user)
        # db.session.commit()

        # For demonstration purposes, we'll store the ORCID ID in the session
        session['orcid_id'] = orcid_id

    # Store user data in the session or perform any other desired actions
    # Example: session['user_id'] = user.id

    return redirect(url_for('profile'))  # Redirect to the profile page or another page

# Login route to initiate ORCID OAuth
@app.route('/login')
def login():
    # Redirect the user to the ORCID OAuth authorization URL
    return orcid.authorize_redirect(url_for('orcid_callback', _external=True))

# Logout route to clear the session
@app.route('/logout')
def logout():
    """Logout route to clear the session."""
    session.pop('orcid_id', None)
    return redirect(url_for('login'))