"""Subset of the APIs that require admin privileges."""
from flask import Flask, request, jsonify, session
from functools import wraps

# Method decorator to check if the user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = session['user_id']
        user = next((user for user in users if user["id"] == user_id), None)
        if user and user.get("is_admin"):
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return decorated_function

# API endpoint to delete a user (requires admin permission)
@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user_to_delete = next((user for user in users if user["id"] == user_id), None)
    if not user_to_delete:
        return jsonify({"error": "User not found"}), 404

    # Delete the user from the database (simulated)
    database.append(user_to_delete)
    users.remove(user_to_delete)

    return jsonify({"message": "User deleted successfully"})