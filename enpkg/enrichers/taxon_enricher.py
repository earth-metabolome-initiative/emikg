"""Module to enrich the metadata of Taxon objects"""

from .enricher import AbstractEnricher
from ..taxons import Taxon


class AbstractTaxonEnricher(AbstractEnricher):
    """Abstract class to enrich the metadata of Taxon objects"""
