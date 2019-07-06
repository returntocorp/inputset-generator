import json

from structures import Dataset, Project
from structures.projects import class_map
from loaders import Loader


class JsonLoader(Loader):
    def __init__(self):
        self.parsers = {
            'r2c': self._parse_r2c
        }

    def load(self, ds: Dataset, filepath: str, parser: str = 'r2c') -> None:
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
            data = {'_versions': {}}

            # sort out project- vs. version-level information
            p_keys = ['repo_url', 'url', 'package_name']
            v_keys = ['commit_hash', 'version']
            for k, val in input_.items():
                if k in p_keys:
                    data[k] = val
                if k in v_keys:
                    data['_versions'][k] = val

            # figure out which type of project to create
            # (default is the vanilla Project)
            project_cls = class_map.get(ds.registry, Project)

            # create the new project & add versions to it
            project = project_cls(**data)

            # add the project (& versions) to the dataset
            ds.projects.append(project)
