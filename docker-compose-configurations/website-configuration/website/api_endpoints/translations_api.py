"""API endpoints regardin the dashboard."""
from ..application import app
from ..models import Translation


@app.route("/<lang>/translation/<label>")
def get_translation(lang: str, label: str):
    """Create a sample.

    Parameters
    ----------
    lang : str
        Language of the translation.
    label : str
        Label of the translation.
    """
    return Translation.retrieve_from_label_and_language(label=label, lang=lang)
