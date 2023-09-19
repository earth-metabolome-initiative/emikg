"""API endpoints regardin the dashboard."""
from flask import session, render_template
from ..models import User
from ..application import app

@app.route("/taxons/new")
@app.route("/<lang>/taxons/new")
def dashboard_create_taxon(
    lang: str = "en"
):
    """Create a taxon.

    Raises
    ------
    APIException
        If the taxon with the provided name already exists.
    NotLogged
        If the user is not logged in.

    """
    session['lang'] = lang
    if User.is_authenticated():
        return render_template(
            'new_taxon.html',
            current_user=User.from_flask_session(),
            lang=lang
        )
    return render_template(
        "home.html",
        current_user=None,
        lang=lang
    )
