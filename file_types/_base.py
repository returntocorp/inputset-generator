from abc import ABC, abstractmethod
from typing import List

from structures import Project


class FileType(ABC):
    @staticmethod
    @abstractmethod
    def read(path: str) -> List[Project]: pass
