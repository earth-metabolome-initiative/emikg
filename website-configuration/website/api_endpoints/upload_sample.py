"""Endpoint to upload samples."""
from flask import request, jsonify, session
from alchemy_wrapper.models import DataPayload
from ..application import app, db
from ..models import User


@app.route("/upload-sample/", methods=["POST"])
def upload_sample():
    """Upload a sample."""
    # Get the user.
    user = User.from_flask_session()
    # Get the sample file.
    sample_file = request.files.get("file")
    # We check if the file has a correct mimetype.
    # It can either be gzip or zip.
    if sample_file.mimetype not in ("application/gzip", "application/zip"):
        return jsonify({"success": False, "error": "Invalid mimetype."})
    # We get the extension of the document.
    extension = sample_file.filename.split(".")[-1]
    # We check if the extension is valid.
    if extension not in ("zip", "gz"):
        return jsonify({"success": False, "error": "Invalid extension."})
    # Save the sample file.
    # path = f"samples/{user.get_id()}.{extension}"
    # We check if the directory exists and create it if it doesn't.

    # We create a data payload.
    data_payload = DataPayload.new_data_payload(
        user,
        extension=extension,
        session=db.session
    )
    task = data_payload.get_task(session=db.session)
    url = task.get_url()

    # We save the file to the unsafe subdirectory.
    sample_file.save(data_payload.get_path())

    lang = session.get("lang", "en")

    url = f"/{lang}/{url}"

    return jsonify({"redirect_url": url})
