"""Endpoint to upload samples."""
import zipfile
from flask import request, jsonify, session
from werkzeug.datastructures import FileStorage
from alchemy_wrapper.models import DataPayload
from ..application import app, db
from ..models import User
from .form_error_output import get_form_error_output_from_input_name

@app.route("/upload-sample/", methods=["POST"])
def upload_sample():
    """Upload a sample."""
    # Get the user.
    user = User.from_flask_session()
    # Get the sample file.
    sample_file: FileStorage = request.files.get("file")
    # We check if the file has a correct mimetype.
    # It can either be gzip or zip.
    if sample_file.mimetype not in ("application/zip", ):
        return get_form_error_output_from_input_name(
            input_name="file",
            error_message="Invalid mimetype, expected application/zip.",
            status_code=415
        )
    # We get the extension of the document.
    extension = sample_file.filename.split(".")[-1]
    # We check if the extension is valid.
    if extension not in ("zip", ):
        return get_form_error_output_from_input_name(
            input_name="file",
            error_message="Invalid extension, expected zip.",
            status_code=415
        )
    
    # Run test to see if the zip file is valid.
    with zipfile.ZipFile(sample_file) as zip_file:

        if zip_file.testzip() is not None:
            return get_form_error_output_from_input_name(
                input_name="file",
                error_message="Invalid zip payload, zip file is corrupted.",
                status_code=415
            )

        if "msdata/" not in zip_file.namelist():
            return get_form_error_output_from_input_name(
                input_name="file",
                error_message="Invalid zip payload, no msdata directory.",
                status_code=415
            )
        if "metadata/" not in zip_file.namelist():
            return get_form_error_output_from_input_name(
                input_name="file",
                error_message="Invalid zip payload, no metadata directory.",
                status_code=415
            )
        if "msdata/processed/" not in zip_file.namelist():
            return get_form_error_output_from_input_name(
                input_name="file",
                error_message="Invalid zip payload, no processed directory.",
                status_code=415
            )
        
        metadata_file_ends = [
            "metadata.tsv",
            "lcms_params.txt",
            "mzmine_params.xml"
        ]

        for metadata_file_end in metadata_file_ends:
            # We now check that there is a file that matches the pattern
            # "metadata/*metadata.tsv".
            metadata_files = [
                f for f in zip_file.namelist()
                if f.startswith("metadata/") and f.endswith(metadata_file_end) and f.count("/") == 1
            ]
            if len(metadata_files) != 1:
                return get_form_error_output_from_input_name(
                    input_name="file",
                    error_message=f"Invalid zip payload, no file with pattern metadata/{metadata_file_end}.",
                    status_code=415
                )

        # Under the processed directory, we check that there is are
        # *.mgf, *_sirius.mgf, and *_quant.csv.
        for extension in (".mgf", "sirius.mgf", "quant.csv"):
            processed_files = [
                f for f in zip_file.namelist()
                if f.startswith("msdata/processed/") and f.count("/") == 2 and f.endswith(extension)
            ]

            if len(processed_files) == 0:
                return get_form_error_output_from_input_name(
                    input_name="file",
                    error_message=f"Invalid zip payload, no file with pattern msdata/processed/*{extension}.",
                    status_code=415
                )

    # We create a data payload.
    data_payload = DataPayload.new_data_payload(
        user,
        extension="zip",
        session=db.session
    )
    task = data_payload.get_task(session=db.session)
    url = task.get_url()

    # We save the file to the unsafe subdirectory.
    sample_file.stream.seek(0)
    sample_file.save(data_payload.get_unsafe_path())

    lang = session.get("lang", "en")

    url = f"/{lang}/{url}"

    return jsonify({"redirect_url": url})
