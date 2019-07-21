from abc import ABC, abstractmethod

from structures import Dataset


class Loader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, handle: str, **kwargs) -> Dataset: pass
