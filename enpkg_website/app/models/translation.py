"""Class providing methods to update textual entries in the database."""

from ..app import db
from .user import User

class Translation:
    """Class providing methods to update textual entries in the database."""

    @staticmethod
    def retrieve_from_label_and_language(label: str, lang: str = "en") -> "Translation":
        """Retrieve a translation from its label and language.

        Parameters
        ----------
        label: str
            Label of the translation to retrieve.
        lang: str = "en"
            Language of the translation to retrieve.

        Implementative details
        ----------------------
        If the translation is not found in the requested language, then
        the translation is searched in the default language (English).
        If the translation is not found in the default language either,
        then the translation is searched in any language. If the
        translation is still not found, then an exception is raised.
        """
        return db.engine.execute(
            """
            SELECT label, translation, lang
            FROM translations
            WHERE label = :label AND lang = :lang
            LIMIT 1
            UNION
            SELECT label, translation, lang
            FROM translations
            WHERE label = :label AND lang = 'en'
            LIMIT 1
            UNION
            SELECT label, translation, lang
            FROM translations
            WHERE label = :label
            LIMIT 1
            """,
            label=label,
            lang=lang.lower()
        ).first()

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
        
        lang = lang.lower()

        if len(lang) != 2:
            raise ValueError("Language must be a two-letter code")

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