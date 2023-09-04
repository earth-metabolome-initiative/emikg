from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/google-login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/google-authorized')
@google.authorized_handler
def google_authorized(resp):
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    # You can access user_info data and use it to log in the user
    # Example: user_email = user_info.data['email']
    return 'Logged in as: ' + user_info.data['email']

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

oauth = OAuth(app)

orcid = oauth.register(
    name='orcid',
    client_id='YOUR_ORCID_CLIENT_ID',
    client_secret='YOUR_ORCID_CLIENT_SECRET',
    authorize_url='https://orcid.org/oauth/authorize',
    authorize_params=None,
    access_token_url='https://orcid.org/oauth/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='YOUR_REDIRECT_URI',
    client_kwargs={
        'scope': 'openid',
    }
)

@app.route('/orcid-login')
def orcid_login():
    return orcid.authorize_redirect(redirect_uri=url_for('orcid_authorized', _external=True))

@app.route('/orcid-authorized')
def orcid_authorized():
    token = orcid.authorize_access_token()
    user_info = orcid.parse_id_token(token)
    # You can access user_info data and use it to log in the user
    user_id = user_info['sub']
    return 'Logged in as: ' + user_id