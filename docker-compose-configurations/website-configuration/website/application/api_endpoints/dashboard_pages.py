"""API endpoints regardin the dashboard."""
from flask import session, render_template, abort
from ..models import User, Taxon, Sample, Specter
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

@app.route("/settings")
@app.route("/<lang>/settings")
def dashboard_settings(
    lang: str = "en"
):
    """Load the settings page."""
    return dashboard_page("settings", lang)

@app.route("/taxons")
@app.route("/<lang>/taxons")
def dashboard_taxons(
    lang: str = "en"
):
    """Load the taxons page."""
    return dashboard_page("taxons", lang)

@app.route("/samples")
@app.route("/<lang>/samples")
def dashboard_samples(
    lang: str = "en"
):
    """Load the samples page."""
    return dashboard_page("samples", lang)

@app.route("/specters")
@app.route("/<lang>/specters")
def dashboard_specters(
    lang: str = "en"
):
    """Load the specters page."""
    return dashboard_page("specters", lang)

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

@app.route("/specters/new")
@app.route("/<lang>/specters/new")
def dashboard_create_specter(
    lang: str = "en"
):
    """Create a specter.

    Raises
    ------
    APIException
        If the specter with the provided name already exists.
    NotLogged
        If the user is not logged in.

    """
    return dashboard_page("new_specter", lang)

@app.route("/taxons/<int:taxon_id>")
@app.route("/<lang>/taxons/<int:taxon_id>")
def taxon_page(
    lang: str = "en",
    taxon_id: int = None
):
    """Return the taxon page."""
    if not Taxon.is_valid_taxon_id(taxon_id):
        abort(404)
    return render_template(
        "taxon.html",
        taxon=Taxon(taxon_id),
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )

@app.route("/taxons/search")
@app.route("/<lang>/taxons/search")
def search_taxon_page(
    lang: str = "en",
):
    """Return the taxon page."""
    return render_template(
        "search_taxon.html",
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )

@app.route("/samples/<int:sample_id>")
@app.route("/<lang>/samples/<int:sample_id>")
def sample_page(
    lang: str = "en",
    sample_id: int = None
):
    """Return the sample page."""
    if not Sample.is_valid_sample_id(sample_id):
        abort(404)
    return render_template(
        "sample.html",
        sample=Sample(sample_id),
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )

@app.route("/samples/search")
@app.route("/<lang>/samples/search")
def search_sample_page(
    lang: str = "en",
):
    """Return the sample page."""
    return render_template(
        "search_sample.html",
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )

@app.route("/specters/<int:specter_id>")
@app.route("/<lang>/specters/<int:specter_id>")
def specter_page(
    lang: str = "en",
    specter_id: int = None
):
    """Return the specter page."""
    if not Specter.is_valid_specter_id(specter_id):
        abort(404)
    return render_template(
        "specter.html",
        specter=Specter(specter_id),
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )

@app.route("/specters/search")
@app.route("/<lang>/specters/search")
def search_specter_page(
    lang: str = "en",
):
    """Return the specter page."""
    return render_template(
        "search_specter.html",
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )

@app.route("/users/search")
@app.route("/<lang>/users/search")
def search_user_page(
    lang: str = "en",
):
    """Return the sample page."""
    return render_template(
        "search_user.html",
        current_user=User.from_flask_session() if User.is_authenticated() else None,
        lang=lang
    )