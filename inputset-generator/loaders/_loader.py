from abc import ABC, abstractmethod

from structures import Dataset


class Loader(ABC):
    @abstractmethod
    def load(self, ds: Dataset, handle: str, **kwargs) -> None: pass
