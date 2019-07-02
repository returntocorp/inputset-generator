from pathlib import Path
from typing import List, Optional
from types import MethodType

from .project import Project


class Dataset:
    def __init__(self):
        from functions import functions
        from util import get_user_name, get_user_email

        # a dataset contains projects
        self.projects: List[Project] = []

        # registry is used to access web resources
        self.registry = None

        # register the various transformation functions
        for name, function in functions.items():
            setattr(self, name, MethodType(function, self))

        # set default dataset metadata
        self.name = None
        self.version = None
        self.description = None
        self.readme = None
        self.author = get_user_name()
        self.email = get_user_email()

    def set_meta(self, name=None, version=None, description=None,
                 readme=None, author=None, email=None):
        """Sets dataset metadata."""
        if not (name or version or description
                or readme or author or email):
            raise Exception('Error setting metadata. Must provide at '
                            'least one of name, version, description, '
                            'readme, author, or email.')

        # override existing data only if the override is not None
        self.name = name or self.name
        self.version = version or self.version
        self.description = description or self.description
        self.readme = readme or self.readme
        self.author = author or self.author
        self.email = email or self.email

    def set_registry(self, registry: str) -> None:
        """Loads up the specified registry."""
        from registries import registries

        # check if the registry name is valid
        if registry not in registries:
            raise Exception('Invalid registry. Valid types are: %s'
                            % list(registries))

        # link to the appropriate registry
        self.registry = registries[registry]

    def load_file(self, path: str) -> None:
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
        print('Loading %s...' % path)
        file_handlers[extension].load(self, path)

    def load_weblist(self, name: str) -> None:
        """Loads a weblist from the registry."""
        from registries import registries

        # check if the registry has been set
        if not self.registry:
            raise Exception('Registry has not been set. Valid '
                            'registries are: %s' % list(registries))

        # check if the name is valid
        names = list(self.registry.weblists)
        if name not in names:
            raise Exception('Invalid weblist for registry %s. Valid '
                            'weblists are: %s' % (self.registry.name,
                                                  names))

        # load initial data from the weblist
        print("Loading '%s' from %s..." % (name, self.registry.name))
        self.registry.load_weblist(self, name)

    def load_project_metadata(self) -> None:
        """Downloads all projects' metadata."""
        from registries import registries

        # check if the registry has been set
        if not self.registry:
            raise Exception('Registry has not been set. Valid '
                            'registries are: %s' % list(registries))

        for project in self.projects:
            print("Retrieving details on %s..." % project)
            self.registry.load_project_metadata(project)

    def load_project_versions(self, historical: str):
        """Downloads all projects' versions."""
        from registries import registries

        # check if the registry has been set
        if not self.registry:
            raise Exception('Registry has not been set. Valid '
                            'registries are: %s' % list(registries))

        for project in self.projects:
            print("Retrieving versions of %s..." % project)
            self.registry.load_project_versions(project, historical)

    def jsonify(self) -> dict:
        """Jsonifies a dataset."""
        from file_handlers import JsonFileHandler

        return JsonFileHandler()._jsonify(self)

    def save_json(self, path: str = None) -> None:
        from file_handlers import JsonFileHandler

        # check that all necessary meta values have been set
        if not (self.name and self.version):
            # name and version are mandatory
            raise Exception('Dataset name and/or version are missing.')

        # file name is dataset name, if not provided by user
        path = path or (self.name + '.json')

        # save to disk
        print('Saving results to %s' % path)
        JsonFileHandler().save(self, path)

    def get_project(self, **kwargs) -> Optional[Project]:
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

    def _get_or_add_project(self, **kwargs) -> Project:
        """Finds a matching project or adds a new one."""
        project = self.get_project(**kwargs)
        if not project:
            project = Project(**kwargs)
            self.projects.append(project)

        return project

    def __repr__(self):
        return 'Dataset(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
