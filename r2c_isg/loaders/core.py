from abc import ABC, abstractmethod

from r2c_isg.dataset import Dataset


class Loader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, handle: str, **kwargs) -> Dataset: pass
