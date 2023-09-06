"""APIs relative to token handling and operations possible with tokens."""
from flask import jsonify
from ..application import app
from ..models import User


@app.route("/create-token/<token_name>", methods=["GET"])
def create_token(token_name: str):
    """Create a token for the current user with the given name and returns a JSON object with the token's name and value.
    
    Parameters
    ----------
    token_name: str
        Name of the token to create.

    Raises
    ------
    APIException
        If the token name is already taken for the current user.
    NotLoggedIn
        If the user is not logged in.

    Implementative details
    ----------------------
    This endpoint receives a token name as an URL parameter and,
    if the user is logged in, creates a token with the given name
    for the current user. The token itself is create using as salt
    ingredients the curreny time, user ID and token name.
    The token value is then hashed using SHA-256 and the resulting
    hash is used as the token value, which must be unique for the
    entire database, as it is used as the primary key for the
    tokens table.
    The token name is inserted in the database
    using SQLAlchemy, after checking that the token name is not
    already taken for the current user.
    The flask method returns a JSON object with the token name and
    value, which is then sent to the client.
    """
    user = User.from_flask_session()

    # We create a token for the current user with the given name.
    token_value = user.create_token(token_name)

    # We return a JSON object with the token name and value.
    return jsonify({"token_name": token_name, "token_value": token_value})


@app.route("/delete-token/<token_name>", methods=["DELETE"])
def delete_token(token_name: str):
    """Delete a token for the current user with the given name.
    
    Parameters
    ----------
    token_name: str
        Name of the token to delete.

    Raises
    ------
    APIException
        If the token name is not taken for the current user.
    NotLoggedIn
        If the user is not logged in.

    Implementative details
    ----------------------
    This endpoint receives a token name as an URL parameter and,
    if the user is logged in, deletes the token with the given name
    for the current user.
    The token name is deleted from the database using SQLAlchemy.
    """
    user = User.from_flask_session()

    # We delete the token with the given name for the current user.
    user.delete_token(token_name)

    # We return a JSON object with the token name and value.
    return jsonify({"message": "Token deleted successfully."})