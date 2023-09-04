"""Class providing methods to update textual entries in the database."""

from ..app import db
from .user import User

class Translation:
    """Class providing methods to update textual entries in the database."""

    @staticmethod
    def update_translation(label: str, translation: str, lang: str):
        """Update or insert a translation in the database.

        Parameters
        ----------
        label: str
            Label of the translation to update or insert.
        translation: str
            The translation to update or insert.
        lang: str
            lang of the translation to update or insert.

        Raises
        ------
        Unauthorized
            If the current user is not a moderator.
        ValueError
            If the label or translation are empty strings.

        Implementative details
        ----------------------
        The combination of label and lang forms the unique label
        of the translation in the database. If the combination of
        label and lang already exists in the database, then the
        translation is updated, otherwise it is inserted. Upon
        insertion or update, also the column last_updated_by is
        updated to reflect the current user.

        The label and translation are sanitized before being
        inserted into the database so as to avoid SQL injection.
        """
        User.must_be_moderator()

        if not label or not translation:
            raise ValueError("Label and translation must be non-empty strings")

        db.engine.execute(
            """
            INSERT INTO translations (label, translation, lang, last_updated_by)
            VALUES (:label, :translation, :lang, :user_id)
            ON CONFLICT (label, lang) DO UPDATE SET
                translation = :translation,
                last_updated_by = :user_id
            """,
            label=label,
            translation=translation,
            lang=lang,
            user_id=User.session_user_id()
        )