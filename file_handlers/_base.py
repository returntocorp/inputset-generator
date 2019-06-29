from abc import ABC, abstractmethod

from structures import Dataset


class FileHandler(ABC):
    def __init__(self):
        self.parsers: dict = {}

    @abstractmethod
    def load(self, ds: Dataset, path: str) -> None: pass
