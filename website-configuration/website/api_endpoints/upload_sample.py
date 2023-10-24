"""Endpoint to upload samples."""
from flask import request, jsonify, session
from alchemy_wrapper.models import DataPayload
from ..application import app, db
from ..models import User
import zipfile
import tarfile


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
    
    # TODO! CHECK THE INTERNAL STRUCTURE OF THE GZIP.

    # Here we check, without extracting the payload, whether
    # the compressed directory contains two directories, namely
    # "msdata" and "metadata".

    if sample_file.mimetype == "application/zip":
        with zipfile.ZipFile(sample_file) as zip_file:
            if "msdata/" not in zip_file.namelist():
                return jsonify({"success": False, "error": "Invalid zip payload, no msdata directory.", "directories": zip_file.namelist()})
            if "metadata/" not in zip_file.namelist():
                return jsonify({"success": False, "error": "Invalid zip payload, no metadata directory."})
            if "msdata/processed/" not in zip_file.namelist():
                return jsonify({"success": False, "error": "Invalid zip payload, no msdata/processed directory."})
    elif sample_file.mimetype == "application/gzip":
        with tarfile.open(sample_file) as tar_file:
            if "msdata/" not in tar_file.getnames():
                return jsonify({"success": False, "error": "Invalid gzip payload, no msdata directory."})
            if "metadata/" not in tar_file.getnames():
                return jsonify({"success": False, "error": "Invalid gzip payload, no metadata directory."})
            if "msdata/processed/" not in tar_file.getnames():
                return jsonify({"success": False, "error": "Invalid gzip payload, no msdata/processed directory."})

    # We create a data payload.
    data_payload = DataPayload.new_data_payload(
        user,
        extension=extension,
        session=db.session
    )
    task = data_payload.get_task(session=db.session)
    url = task.get_url()

    # We save the file to the unsafe subdirectory.
    sample_file.save(data_payload.get_unsafe_path())

    lang = session.get("lang", "en")

    url = f"/{lang}/{url}"

    return jsonify({"redirect_url": url})
