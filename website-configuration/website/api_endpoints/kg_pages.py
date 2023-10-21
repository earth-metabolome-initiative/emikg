"""API endpoints regardin the dashboard."""
from typing import Optional, Type
from flask import abort, session, render_template, redirect
from emikg_interfaces import IdentifierNotFound
from ..models import User, RecordPage, Taxon, Task
from ..application import app
from ..exceptions import NotLoggedIn

def kg_page(
    lang: str,
    record_class: Type[RecordPage],
    identifier: Optional[int] = None,
):
    """Return the page."""
    session['lang'] = lang
    if identifier is None:
        record = record_class.get_default()
    try:
        record = record_class.from_id(identifier)
    except IdentifierNotFound:
        abort(404)

    if User.is_authenticated():
        user = User.from_flask_session()
    else:
        user = None

    return render_template(
        "record.html",
        record=record,
        lang=lang,
        user=user,
    )


@app.route("/upload")
@app.route("/upload/")
@app.route("/<lang>/upload")
@app.route("/<lang>/upload/")
def upload_page(lang: str = "en"):
    """Load the taxons page."""
    if not User.is_authenticated():
        return redirect(f"/{lang}/", code=302)

    user = User.from_flask_session()

    return render_template(
        "upload.html",
        lang=lang,
        user=user,
    )

@app.route("/taxons")
@app.route("/<lang>/taxons")
@app.route("/taxons/<int:identifier>")
@app.route("/<lang>/taxons/<int:identifier>")
def taxons_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the taxons page."""
    return kg_page(
        lang=lang,
        record_class=Taxon,
        identifier=identifier,
    )

@app.route("/tasks")
@app.route("/<lang>/tasks")
@app.route("/tasks/<int:identifier>")
@app.route("/<lang>/tasks/<int:identifier>")
def tasks_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the tasks page."""
    return kg_page(
        lang=lang,
        record_class=Task,
        identifier=identifier,
    )


# @app.route("/samples")
# @app.route("/<lang>/samples")
# @app.route("/samples/<int:identifier>")
# @app.route("/<lang>/samples/<int:identifier>")
# def samples_page(lang: str = "en", identifier: Optional[int] = None):
#     """Load the samples page."""
#     return kg_page(
#         lang=lang,
#         record_class=Sample,
#         identifier=identifier,
#     )


# @app.route("/spectra_collections")
# @app.route("/<lang>/spectra_collections")
# @app.route("/spectra_collections/<int:identifier>")
# @app.route("/<lang>/spectra_collections/<int:identifier>")
# def spectra_collections_page(lang: str = "en", identifier: Optional[int] = None):
#     """Load the spectra_collections page."""
#     return kg_page(
#         lang=lang,
#         record_class=SpectraCollection,
#         identifier=identifier,
#     )


@app.route("/users")
@app.route("/users/")
@app.route("/<lang>/users")
@app.route("/<lang>/users/")
@app.route("/users/<int:identifier>")
@app.route("/users/<int:identifier>/")
@app.route("/<lang>/users/<int:identifier>")
@app.route("/<lang>/users/<int:identifier>/")
def users_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the users page."""
    return kg_page(
        lang=lang,
        record_class=User,
        identifier=identifier,
    )


# @app.route("/spectra")
# @app.route("/<lang>/spectra")
# @app.route("/spectra/<int:identifier>")
# @app.route("/<lang>/spectra/<int:identifier>")
# def spectra_page(lang: str = "en", identifier: Optional[int] = None):
#     """Load the spectra page."""
#     return kg_page(
#         lang=lang,
#         record_class=Spectrum,
#         identifier=identifier,
#     )

@app.route("/")
@app.route("/<lang>")
@app.route("/<lang>/")
def home_page(lang: str = "en"):
    """Load the taxons page."""
    return render_template(
        "home.html",
        lang=lang,
    )