from typing import Dict, List
from flask import jsonify, Response

def get_form_error_output_from_input_name(
    input_name: str,
    error_message: str,
    status_code: int = 400
) -> (Response, int):
    """Returns a Flask response with the error output."""
    return get_form_error_output(
        errors=[{
            "field": input_name,
            "message": error_message
        }],
        status_code=status_code
    )

def get_form_error_output(
    errors: List[Dict[str, str]],
    status_code: int = 400
) -> (Response, int):
    """Returns a Flask response with the error output."""
    return jsonify({
        "success": False,
        "errors": errors
    }), status_code
