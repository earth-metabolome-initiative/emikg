"""Abstract class describing a collection of spectra."""
from typing import List, Type
from enpkg_interfaces import Spectrum, Record, Sample


class SpectraCollection(Record):
    def get_spectra(self) -> List[Type[Spectrum]]:
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
