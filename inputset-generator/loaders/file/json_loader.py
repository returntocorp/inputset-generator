import json

from structures import Dataset, Project, Version
from structures.projects import class_map as p_class_map
from structures.versions import class_map as v_class_map
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

        # remove any existing projects
        ds.projects = []

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
            # split out project- vs. version-level information
            p_data, v_data = {}, {}
            p_keys = ['repo_url', 'url', 'package_name']
            v_keys = ['commit_hash', 'version']
            for k, val in input_.items():
                # add the attribute to the project or version
                if k in v_keys:
                    v_data[k] = val
                elif k in p_keys:
                    p_data[k] = val

            # get or create the new project
            project = ds.find_project(**p_data)
            if not project:
                p_class = p_class_map.get(ds.registry, Project)
                project = p_class(**p_data)
                ds.projects.append(project)

            # add any versions to the project
            if v_data:
                v_class = v_class_map.get(ds.registry, Version)
                project.versions.append(v_class(**v_data))
