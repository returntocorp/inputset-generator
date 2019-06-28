from abc import ABC, abstractmethod

from structures import Dataset


class FileHandler(ABC):
    @staticmethod
    @abstractmethod
    def load(dataset: Dataset, path: str) -> None: pass
