from pathlib import Path
from typing import List

from .project import Project


class Dataset:
    def __init__(self, registry: str = None):
        from registries import registries
        from util import get_user_name, get_user_email

        # link to the appropriate registry
        self.registry = registries.get(registry, None)

        # if the user specified a registry, ensure it's valid
        if registry and registry not in registries:
            raise Exception('Invalid registry. Valid types are: %s'
                            % list(registries))

        self.name = None
        self.version = None
        self.description = None
        self.readme = None
        self.author = get_user_name()
        self.email = get_user_email()
        self.projects: List[Project] = []

    def load_file(self, path: str):
        from file_types import file_types

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
        file.load(self, path)

    def load_weblist(self, name: str):
        from registries import registries, sources

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
        self.registry.load_weblist(self, name)

    def save(self, name: str = None):
        from file_types import JsonFileType

        # check that all necessary meta values have been set
        if not (self.name and self.version):
            # name and version are mandatory
            raise Exception('Dataset name and/or version are missing.')

        # file name is dataset name, if not provided by user
        name = name or self.name + '.json'

        # save to disk
        JsonFileType.save(self, name)
