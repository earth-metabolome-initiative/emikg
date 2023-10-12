"""SQLAlchemy database proxy relative to the open tree of life table."""
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql import func
from alchemy_wrapper.models.base import Base


class OpenTreeOfLifeEntry(Base):
    """Define the OpenTreeOfLifeEntry model."""

    __tablename__ = "open_tree_of_life"

    id = Column(Integer, primary_key=True)
    ott_id = Column(Integer, nullable=False)
    domain = Column(
        Enum("eukaryota", "bacteria", "archaea", name="domain"), nullable=False
    )
    kingdom = Column(
        Enum(
            "animalia",
            "plantae",
            "fungi",
            "protista",
            "chromista",
            "protozoa",
            name="kingdom",
        ),
        nullable=False,
    )
    phylum = Column(String(80), nullable=False)
    class_ = Column(String(80), nullable=False)
    order = Column(String(80), nullable=False)
    family = Column(String(80), nullable=False)
    tribe = Column(String(80), nullable=False)
    genus = Column(String(80), nullable=False)
    species = Column(String(80), nullable=False)
    # The version of the open tree of life taxonomy, which is
    # referred to as the "taxon source"
    version = Column(String(80), nullable=False)
    # This is the best approximation of the taxon name that
    # open tree of life was able to determine. It could be as
    # general as tje kingdom or as specific as the species.
    resolved_taxon_name = Column(String(80), nullable=False)
    # Whether the taxon name is a synonym or not.
    is_synonym = Column(Boolean, nullable=False)
    is_approximated_match = Column(Boolean, nullable=False)

    taxon_id = Column(
        Integer,
        ForeignKey("taxons.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<OpenTreeOfLifeEntry({self.ott_id!r})>"
