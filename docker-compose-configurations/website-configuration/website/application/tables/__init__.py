"""Submodule for the tables of the application."""
from .orcid_table import ORCIDTable
from .moderators_table import ModeratorsTable
from .administrators_table import AdministratorsTable
from .users_table import UsersTable
from .samples_table import SamplesTable
from .taxons_table import TaxonsTable
from .translations_table import TranslationsTable
from .tokens_table import TokensTable


__all__ = [
    'ORCIDTable',
    'ModeratorsTable',
    'AdministratorsTable',
    'UsersTable',
    'SamplesTable',
    'TaxonsTable',
    'TranslationsTable',
    'TokensTable',
]