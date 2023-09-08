"""Submodule providing the proxy for the tokens table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the tokens table is the following:

```sql
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    token_name VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    used_last_on TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, token_name),
    UNIQUE (token)
);
```

"""
from .database import db
from time import time
from dict_hash import sha256

class TokensTable(db.Model):
    """Proxy for the tokens table in the database, using SQLAlchemy."""

    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token_name = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    used_last_on = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return f'<Token #{self.id}>'
    
    @staticmethod
    def is_valid_token_id(token_id: int) -> bool:
        """Check if token ID exists.

        Parameters
        ----------
        token_id : int
            token ID.

        Returns
        -------
        bool
            True if token ID exists, False otherwise.
        """
        return TokensTable.query.filter_by(id=token_id).count() > 0
    
    @staticmethod
    def is_valid_token_name(token_name: str) -> bool:
        """Check if token name exists.

        Parameters
        ----------
        token_name : str
            token name.

        Returns
        -------
        bool
            True if token name exists, False otherwise.
        """
        return TokensTable.query.filter_by(token_name=token_name).count() > 0
    
    @staticmethod
    def is_valid_token(token: str) -> bool:
        """Check if token exists.

        Parameters
        ----------
        token : str
            token.

        Returns
        -------
        bool
            True if token exists, False otherwise.
        """
        return TokensTable.query.filter_by(token=token).count() > 0
    
    @staticmethod
    def is_valid_user_id(user_id: int) -> bool:
        """Check if user ID exists.

        Parameters
        ----------
        user_id : int
            user ID.

        Returns
        -------
        bool
            True if user ID exists, False otherwise.
        """
        return TokensTable.query.filter_by(user_id=user_id).count() > 0
    
    @staticmethod
    def get_user_id_from_token(token: str) -> int:
        """Return user ID from token.

        Parameters
        ----------
        token : str
            token.

        Returns
        -------
        int
            user ID.
        """
        return TokensTable.query.filter_by(token=token).first().user_id
    
    @staticmethod
    def get_token_name_from_token(token: str) -> str:
        """Return token name from token.

        Parameters
        ----------
        token : str
            token.

        Returns
        -------
        str
            token name.
        """
        return TokensTable.query.filter_by(token=token).first().token_name
    
    @staticmethod
    def get_token_id_from_token(token: str) -> int:
        """Return token ID from token.

        Parameters
        ----------
        token : str
            token.

        Returns
        -------
        int
            token ID.
        """
        return TokensTable.query.filter_by(token=token).first().id
    
    @staticmethod
    def get_token_from_token_name(token_name: str) -> str:
        """Return token from token name.

        Parameters
        ----------
        token_name : str
            token name.

        Returns
        -------
        str
            token.
        """
        return TokensTable.query.filter_by(token_name=token_name).first().token
    
    @staticmethod
    def create_token(user_id: int, token_name: str) -> str:
        """Create a token.

        Parameters
        ----------
        user_id : int
            user ID.
        token_name : str
            token name.
        """
        # We insert the token name in the database.
        # This insertion is done using SQLAlchemy, and as the token is
        # required to be unique, we expect the insertion to fail if the
        # token name is already taken. This should be extremely rare, as
        # the token is created using as salt ingredients the current time,
        # the user ID and the token name. Still, we check for this case.
        # When such a case happens, we recreate the token and try again.
        while True:
             # We create a token for the current user with the given name.
            token = sha256({
                "time": time(),
                "user_id": user_id,
                "token_name": token_name
            })

            try:
                # We insert the token in the database.

                with db.session.begin_nested():
                    token = TokensTable(
                        user_id=user_id,
                        token_name=token_name,
                        token=token,
                    )
                    db.session.add(token)
                    db.session.flush()
                    db.session.commit()
                
                break
            except Exception as exception:
                if "UNIQUE constraint failed" in str(exception):
                    continue
                raise exception
        
        return token
    
    @staticmethod
    def delete_token_from_token_name_and_user_id(token_name: str, user_id: int) -> None:
        """Delete a token.

        Parameters
        ----------
        token_name : str
            token name.
        user_id : int
            user ID.
        """
        # We delete the token from the database.
        with db.session.begin_nested():
            token = TokensTable.query.filter_by(token_name=token_name, user_id=user_id).first()
            db.session.delete(token)
            db.session.commit()

    @staticmethod
    def delete_token_from_token(token: str) -> None:
        """Delete a token.

        Parameters
        ----------
        token : str
            token.
        """
        # We delete the token from the database.
        with db.session.begin_nested():
            token = TokensTable.query.filter_by(token=token).first()
            db.session.delete(token)
            db.session.commit()

    @staticmethod
    def has_token_from_token_name_and_user_id(token_name: str, user_id: int) -> bool:
        """Check if a token exists.

        Parameters
        ----------
        token_name : str
            token name.
        user_id : int
            user ID.

        Returns
        -------
        bool
            True if token exists, False otherwise.
        """
        return TokensTable.query.filter_by(token_name=token_name, user_id=user_id).count() > 0