from flask import redirect, jsonify
from emikg_interfaces.from_identifier import IdentifierNotFound
from ..application import app
from ..models import Document, Task


@app.route("/<root>/delete/<int:identifier>")
def delete(root: str, identifier: int):
    """Load the tasks page."""
    try:
        if Document.get_root() == root:
            Document.from_id(identifier).delete()
        elif Task.get_root() == root:
            Task.from_id(identifier).delete()
        else:
            return jsonify({"success": False, "error": "Provided root is not valid."})
    except IdentifierNotFound as e:
        return jsonify({"success": False, "error": f"Identifier {identifier} for {root} not found."})

    return redirect(f"/{root}/", code=302)
