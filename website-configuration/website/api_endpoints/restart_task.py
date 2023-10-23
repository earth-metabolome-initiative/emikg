"""API endpoint to restart a task."""
from flask import redirect, jsonify
from ..models import User, Task
from ..application import app


@app.route("/tasks/restart/<int:task_id>", methods=["POST", "GET"])
def restart_task(task_id: int):
    """Restart a task."""
    # First we check that the user is authenticated.
    if not User.is_authenticated():
        return jsonify({"success": False, "error": "User not authenticated."})

    user = User.from_flask_session()

    task = Task.from_id(task_id)

    # Check that the current user is the author of the task
    # or an administrator.
    if not task.is_author(user) and not user.is_administrator():
        return jsonify({"success": False, "error": "User not authorized."})

    # We restart the task.
    task.restart()

    return redirect(task.get_url(), code=302)
