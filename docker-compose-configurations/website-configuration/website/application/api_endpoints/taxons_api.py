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
    if "taxon_name" not in request.form:
        raise APIException("The 'taxon_name' field is missing in the request.", 400)
    taxon_id = Taxon.create(request.form.get("taxon_name"))
    return jsonify({"taxon_id": taxon_id, "message": "Taxon created successfully."})


@app.route("/autocomplete-taxons/", methods=["POST"])
def autocomplete_taxon():
    """Autocomplete a taxon."""
    candidate_taxon_name = request.args.get("candidate_taxon_name")
    return jsonify(matching_results=TaxonsTable.find_taxons_like(candidate_taxon_name))
