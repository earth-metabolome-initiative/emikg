"""Submodule providing the proxy for the moderators table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the moderators table is the following:

```sql
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    lang VARCHAR(255) NOT NULL,
    translation TEXT NOT NULL,
    last_updated_by INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (label, lang)
);
```

"""
from .database import db

class TranslationsTable(db.Model):
    """Proxy for the translations table in the database, using SQLAlchemy."""

    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(255), nullable=False)
    lang = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.Text, nullable=False)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return f'<Translation #{self.id}>'
    
    @staticmethod
    def get_translation_from_label_and_lang(label: str, lang: str) -> str:
        """Get translation from label and language.

        Parameters
        ----------
        label : str
            label.
        lang : str
            language.

        Returns
        -------
        str
            translation.
        """
        result = TranslationsTable.query.filter_by(label=label, lang=lang).first()
        if result is not None:
            return result.translation
        return None
    
    @staticmethod
    def get_translation_from_label(label: str) -> str:
        """Get translation from label.

        Parameters
        ----------
        label : str
            label.

        Returns
        -------
        str
            translation.
        """
        result = TranslationsTable.query.filter_by(label=label).first()
        if result is not None:
            return result.translation
        return None 
   
    @staticmethod
    def update_translation(label: str, translation: str, lang: str, last_updated_by: int):
        """Update translation.
        
        Parameters
        ----------
        label : str
            label.
        translation : str
            translation.
        lang : str
            language associated with the translation.
        last_updated_by : int
            ID of the user who updated the translation.
        """
        translation = TranslationsTable.query.filter_by(label=label, lang=lang).first()
        translation.translation = translation
        translation.last_updated_by = last_updated_by
        db.session.commit()