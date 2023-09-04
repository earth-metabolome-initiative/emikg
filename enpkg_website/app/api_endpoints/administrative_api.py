"""Subset of the APIs that require admin privileges."""
from flask import jsonify
from ..app import app
from ..models import User

# API endpoint to delete a user (requires admin permission)
@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    """Delete the user at the given user ID."""
    User(user_id).delete()
    return jsonify({"message": "User deleted successfully"})