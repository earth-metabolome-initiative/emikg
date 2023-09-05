"""Class providing methods to update textual entries in the database."""

from flask import session
from ..app import db, app
from .user import User

class Translation:
    """Class providing methods to update textual entries in the database."""

    @staticmethod
    def retrieve_from_label(label: str) -> "Translation":
        """Retrieve a translation from its label and language.

        Parameters
        ----------
        label: str
            Label of the translation to retrieve.

        Implementative details
        ----------------------
        If the translation is not found in the requested language, then
        the translation is searched in the default language (English).
        If the translation is not found in the default language either,
        then the translation is searched in any language. If the
        translation is still not found, then we return the textual
        label itself as the translation, plus the message in all caps
        that the translation is missing. A moderator can then add the
        missing translation by clicking on the message.
        """
        # We determine whether the session language was set.
        # If not, we set it to the default language, i.e. English.
        lang = session.get("lang", "en")

        # We first try to retrieve the translation in the requested
        # language. If not found, we try the default language.
        # If not found, we try any language.
        # If not found, we return the label itself as the translation
        # and a message in all caps that the translation is missing.

        translation = db.engine.execute(
            """
            SELECT translation
            FROM translations
            WHERE label = :label AND lang = :lang
            """,
            label=label,
            lang=lang
        ).scalar()

        # If the translation is not found in the requested language,
        # we try the default language, if the default language is not
        # the requested language.
        if translation is None and lang != "en":
            translation = db.engine.execute(
                """
                SELECT translation
                FROM translations
                WHERE label = :label AND lang = :lang
                """,
                label=label,
                lang="en"
            ).scalar()

        # If the translation is not found in the requested language
        # or in the default language, we try any language.
        if translation is None:
            translation = db.engine.execute(
                """
                SELECT translation
                FROM translations
                WHERE label = :label
                """,
                label=label
            ).scalar()

        # If the translation is still not found, we return the label
        # itself as the translation and a message in all caps that
        # the translation is missing.
        if translation is None:
            translation = f"{label} (TRANSLATION MISSING)"

        return translation

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

app.jinja_env.globals.update(translation=Translation.retrieve_from_label)
