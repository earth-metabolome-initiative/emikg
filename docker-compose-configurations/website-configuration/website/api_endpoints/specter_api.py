"""API endpoints to manipulate specters."""

from flask import jsonify, request
from ..models import Specter
from ..application import app
from ..exceptions import APIException

@app.route("/delete-specter/<int:specter_id>", methods=["DELETE"])
def delete_specter(specter_id: int):
    """Delete specter with the provided ID.

    Parameters
    ----------
    specter_id : int
        Specter ID.

    Raises
    ------
    APIException
        If the specter ID does not exist.
    NotLogged
        If the user is not logged in.
    Unauthorized
        If the user is not the specter author.
        If the user is not a moderator.

    """
    Specter(specter_id).delete()
    return jsonify({
        "message": "Specter deleted successfully."
    })

@app.route("/create-specter/", methods=["POST"])
def create_specter():
    """Create a specter.

    Raises
    ------
    APIException
        If the taxon ID does not exist.
        If the parent specter ID does not exist.
        If the specter name already exists.
    NotLogged
        If the user is not logged in.

    """
    if "taxon_id" not in request.form:
        raise APIException(
            "The 'taxon_id' field is missing in the request.",
            400
        )
    if "specter_name" not in request.form:
        raise APIException(
            "The 'specter_name' field is missing in the request.",
            400
        )
    taxon_id = int(request.form.get("taxon_id"))
    specter_name = request.form.get("specter_name")
    parent_specter_id = request.form.get("parent_specter_id", None)
    specter_id = Specter.create(
        taxon_id,
        specter_name,
        parent_specter_id
    )
    return jsonify({
        "specter_id": specter_id,
        "message": "Specter created successfully."
    })