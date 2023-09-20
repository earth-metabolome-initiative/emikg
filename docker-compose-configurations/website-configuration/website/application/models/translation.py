"""Class providing methods to update textual entries in the database."""

from flask import session
from ..application import app
from .user import User
from ..tables import TranslationsTable

class Translation:
    """Class providing methods to update textual entries in the database."""

    @staticmethod
    def get_current_language() -> str:
        """Return the current language."""
        return session.get("lang", "en")

    @staticmethod
    def retrieve_from_label_and_language(label: str, lang: str) -> "Translation":
        """Retrieve a translation from its label and language.

        Parameters
        ----------
        label: str
            Label of the translation to retrieve.
        lang: str
            Language of the translation to retrieve.
        """
        # We first try to retrieve the translation in the requested
        # language. If not found, we try the default language.
        # If not found, we try any language.
        # If not found, we return the label itself as the translation
        # and a message in all caps that the translation is missing.

        translation = TranslationsTable.get_translation_from_label_and_lang(
            label=label,
            lang=lang
        )

        # If the translation is not found in the requested language,
        # we try the default language, if the default language is not
        # the requested language.
        if translation is None and lang != "en":
            translation = TranslationsTable.get_translation_from_label_and_lang(
                label=label,
                lang="en"
            )

        # If the translation is not found in the requested language
        # or in the default language, we try any language.
        if translation is None:
            translation = TranslationsTable.get_translation_from_label(
                label=label
            )

        # If the translation is still not found, we return the label
        # itself as the translation and a message in all caps that
        # the translation is missing.
        if translation is None:
            translation = f"{label} (TRANSLATION MISSING)"

        return translation

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
        return Translation.retrieve_from_label_and_language(
            label=label,
            lang=Translation.get_current_language()
        )


    @staticmethod
    def retrieve_from_label_with_markup(label: str) -> "Translation":
        """Retrieve a translation from its label and language, with markup."""
        translation = Translation.retrieve_from_label(label)

        if User.is_authenticated() and User.from_flask_session().is_moderator():
            lang = Translation.get_current_language()

            return f"<span data-label='{label}' data-lang='{lang}' class='translatable'>{translation}</span>"
        
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

        TranslationsTable.update_translation(
            label=label,
            translation=translation,
            lang=lang,
            last_updated_by=User.get_current_user_id()
        )

app.jinja_env.globals.update(
    translation=Translation.retrieve_from_label_with_markup
)

app.jinja_env.globals.update(
    current_language=Translation.get_current_language
)
