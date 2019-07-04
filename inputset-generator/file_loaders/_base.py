from abc import ABC, abstractmethod

from structures import Dataset


class FileLoader(ABC):
    @abstractmethod
    def load(self, ds: Dataset, path: str, fileargs: str = None) -> None: pass
