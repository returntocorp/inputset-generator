from abc import ABC, abstractmethod

from structures import Dataset


class FileHandler(ABC):
    @abstractmethod
    def load(self, ds: Dataset, path: str, fileargs: str) -> None: pass
