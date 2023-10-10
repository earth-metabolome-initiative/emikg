"""API endpoints regardin the dashboard."""
from typing import Optional, Type
from flask import render_template, abort
from enpkg_interfaces import Record, IdentifierNotFound
from alchemy_wrapper.models import Taxon, Sample, Spectrum, SpectraCollection
from ..models import User
from ..application import app


def kg_page(
    lang: str,
    record_class: Type[Record],
    identifier: Optional[int] = None,
):
    """Return the page."""
    current_user = (User.from_flask_session() if User.is_authenticated() else None,)
    if identifier is None:
        return render_template(
            f"{record_class.get_root()}.html",
            record=None,
            current_user=current_user,
            lang=lang,
        )
    try:
        record = record_class.from_id(identifier)
    except IdentifierNotFound:
        abort(404)

    return render_template(
        f"{record_class.get_root()}.html",
        record=record,
        current_user=current_user,
        lang=lang,
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


@app.route("/samples")
@app.route("/<lang>/samples")
@app.route("/samples/<int:identifier>")
@app.route("/<lang>/samples/<int:identifier>")
def samples_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the samples page."""
    return kg_page(
        lang=lang,
        record_class=Sample,
        identifier=identifier,
    )


@app.route("/spectra_collections")
@app.route("/<lang>/spectra_collections")
@app.route("/spectra_collections/<int:identifier>")
@app.route("/<lang>/spectra_collections/<int:identifier>")
def spectra_collections_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the spectra_collections page."""
    return kg_page(
        lang=lang,
        record_class=SpectraCollection,
        identifier=identifier,
    )


@app.route("/users")
@app.route("/<lang>/users")
@app.route("/users/<int:identifier>")
@app.route("/<lang>/users/<int:identifier>")
def users_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the users page."""
    return kg_page(
        lang=lang,
        record_class=User,
        identifier=identifier,
    )


@app.route("/spectra")
@app.route("/<lang>/spectra")
@app.route("/spectra/<int:identifier>")
@app.route("/<lang>/spectra/<int:identifier>")
def spectra_page(lang: str = "en", identifier: Optional[int] = None):
    """Load the spectra page."""
    return kg_page(
        lang=lang,
        record_class=Spectrum,
        identifier=identifier,
    )
