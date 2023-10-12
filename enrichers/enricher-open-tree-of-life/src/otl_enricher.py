"""Concrete implementation for the Open Tree of Life taxon Enricher."""
from typing import Dict, List

import numpy as np
import pandas as pd
from alchemy_wrapper import Session
from alchemy_wrapper.models import Taxon
from enrichers import TaxonEnricher
from enrichers.models import EnrichmentTask
from opentree import OT

from .models import OpenTreeOfLifeEntry


class OTLEnricher(TaxonEnricher):
    @classmethod
    def repository(cls) -> str:
        """Name of the repository providing these specific metadata."""
        return "Open Tree of Life"

    @classmethod
    def name(cls) -> str:
        """Name of the enricher."""
        return "Open Tree of Life"

    def _can_enrich(self, enrichable: Taxon) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        if not isinstance(enrichable, Taxon):
            return False

        # A Taxon is enrichable if there is not already an entry in the
        # open_tree_of_life table with the same taxon_id.
        return (
            OpenTreeOfLifeEntry.query.filter_by(taxon_id=enrichable.id).first() is None
        )

    def _get_sleep_time_between_start_attempts(self) -> int:
        """Returns the number of seconds to wait between two start attempts."""
        return 10

    def _task_can_start(self, enrichable: Taxon, task: EnrichmentTask) -> bool:
        """Returns whether the task can start.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # A task can start if there is not already an entry in the
        # open_tree_of_life table with the same taxon_id.
        return self._can_enrich(enrichable)

    def _get_new_elements_to_enrich(self) -> List[Taxon]:
        """Returns a list of new elements to enrich."""
        # Get all the taxons that are not already in the open_tree_of_life table.
        return Taxon.query.filter(
            ~Taxon.id.in_(
                self._session.query(OpenTreeOfLifeEntry.taxon_id).filter(
                    OpenTreeOfLifeEntry.taxon_id.isnot(None)
                )
            )
        ).all()

    def _enrich(self, enrichable: Taxon, task: EnrichmentTask):
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # We retrieve from open tree the ott_id of the taxon.
        otl_taxon_info = otl_taxon_lineage_appender(enrichable.name)
        # We create a new entry in the open_tree_of_life table
        # with the taxon_id of the enrichable class.
        session = Session()
        entry = OpenTreeOfLifeEntry(
            ott_id=otl_taxon_info.get_ott_id(),
            taxon_id=enrichable.id,
            domain=otl_taxon_info.get_otol_domain(),
            kingdom=otl_taxon_info.get_otol_kingdom(),
            phylum=otl_taxon_info.get_otol_phylum(),
            class_=otl_taxon_info.get_otol_class(),
            order=otl_taxon_info.get_otol_order(),
            family=otl_taxon_info.get_otol_family(),
            tribe=otl_taxon_info.get_otol_tribe(),
            genus=otl_taxon_info.get_otol_genus(),
            species=otl_taxon_info.get_otol_species(),
            version=otl_taxon_info.get_taxon_source(),
            resolved_taxon_name=otl_taxon_info.get_matched_name(),
            is_synonym=otl_taxon_info.get_is_synonym(),
            is_approximated_match=otl_taxon_info.get_is_approximate_match(),
        )
        session.add(entry)
        session.commit()


class OTLTaxonInfo:
    def __init__(
        self,
        ott_id: int,
        otol_domain: str,
        otol_kingdom: str,
        otol_phylum: str,
        otol_class: str,
        otol_order: str,
        otol_family: str,
        otol_tribe: str,
        otol_genus: str,
        otol_species: str,
        taxon_source: str,
        taxon_rank: str,
        search_string: str,
        score: float,
        matched_name: str,
        is_synonym: bool,
        is_approximate_match: bool,
    ):
        self.ott_id = ott_id
        self.otol_domain = otol_domain
        self.otol_kingdom = otol_kingdom
        self.otol_phylum = otol_phylum
        self.otol_class = otol_class
        self.otol_order = otol_order
        self.otol_family = otol_family
        self.otol_tribe = otol_tribe
        self.otol_genus = otol_genus
        self.otol_species = otol_species
        self.taxon_source = taxon_source
        self.taxon_rank = taxon_rank
        self.search_string = search_string
        self.score = score
        self.matched_name = matched_name
        self.is_synonym = is_synonym
        self.is_approximate_match = is_approximate_match

    def get_ott_id(self) -> int:
        """
        Returns the OpenTree of Life ID of the sample.
        """
        return self.ott_id

    def get_otol_domain(self) -> str:
        """
        Returns the OpenTree of Life domain of the sample.
        """
        return self.otol_domain

    def get_otol_kingdom(self) -> str:
        """
        Returns the OpenTree of Life kingdom of the sample.
        """
        return self.otol_kingdom

    def get_otol_phylum(self) -> str:
        """
        Returns the OpenTree of Life phylum of the sample.
        """
        return self.otol_phylum

    def get_otol_class(self) -> str:
        """
        Returns the OpenTree of Life class of the sample.
        """
        return self.otol_class

    def get_otol_order(self) -> str:
        """
        Returns the OpenTree of Life order of the sample.
        """
        return self.otol_order

    def get_otol_family(self) -> str:
        """
        Returns the OpenTree of Life family of the sample.
        """
        return self.otol_family

    def get_otol_tribe(self) -> str:
        """
        Returns the OpenTree of Life tribe of the sample.
        """
        return self.otol_tribe

    def get_otol_genus(self) -> str:
        """
        Returns the OpenTree of Life genus of the sample.
        """
        return self.otol_genus

    def get_otol_species(self) -> str:
        """
        Returns the OpenTree of Life species of the sample.
        """
        return self.otol_species

    def get_taxon_source(self) -> str:
        """
        Returns the taxon source of the sample.
        """
        return self.taxon_source

    def get_taxon_rank(self) -> str:
        """
        Returns the taxon rank of the sample.
        """
        return self.taxon_rank

    def get_search_string(self) -> str:
        """
        Returns the search string of the sample.
        """
        return self.search_string

    def get_score(self) -> float:
        """
        Returns the score of the sample.
        """
        return self.score

    def get_matched_name(self) -> str:
        """
        Returns the matched name of the sample.
        """
        return self.matched_name

    def get_is_synonym(self) -> bool:
        """
        Returns whether the sample is a synonym.
        """
        return self.is_synonym

    def get_is_approximate_match(self) -> bool:
        """
        Returns whether the sample is an approximate match.
        """
        return self.is_approximate_match


def tnrs_lookup(taxon_name: str) -> Dict:
    """Fetches the taxonomic information for a given taxon name using the OpenTree Taxonomic Name Resolution Service.

    Parameters
    ----------
    taxon_name : str
        The taxon to be resolved.

    Returns
    -------
    taxon_tnrs_matched.response_dict : dict
        The response of the OT call.
    """

    # Taxonomic Name Resolution Service lookup
    taxon_tnrs_matched = OT.tnrs_match(
        names=[taxon_name],
        context_name=None,
        do_approximate_matching=True,
        include_suppressed=False,
    )

    # The response of the OT call is returned
    return taxon_tnrs_matched.response_dict


def otl_taxon_lineage_appender(taxon_name: str) -> OTLTaxonInfo:
    """Fetches the taxonomic information for a given taxon name using the OpenTree Taxonomic Name Resolution Service."""
    jsondic = tnrs_lookup(taxon_name)

    df_species_tnrs_matched = pd.json_normalize(
        jsondic, record_path=["results", "matches"]
    )

    # We then want to match with the accepted name instead of the synonym in case both are present.
    # We thus order by matched_name and then by is_synonym status prior to returning the first row.

    df_species_tnrs_matched.sort_values(
        ["search_string", "is_synonym"], axis=0, inplace=True
    )
    merged_df = df_species_tnrs_matched.drop_duplicates("search_string", keep="first")
    # converting 'ott_ids' from float to int (check the astype('Int64') whic will work while the astype('int') won't see https://stackoverflow.com/a/54194908)
    merged_df["taxon.ott_id"] = merged_df["taxon.ott_id"].astype("Int64")

    # However, we then need to put them back to
    ott_list = list(merged_df["taxon.ott_id"].dropna().astype("int"))

    ott_resolved = [
        OT.taxon_info(ott, include_lineage=True).response_dict for ott in ott_list
    ]

    df_tax_lineage = pd.json_normalize(
        ott_resolved,
        record_path=["lineage"],
        meta=["ott_id", "unique_name"],
        record_prefix="sub_",
        errors="ignore",
    )

    # This keeps the last occurence of each ott_id / sub_rank grouping https://stackoverflow.com/a/41886945
    df_tax_lineage_filtered = df_tax_lineage.groupby(
        ["ott_id", "sub_rank"], as_index=False
    ).last()

    # Here we pivot long to wide to get the taxonomy
    df_tax_lineage_filtered_flat = df_tax_lineage_filtered.pivot(
        index="ott_id", columns="sub_rank", values="sub_name"
    )

    # Here we actually also want the lowertaxon (species usually) name
    df_tax_lineage_filtered_flat = pd.merge(
        df_tax_lineage_filtered_flat,
        df_tax_lineage_filtered[["ott_id", "unique_name"]],
        how="left",
        on="ott_id",
    )

    # Despite the left join ott_id are duplicated
    df_tax_lineage_filtered_flat.drop_duplicates(
        subset=["ott_id", "unique_name"], inplace=True
    )

    # here we want to have these columns whatever happens
    col_list = [
        "ott_id",
        "domain",
        "kingdom",
        "phylum",
        "class",
        "order",
        "family",
        "tribe",
        "genus",
        "unique_name",
    ]

    df_tax_lineage_filtered_flat = df_tax_lineage_filtered_flat.reindex(
        columns=col_list, fill_value=np.NaN
    )

    # We now rename our columns of interest
    renaming_dict = {
        "domain": "query_otol_domain",
        "kingdom": "query_otol_kingdom",
        "phylum": "query_otol_phylum",
        "class": "query_otol_class",
        "order": "query_otol_order",
        "family": "query_otol_family",
        "tribe": "query_otol_tribe",
        "genus": "query_otol_genus",
        "unique_name": "query_otol_species",
    }

    df_tax_lineage_filtered_flat.rename(columns=renaming_dict, inplace=True)

    # We select columns of interest
    cols_to_keep = [
        "ott_id",
        "query_otol_domain",
        "query_otol_kingdom",
        "query_otol_phylum",
        "query_otol_class",
        "query_otol_order",
        "query_otol_family",
        "query_otol_tribe",
        "query_otol_genus",
        "query_otol_species",
    ]

    df_tax_lineage_filtered_flat = df_tax_lineage_filtered_flat[cols_to_keep]

    # We merge this back with the samplemetadata only if we have an ott.id in the merged df
    samples_metadata = pd.merge(
        merged_df[pd.notnull(merged_df["taxon.ott_id"])],
        df_tax_lineage_filtered_flat,
        how="left",
        left_on="taxon.ott_id",
        right_on="ott_id",
    )

    # We now populate the OTLTaxonInfo object

    taxon_lineage = OTLTaxonInfo(
        ott_id=samples_metadata["taxon.ott_id"],
        otol_domain=samples_metadata["query_otol_domain"],
        otol_kingdom=samples_metadata["query_otol_kingdom"],
        otol_phylum=samples_metadata["query_otol_phylum"],
        otol_class=samples_metadata["query_otol_class"],
        otol_order=samples_metadata["query_otol_order"],
        otol_family=samples_metadata["query_otol_family"],
        otol_tribe=samples_metadata["query_otol_tribe"],
        otol_genus=samples_metadata["query_otol_genus"],
        otol_species=samples_metadata["query_otol_species"],
        taxon_source=samples_metadata["taxon.source"],
        taxon_rank=samples_metadata["taxon.rank"],
        search_string=samples_metadata["search_string"],
        score=samples_metadata["score"],
        matched_name=samples_metadata["matched_name"],
        is_synonym=samples_metadata["is_synonym"],
        is_approximate_match=samples_metadata["is_approximate_match"],
    )

    return taxon_lineage
