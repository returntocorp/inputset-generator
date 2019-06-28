from abc import ABC, abstractmethod
from typing import Any, List, Dict
import requests
import json

from structures import Project


class Registry(ABC):
    def __init__(self):
        # child classes must define name and url_format
        self.name: str
        self.url_format: str

        # default Registry has no weblists, a simple csv parser, and a
        # json parser for all known input types
        self.weblists: Dict[str, Dict[str, Any]] = {}

    def load_weblist(self, name: str) -> List[Project]:
        """Loads and parses a weblist."""
        weblist = self.weblists[name]

        # try to load json from the url
        r = requests.get(weblist['url'])
        try:
            data = r.json()
        except json.decoder.JSONDecodeError:
            raise Exception('Weblist url did not return a json file.')

        # parse the data (calls the registered parser)
        weblist['parser'](data)

    def head(self, n) -> None:
        # trim all but the first n projects
        self.projects = self.projects[:n]

    def sample(self, n) -> None:
        pass

    def sort(self, args: List[str]) -> None:
        #getattr(self, str, default)
        pass

    @abstractmethod
    def get_meta(self, project: Project) -> None: pass

    @abstractmethod
    def get_versions(self, project: Project) -> None: pass
