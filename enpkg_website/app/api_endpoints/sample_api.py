"""API endpoints to manipulate samples."""

from flask import jsonify, request
from ..models import Sample
from ..app import app
from ..exceptions import APIException

@app.route("/delete-sample/<int:sample_id>", methods=["DELETE"])
def delete_sample(sample_id: int):
    """Delete sample with the provided ID.

    Parameters
    ----------
    sample_id : int
        Sample ID.

    Raises
    ------
    APIException
        If the sample ID does not exist.
    NotLogged
        If the user is not logged in.
    Unauthorized
        If the user is not the sample author.
        If the user is not a moderator.

    """
    Sample(sample_id).delete()
    return jsonify({
        "message": "Sample deleted successfully."
    })

@app.route("/create-sample/", methods=["POST"])
def create_sample():
    """Create a sample.

    Raises
    ------
    APIException
        If the taxon ID does not exist.
        If the parent sample ID does not exist.
        If the sample name already exists.
    NotLogged
        If the user is not logged in.

    """
    if "taxon_id" not in request.form:
        raise APIException(
            "The 'taxon_id' field is missing in the request.",
            400
        )
    if "sample_name" not in request.form:
        raise APIException(
            "The 'sample_name' field is missing in the request.",
            400
        )
    taxon_id = int(request.form.get("taxon_id"))
    sample_name = request.form.get("sample_name")
    parent_sample_id = request.form.get("parent_sample_id", None)
    sample_id = Sample.create(
        taxon_id,
        sample_name,
        parent_sample_id
    )
    return jsonify({
        "sample_id": sample_id,
        "message": "Sample created successfully."
    })