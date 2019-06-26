from abc import ABC, abstractmethod
from typing import List, Dict


class Registry(ABC):
    name: str = ''
    url_format: str = ''
    weblists: Dict[str, Dict] = {}

    def __init__(self):
        self.projects: List['Project'] = []

    def head(self, n):
        # trim all but the first n projects
        self.projects = self.projects[:n]

    @abstractmethod
    def load_weblist(self, name: str): pass

    @abstractmethod
    def load_file(self, path: str): pass

    @abstractmethod
    def sort(self, args: List[str]): pass


class Project(ABC):
    def __init__(self, name: str = '', url: str = ''):
        if not (name or url):
            # gotta have at least one!
            raise Exception('Missing project name or url.')

        self.name = name
        self.url = url

        self.versions: List[Dict] = []
