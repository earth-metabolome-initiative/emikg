"""Abstract class describing a collection of spectra."""
from typing import List, Type
from enpkg_interfaces.record import Record
from enpkg_interfaces.sample import Sample
from enpkg_interfaces.authored import Authored


class SpectraCollection(Record, Authored):
    def get_spectra(self) -> List[Type["Spectrum"]]:
        """Return a list of spectra."""
        raise NotImplementedError(
            "SpectraCollection.get_spectra() not implemented "
            f" for {self.__class__.__name__}"
        )

    def get_sample(self) -> Type[Sample]:
        """Return sample."""
        raise NotImplementedError(
            "SpectraCollection.get_sample() not implemented "
            f" for {self.__class__.__name__}"
        )
