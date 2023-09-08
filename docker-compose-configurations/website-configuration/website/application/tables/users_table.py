"""Submodule providing the proxy for the users table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the users table is the following:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY
    -- Add other user-related fields as needed
);
```

"""

from .database import db
from .orcid_table import ORCIDTable

class UsersTable(db.Model):
    """Proxy for the users table in the database, using SQLAlchemy."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<User #{self.id}>'
    
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
        return UsersTable.query.filter_by(id=user_id).count() > 0
    
    @staticmethod
    def create_user_from_orcid(orcid: str) -> int:
        """Create a new user from an ORCID.

        Parameters
        ----------
        orcid : str
            ORCID.

        Returns
        -------
        int
            User ID.
        """
        
        # We open a transaction, and insert a new user in the users table.
        # We also insert the ORCID in the orcid table alongside the user ID.

        with db.session.begin_nested():
            # We insert a new user in the users table.
            user = UsersTable()
            db.session.add(user)
            db.session.flush()
            user_id = user.id

            # We also insert the ORCID in the orcid table alongside the user ID.
            orcid = ORCIDTable(user_id=user_id, orcid=orcid)
            db.session.add(orcid)
            db.session.flush()

            db.session.commit()

        return user_id
    
    @staticmethod
    def delete_user(user_id: int) -> None:
        """Delete a user.

        Parameters
        ----------
        user_id : int
            User ID.
        """
        # We delete the user from the database.
        with db.session.begin_nested():
            user = UsersTable.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()