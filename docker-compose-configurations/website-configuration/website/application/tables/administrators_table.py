"""Submodule providing the proxy for the administrators table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the administrators table is the following:

```sql
CREATE TABLE administrators (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    -- Add other administrator-related fields as needed
    -- The user_id must be unique
    UNIQUE (user_id)
);
```

"""

from .database import db

class AdministratorsTable(db.Model):
    """Proxy for the administrators table in the database, using SQLAlchemy."""

    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    def __repr__(self):
        return f'<administrator #{self.id}>'
    
    @staticmethod
    def is_valid_administrator_id(administrator_id: int) -> bool:
        """Check if administrator ID exists.

        Parameters
        ----------
        administrator_id : int
            administrator ID.

        Returns
        -------
        bool
            True if administrator ID exists, False otherwise.
        """
        return AdministratorsTable.query.filter_by(id=administrator_id).count() > 0
    
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
        return AdministratorsTable.query.filter_by(user_id=user_id).count() > 0
    
    @staticmethod
    def create_administrator_from_user_id(user_id: int) -> int:
        """Create a new administrator from a user ID.

        Parameters
        ----------
        user_id : int
            user ID.

        Returns
        -------
        int
            administrator ID.
        """
        
        # We open a transaction, and insert a new administrator in the administrators table.
        # We also insert the user ID in the users table alongside the administrator ID.
        # We return the administrator ID.
        administrator = AdministratorsTable(user_id=user_id)
        db.session.add(administrator)
        db.session.commit()
        return administrator.id
    
    @staticmethod
    def delete_administrator(administrator_id: int) -> None:
        """Delete an administrator.

        Parameters
        ----------
        administrator_id : int
            administrator ID.
        """
        
        # We open a transaction, and delete the administrator from the administrators table.
        # We also delete the user ID from the users table.
        # We commit the transaction.
        administrator = AdministratorsTable.query.filter_by(id=administrator_id).first()
        db.session.delete(administrator)
        db.session.commit()

    @staticmethod
    def delete_administrator_from_user_id(user_id: int) -> None:
        """Delete an administrator.

        Parameters
        ----------
        user_id : int
            user ID.
        """
        
        # We open a transaction, and delete the administrator from the administrators table.
        # We also delete the user ID from the users table.
        # We commit the transaction.
        administrator = AdministratorsTable.query.filter_by(user_id=user_id).first()
        db.session.delete(administrator)
        db.session.commit()