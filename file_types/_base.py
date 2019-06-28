from abc import ABC, abstractmethod

from structures import Dataset


class FileType(ABC):
    @staticmethod
    @abstractmethod
    def read(path: str) -> Dataset: pass
