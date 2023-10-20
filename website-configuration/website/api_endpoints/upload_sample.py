"""Endpoint to upload samples."""
from flask import request, jsonify, session
from alchemy_wrapper.models import DataPayload
from ..application import app
from ..models import User

@app.route('/upload-sample/', methods=['POST'])
def upload_sample():
    """Upload a sample."""
    # Get the user.
    user = User.from_flask_session()
    # Get the sample file.
    sample_file = request.files.get('file')
    # We check if the file has a correct mimetype.
    # It can either be gzip or zip.
    if sample_file.mimetype not in ('application/gzip', 'application/zip'):
        return jsonify({'success': False, 'error': 'Invalid mimetype.'})
    # We get the extension of the document.
    extension = sample_file.filename.split('.')[-1]
    # We check if the extension is valid.
    if extension not in ('zip', 'gz'):
        return jsonify({'success': False, 'error': 'Invalid extension.'})
    # Save the sample file.
    # path = f"samples/{user.get_id()}.{extension}"
    # We check if the directory exists and create it if it doesn't.
    # os.makedirs("samples", exist_ok=True)
    # We save the file to the path.
    # sample_file.save(path)

    # We create a data payload.
    data_payload = DataPayload.new_data_payload(user)
    task = data_payload.get_task()
    url = task.get_url()

    lang = session.get('lang', "en")

    url = f"/{lang}/{url}"

    return jsonify({'redirect_url': url})