from pathlib import Path
from typing import List

from .project import Project


class Dataset:
    def __init__(self, registry: str = None):
        from util import get_user_name, get_user_email

        self.registry = None
        self.name = None
        self.version = None
        self.description = None
        self.readme = None
        self.author = get_user_name()
        self.email = get_user_email()
        self.projects: List[Project] = []

        # set the registry, if the user provided it
        if registry:
            self.set_registry(registry)

    def set_registry(self, registry: str) -> None:
        """Loads up the specified registry."""
        from registries import registries

        # check if the registry name is valid
        if registry not in registries:
            raise Exception('Invalid registry. Valid types are: %s'
                            % list(registries))

        # link to the appropriate registry
        self.registry = registries[registry]

    def load_file(self, path: str):
        """Uses a file handler to load a dataset from file."""
        from file_handlers import file_handlers

        # check if the path is valid
        if not Path(path).is_file():
            raise Exception('Invalid path; file does not exist.')

        # check if the filetype is valid
        extension = Path(path).suffix
        if extension not in file_handlers:
            raise Exception("Invalid input file type '%s'. Valid types"
                            "are: %s." % (extension, list(file_handlers)))

        # load initial data from the file
        file = file_handlers[extension]
        file.load(self, path)

    def load_weblist(self, name: str):
        """Uses the dataset's registry to """
        from registries import registries

        # check if the registry has been set
        if not self.registry:
            raise Exception('Registry has not been set. Valid types '
                            'are: %s' % list(registries))

        # check if the name is valid
        list_names = list(self.registry.weblists)
        if name not in list_names:
            reg_name = self.registry.name
            raise Exception('Invalid weblist for registry %s. Valid '
                            'names are: %s' % (reg_name, list_names))

        # load initial data from the weblist
        self.registry.load_weblist(self, name)

    def save(self, name: str = None):
        from file_handlers import JsonFileHandler

        # check that all necessary meta values have been set
        if not (self.name and self.version):
            # name and version are mandatory
            raise Exception('Dataset name and/or version are missing.')

        # file name is dataset name, if not provided by user
        name = name or self.name + '.json'

        # save to disk
        JsonFileHandler.save(self, name)

    def get_project(self, **kwargs):
        """Gets a project matching all parameters or returns None."""

        # linear search function; potential for being slow...
        for p in self.projects:
            match = True
            for param, val in kwargs.items():
                if getattr(p, param, None) != val:
                    match = False
                    break
            if match:
                return p

        return None

    def _get_or_add_project(self, **kwargs):
        """Finds a matching project or adds a new one."""
        project = self.get_project(**kwargs)
        if not project:
            project = Project(**kwargs)
            self.projects.append(project)

        return project


    """
    def head(self, n) -> None:
        # trim all but the first n projects
        self.projects = self.projects[:n]
        
    def sample(self, n) -> None:
        pass

    def sort(self, args: List[str]) -> None:
        #getattr(self, str, default)
        pass
    """
