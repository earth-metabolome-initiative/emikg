import os
from flask import redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from ..app import app

# Configure the OAuth client
oauth = OAuth(app)
oauth.register(
    name='orcid',
    client_id=os.environ.get('ORCID_CLIENT_ID'),
    client_secret=os.environ.get('ORCID_CLIENT_SECRET'),
    authorize_url='https://sandbox.orcid.org/oauth/authorize',
    authorize_params=None,
    authorize_kwargs=None,
    token_url='https://sandbox.orcid.org/oauth/token',
    client_kwargs={'scope': 'openid'},
)

# Callback route for ORCID OAuth
@app.route('/orcid/callback')
def orcid_callback():
    token = oauth.orcid.authorize_access_token()
    orcid_id = oauth.orcid.get('orcid', token=token)
    
    # Check if the user exists in the database
    db_session = Session()
    user = db_session.query(User).filter_by(orcid=orcid_id).first()

    if user is None:
        # User is not in the database, you can create a new user here
        # For demonstration, we'll just store the ORCID ID
        new_user = User(orcid=orcid_id)
        db_session.add(new_user)
        db_session.commit()

    session['user_id'] = orcid_id  # Store the user ID in the session

    return redirect(url_for('profile'))

# Profile route to display user information
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Query the database for user information (orcid_id in this example)
    db_session = Session()
    user = db_session.query(User).filter_by(orcid=user_id).first()

    return jsonify({'user_id': user.orcid})

# Login route to initiate ORCID OAuth
@app.route('/login')
def login():
    return oauth.orcid.authorize_redirect(redirect_uri=url_for('orcid_callback', _external=True))

# Logout route to clear the session
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))