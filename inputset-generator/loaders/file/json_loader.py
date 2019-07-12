import json

from structures import Dataset, DefaultProject, DefaultVersion
from structures.projects import project_map
from structures.versions import version_map
from loaders import Loader


class JsonLoader(Loader):
    def __init__(self):
        # Note: No Json parsers are provided by default.
        self.parsers = {}

    def load(self, ds: Dataset, filepath: str, parser: str = None) -> None:
        """Loads a json file."""

        # ensure the user specified which parser to use
        if not parser:
            raise Exception('Missing json parser. Valid options are: %s'
                            % list(self.parsers))

        # load the file
        data = json.load(open(filepath))

        # check if the parsing schema exists
        if parser not in self.parsers:
            raise Exception('Unrecognized json parsing schema.')

        # remove any existing projects
        ds.projects = []

        # run the appropriate parser
        self.parsers[parser](ds, data)
