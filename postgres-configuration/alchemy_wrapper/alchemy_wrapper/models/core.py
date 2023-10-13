"""SQLAlchemy model for the user and sample tables."""

from typing import List, Optional, Type
from alchemy_wrapper.database import Session
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float

from emikg_interfaces import User as UserInterface
from emikg_interfaces import Sample as SampleInterface
from emikg_interfaces import Taxon as TaxonInterface
from emikg_interfaces import Spectrum as SpectrumInterface
from emikg_interfaces import SpectraCollection as SpectraCollectionInterface
from emikg_interfaces.from_identifier import IdentifierNotFound

from alchemy_wrapper.models.administrator import Administrator
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.models.moderator import Moderator
from alchemy_wrapper.models.social import Social
from alchemy_wrapper.models.social_profiles import SocialProfile



class User(Base, UserInterface):
    """Define the User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    @staticmethod
    def from_id(identifier: int) -> "User":
        """Return the user corresponding to the given identifier.

        Parameters
        ----------
        identifier : int
            The identifier of the user to return.

        Raises
        ------
        UserNotFound
            If the user corresponding to the given identifier is not found.
        """
        # We query the user table to get the user corresponding to the given identifier
        user = User.query.filter_by(id=identifier).first()
        if user is None:
            raise IdentifierNotFound(f"User with id {identifier} not found")
        return user

    def get_id(self) -> int:
        """Return the identifier of the user."""
        return self.id

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    def is_moderator(self):
        """Check if user is a moderator.

        Implementation details
        ----------------------
        This method checks if the user is a moderator by checking if the user
        id appears in the moderators table.
        """
        # We query the moderators table to check if the user is a moderator
        return Moderator.query.filter_by(user_id=self.id).first() is not None

    def is_administrator(self):
        """Check if user is an administrator.

        Implementation details
        ----------------------
        This method checks if the user is an administrator by checking if the user
        id appears in the administrators table.
        """
        # We query the administrators table to check if the user is an administrator
        return Administrator.query.filter_by(user_id=self.id).first() is not None

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_samples(self, number_of_records: int) -> List["Sample"]:
        """Return list of samples created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        # We return the most recent samples created by the user
        return (
            Sample.query.filter_by(user_id=self.id)
            .order_by(Sample.updated_at.desc())
            .limit(number_of_records)
            .all()
        )
    
    def get_social_profiles(self) -> List[SocialProfile]:
        """Return list of socials."""
        return Session().query(SocialProfile).filter(SocialProfile.user_id == self.id).all()
    
class Sample(Base, SampleInterface):

    __tablename__ = "samples"

    id = Column(Integer, primary_key=True)
    taxon_id = Column(
        Integer, ForeignKey("taxons.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    # The derived from column is a foreign key to the sample table
    # It is used to link a sample to the sample it was derived from
    # For example, if a sample is a subsample of another sample, the derived from column
    # will be set to the id of the sample it was derived from
    # If the sample is not derived from another sample, the derived from column will be
    # set to None
    # The ondelete="SET NULL" means that if the sample it was derived from is deleted,
    # the derived from column will be set to None
    # The nullable=True means that the derived from column can be set to None
    # If the derived from column is set to None, it means that the sample is not derived
    # from another sample
    derived_from = Column(
        Integer, ForeignKey("samples.id", ondelete="SET NULL"), nullable=True
    )

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def get_parent_sample(self) -> Optional["Sample"]:
        """Return parent sample."""
        if self.derived_from is None:
            return None
        return Sample.from_id(self.derived_from)

    def get_child_samples(self) -> List["Sample"]:
        """Return list of child samples."""
        return Sample.query.filter_by(derived_from=self.id).all()

    @staticmethod
    def from_id(identifier: int) -> "Sample":
        """Return Sample instance from Sample id."""
        # We query the user table to get the user corresponding to the given identifier
        sample = Sample.query.filter_by(id=identifier).first()
        if sample is None:
            raise IdentifierNotFound(f"Sample with id {identifier} not found")
        return sample

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def get_author(self) -> User:
        """Return the author of the sample."""
        return User.from_id(self.author_id)

    def delete(self):
        """Delete the sample."""
        # We delete the sample from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return f"{self.first_name} {self.second_name}"

class Taxon(Base, TaxonInterface):
    """Define the Taxon model."""

    __tablename__ = "taxons"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Taxon({self.name!r})>"

    @staticmethod
    def from_id(identifier: int) -> "Taxon":
        """Return taxon instance from taxon id."""
        # We query the user table to get the user corresponding to the given identifier
        taxon = Taxon.query.filter_by(id=identifier).first()
        if taxon is None:
            raise IdentifierNotFound(f"Taxon with id {identifier} not found")
        return taxon

    def get_id(self) -> int:
        """Return taxon id."""
        return self.id

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_samples(self) -> List[Sample]:
        """Return list of samples."""
        return Sample.query.filter_by(taxon_id=self.id).all()

    def get_author(self) -> User:
        """Return author."""
        return User.query.filter_by(id=self.author_id).first()
    
    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description
    
    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name
    

class Spectrum(Base, SpectrumInterface):
    """SQLAlchemy model for the spectrographic data."""

    __tablename__ = "spectra"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    spectra_collection_id = Column(
        Integer, ForeignKey("spectra_collection.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    @staticmethod
    def from_id(identifier: int) -> "Spectrum":
        """Return Spectrum instance from Spectrum id."""
        # We query the user table to get the user corresponding to the given identifier
        spectrum = Spectrum.query.filter_by(id=identifier).first()
        if spectrum is None:
            raise IdentifierNotFound(f"Spectrum with id {identifier} not found")
        return spectrum

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def get_spectra_collection(self) -> "SpectraCollection":
        """Return the spectra collection of the spectrum."""
        return SpectraCollection.from_id(self.spectra_collection_id)

    def get_author(self) -> User:
        """Return the author of the spectrum."""
        return self.get_spectra_collection().get_author()

    def delete(self):
        """Delete the spectrum."""
        # We delete the spectrum from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name
    
class SpectraCollection(Base, SpectraCollectionInterface):
    """SQLAlchemy model for spectra_collection table."""

    __tablename__ = "spectra_collection"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    sample_id = Column(
        Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    def get_spectra(self) -> List[Type[Spectrum]]:
        """Return a list of spectra."""
        raise NotImplementedError(
            "SpectraCollection.get_spectra() not implemented "
            f" for {self.__class__.__name__}"
        )

    def get_sample(self) -> Sample:
        """Return sample."""
        return Sample.from_id(self.sample_id)

    @staticmethod
    def from_id(identifier: int) -> "SpectraCollection":
        """Return SpectraCollection instance from SpectraCollection id."""
        # We query the user table to get the user corresponding to the given identifier
        spectra_collection = SpectraCollection.query.filter_by(id=identifier).first()
        if spectra_collection is None:
            raise IdentifierNotFound(
                f"SpectraCollection with id {identifier} not found"
            )
        return spectra_collection

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def delete(self):
        """Delete the spectra collection."""
        # We delete the spectra collection from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_author(self) -> User:
        """Return the author of the spectrum."""
        return User.from_id(self.author_id)

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name