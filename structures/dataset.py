from pathlib import Path
from typing import List

from .project import Project
from registries import registries, sources
from file_types import file_types
from util import get_user_name, get_user_email


class Dataset:
    def __init__(self, registry: str = None):
        # link to the appropriate registry
        self.registry = registries.get(registry, None)

        # if the user specified a registry, ensure it's valid
        if registry and registry not in registries:
            raise Exception('Invalid registry. Valid types are: %s'
                            % list(registries))

        self.name = ''
        self.version = ''
        self.description = ''
        self.readme = ''
        self.author = get_user_name()
        self.email = get_user_email()
        self.projects: List[Project] = []

    def load_file(self, path: str):
        # check if the path is valid
        if not Path(path).is_file():
            raise Exception('Invalid path; file does not exist.')

        # check if the filetype is valid
        extension = Path(path).suffix
        if extension not in file_types:
            raise Exception("Invalid input file type '%s'. Valid types"
                            "are: %s." % (extension, list(file_types)))

        # load initial data from the file
        file = file_types[extension]
        self.projects = file.read(path)

    def load_weblist(self, name: str):
        # check if the registry has been set
        if not self.registry:
            raise Exception('Registry has not been set. Valid types '
                            'are: %s' % list(registries))

        # check if the name is valid
        reg_name = self.registry.name
        if name not in sources[reg_name]:
            list_names = list(self.registry.weblists)
            raise Exception('Invalid weblist for registry %s. Valid '
                            'names are: %s' % (reg_name, list_names))

        # load initial data from the weblist
        self.projects = self.registry.load_weblist(name)
