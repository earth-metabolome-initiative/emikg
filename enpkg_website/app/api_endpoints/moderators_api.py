"""Submodule providing the API endpoints relative to moderation actions.

Such actions include but are not limited to:
- Editing a textual label on the website so as to extend the website's internationalization support.
"""
from flask import jsonify, request
from ..app import app
from ..models import Translation

@app.route("/update-label/<lang>/<label>", methods=["POST"])
def update_translation(lang: str, label: str):
    """Update or insert a translation in the database.
    
    Implementative details
    ----------------------
    This endpoint expects to receive a JSON object in the request body
    with a single key "translation" whose value is the translation to
    update or insert. The translation is sanitized before being inserted
    into the database so as to avoid SQL injection.
    """
    if not request.is_json:
        return jsonify({"message": "Request body must be a JSON object"}), 400
    
    json_request = request.get_json()

    if "translation" not in json_request:
        return jsonify({"message": "Request body must contain a 'translation' key"}), 400
    
    translation = json_request["translation"]

    Translation.update_translation(label, translation, lang)
    return jsonify({"message": "Translation updated successfully"})