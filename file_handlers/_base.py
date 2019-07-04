from abc import ABC, abstractmethod

from structures.dataset import Dataset


class FileHandler(ABC):
    @abstractmethod
    def load(self, ds: Dataset, path: str, fileargs: str = None) -> None: pass
