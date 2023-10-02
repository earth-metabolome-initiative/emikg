"""APIs relative to validation."""
from flask import jsonify, request
from ..application import app
from ..models import Taxon



@app.route("/validate/<group_name>", methods=["POST"])
def validate_group(group_name: str):
    """Validate a candidate value for a given group.
    
    Parameters
    ----------
    group_name : str
        The name of the group to validate the candidate value for.
    """

    callbacks = {
        "taxon-name": Taxon.is_valid_taxon_name,
        "taxon-id": Taxon.is_valid_taxon_id,
    }

    if group_name not in callbacks:
        return jsonify({"error": "Invalid group name."}), 400
    
    # We extract the candidate value from the POST request.
    candidate = request.form.get("candidate", None)

    if candidate is None or len(candidate) == 0:
        return jsonify({"error": "No candidate value provided."}), 400
    
    callback = callbacks[group_name]

    # We return a JSON object with the token name and value.
    return jsonify({"valid": callback(candidate)})
