import json

from structures import Dataset
from loaders import Loader


class JsonLoader(Loader):
    def __init__(self):
        self.parsers = {
            'r2c': self._parse_r2c
        }

    def load(self, ds: Dataset, filepath: str,
             parser: str = 'r2c') -> None:
        """Loads a json file."""

        # load the file
        data = json.load(open(filepath))

        # check if the parsing schema exists
        if parser not in self.parsers:
            raise Exception('Unrecognized json parsing schema.')

        # run the appropriate parser
        try:
            self.parsers[parser](ds, data)
        except Exception:
            raise Exception('Json file does not match expected schema.')

    @staticmethod
    def _parse_r2c(ds: Dataset, data: dict):
        # don't overwrite previously set metadata
        ds.name = ds.name or data['name']
        ds.version = ds.version or data['version']

        # grab any optional metadata
        ds.description = ds.description or data.get('description', None)
        ds.readme = ds.readme or data.get('readme', None)
        ds.author = ds.author or data.get('author', None)
        ds.email = ds.email or data.get('email', None)

        # generate the projects and versions
        for input_ in data['inputs']:
            # some parts of the input are at the project level...
            p_keys = ['repo_url', 'url', 'package_name']
            p_dict = {k: v for k, v in input_.items() if k in p_keys}
            project = ds.find_or_add_project(ds.types['project'], **p_dict)

            # ...while others are at the version level
            v_keys = ['commit_hash', 'version']
            v_dict = {k: v for k, v in input_.items() if k in v_keys}
            if v_dict:
                project.find_or_add_version(ds.types['version'], **v_dict)
