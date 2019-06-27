from abc import ABC, abstractmethod
from typing import Any, List, Dict, Callable
import requests, json, csv
from pathlib import Path


class Registry(ABC):
    def __init__(self):
        # child classes must define name and url_format
        self.name: str
        self.url_format: str

        # A Registry contains Projects
        self.projects: List['Project'] = []

        # default Registry has no weblists, a simple csv parser, and a
        # json parser for all known input types
        self.weblists: Dict[str, Dict[str, Any]] = {}
        self.fileparsers: Dict[str, Callable] = {
            '.json': self._parse_json,
            '.csv': self._parse_csv
        }

    def load_weblist(self, name: str) -> None:
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

    def load_file(self, path: str) -> None:
        """Loads and parses a file from disk."""
        filetype = Path(path).suffix
        if filetype in self.fileparsers:
            # call the registered file parser
            self.fileparsers[filetype](path)
        else:
            raise Exception('Unrecognized input file type. Acceptable '
                            'types: %s.' % list(self.fileparsers))

    def _parse_json(self, path: str) -> None:
        """Default json parser."""
        data = json.load(open(path))

        try:
            # obtain mandatory json file info
            self.input_type = data['inputs'][0]['input_type']
            self.meta_name = data['name']
            self.meta_version = data['version']
        except Exception:
            raise Exception('JSON file must provide name, version, and '
                            'input_type.')

        # obtain optional json file info
        self.meta_author = data.get('author', None)
        self.meta_email = data.get('email', None)
        self.meta_description = data.get('description', None)
        self.meta_readme = data.get('readme', None)

        # parse the json file's inputs list
        for input in data['inputs']:

        pass

    def _parse_csv(self, path: str) -> None:
        """Default csv parser."""
        # data = csv.???
        pass

    def head(self, n) -> None:
        # trim all but the first n projects
        self.projects = self.projects[:n]

    def sample(self, n) -> None:
        pass

    def sort(self, args: List[str]) -> None:
        #getattr(self, str, default)
        pass

    @abstractmethod
    def get_meta(self) -> None: pass

    @abstractmethod
    def get_versions(self) -> None: pass


class Project(ABC):
    def __init__(self, name: str = '', url: str = ''):
        # must have a name or url
        if not (name or url):
            raise Exception('Project must have a name or url.')

        self.name = name
        self.url = url

        # a Project contains Versions
        self.versions: List['Version'] = []


class Version(ABC):
    def __init__(self, version_string: str = '', commit_hash: str = ''):
        # must have a version string or commit hash
        if not (version_string or commit_hash):
            raise Exception('Version must have a version string '
                            'or commit hash.')

        self.version_string = version_string
        self.commit_hash = commit_hash
