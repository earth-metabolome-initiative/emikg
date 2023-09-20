"""API endpoints to manipulate taxons."""
from flask import jsonify, request
from ..models import Taxon
from ..application import app
from ..tables import TaxonsTable
from ..exceptions import APIException


@app.route("/delete-taxon/<int:taxon_id>", methods=["DELETE"])
def delete_taxon(taxon_id: int):
    """Delete taxon with the provided ID.

    Parameters
    ----------
    taxon_id : int
        Taxon ID.

    Raises
    ------
    APIException
        If the taxon ID does not exist.
    NotLogged
        If the user is not logged in.
    Unauthorized
        If the user is not the taxon author.
        If the user is not a moderator.

    """
    Taxon(taxon_id).delete()
    return jsonify({"message": "Taxon deleted successfully."})


@app.route("/create-taxon/", methods=["POST"])
def create_taxon():
    """Create a taxon.

    Raises
    ------
    APIException
        If the taxon with the provided name already exists.
    NotLogged
        If the user is not logged in.

    """
    if "taxon-name" not in request.form:
        raise APIException("The 'taxon-name' field is missing in the request.", 400)
    if "taxon-description" not in request.form:
        raise APIException(
            "The 'taxon-description' field is missing in the request.", 400
        )
    taxon = Taxon.create(
        taxon_name=request.form.get("taxon-name"),
        description=request.form.get("taxon-description"),
    )
    return jsonify(
        {
            "redirect_url": taxon.get_taxon_url(),
            "message": "Taxon created successfully.",
        }
    )


@app.route("/autocomplete-taxons/", methods=["POST"])
def autocomplete_taxon():
    """Autocomplete a taxon."""
    # We get the JSON data from the request.
    search = request.form["search"]

    return jsonify(
        matching_results=[
            {
                "name": taxon.get_taxon_name(),
                "url": taxon.get_taxon_url(),
                "id": taxon.get_taxon_id(),
            }
            for taxon in Taxon.find_taxons_like(search)
        ]
    )
