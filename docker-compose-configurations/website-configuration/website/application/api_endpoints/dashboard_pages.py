"""API endpoints regardin the dashboard."""
from flask import session, render_template
from ..models import User
from ..application import app

def dashboard_page(
    template_name: str,
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
            f"{template_name}.html",
            current_user=User.from_flask_session(),
            lang=lang
        )
    return render_template(
        "home.html",
        current_user=None,
        lang=lang
    )

@app.route("/taxons")
@app.route("/<lang>/taxons")
def dashboard_taxons(
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
    return dashboard_page("taxons", lang)

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
    return dashboard_page("new_taxon", lang)


@app.route("/samples/new")
@app.route("/<lang>/samples/new")
def dashboard_create_sample(
    lang: str = "en"
):
    """Create a sample.

    Raises
    ------
    APIException
        If the sample with the provided name already exists.
    NotLogged
        If the user is not logged in.

    """
    return dashboard_page("new_sample", lang)
