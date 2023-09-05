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

# API endpoint to promote a user to administrator (requires admin permission)
@app.route('/promote-admin/<int:user_id>', methods=['POST'])
def promote_admin(user_id: int):
    """Promote the user at the given user ID to administrator."""
    User(user_id).promote_admin()
    return jsonify({"message": "User promoted to administrator successfully"})

# API endpoint to demote a user from administrator (requires admin permission)
@app.route('/demote-admin/<int:user_id>', methods=['POST'])
def demote_admin(user_id: int):
    """Demote the user at the given user ID from administrator."""
    User(user_id).demote_admin()
    return jsonify({"message": "User demoted from administrator successfully"})

# API endpoint to promote a user to moderator (requires admin permission)
@app.route('/promote-moderator/<int:user_id>', methods=['POST'])
def promote_moderator(user_id: int):
    """Promote the user at the given user ID to moderator."""
    User(user_id).promote_moderator()
    return jsonify({"message": "User promoted to moderator successfully"})

# API endpoint to demote a user from moderator (requires admin permission)
@app.route('/demote-moderator/<int:user_id>', methods=['POST'])
def demote_moderator(user_id: int):
    """Demote the user at the given user ID from moderator."""
    User(user_id).demote_moderator()
    return jsonify({"message": "User demoted from moderator successfully"})
