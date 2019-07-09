import json
from typing import List, Optional
from types import MethodType
from pathlib import Path

from structures.projects import Project


class Dataset:
    def __init__(self, registry: str = None):
        from apis import class_map as apis_list
        from structures import Project
        from functions import function_map
        from util import get_user_name, get_user_email

        # validate registry name (if provided) and set
        if registry and registry not in apis_list:
            raise Exception('Invalid registry. Valid types are: %s'
                            % list(apis_list))
        self.registry = registry

        # set up the api
        api_class = apis_list.get(self.registry, None)
        self.api = None if not api_class else api_class()

        # register the various transformation functions
        for name, function in function_map.items():
            setattr(self, name, MethodType(function, self))

        # a dataset contains projects
        self.projects: List[Project] = []

        # set default dataset metadata
        self.name = None
        self.version = None
        self.description = None
        self.readme = None
        self.author = get_user_name()  # default to git user.name
        self.email = get_user_email()  # default to git user.email

    def load_file(self, path: str, fileargs: str = None) -> None:
        """Uses a file loader to load an initial dataset from file."""
        from loaders.file import class_map

        # check if the path is valid
        if not Path(path).is_file():
            raise Exception('Invalid path; file does not exist.')

        # check if the filetype is valid
        extension = Path(path).suffix
        loader = class_map.get(extension, None)
        if not loader:
            raise Exception("Invalid input file type '%s'. Valid types"
                            "are: %s." % (extension, list(class_map)))

        # load initial data from the file
        print('Loading %s' % path)
        if fileargs:
            loader().load(self, path, fileargs)
        else:
            loader().load(self, path)

    def load_weblist(self, name: str) -> None:
        """Uses a weblist loader to load an initial dataset from a weblist."""
        from loaders.weblist import class_map

        # check if the registry has been set
        if not self.registry:
            raise Exception('Registry has not been set. Valid '
                            'registries are: %s' % str(class_map))

        # check if the name is valid
        loader = class_map.get(self.registry, None)
        if not loader:
            raise Exception('Invalid weblist for %s. Valid weblists'
                            'are: %s' % (self.registry, str(class_map)))

        # load initial data from the weblist
        print("Loading '%s' from %s" % (name, self.registry))
        loader().load(self, name)

    def get_projects_meta(self) -> None:
        """Gets the metadata for all projects."""
        for p in self.projects:
            self.api.get_project(p)

    def get_project_versions(self, historical: str = 'all') -> None:
        """Gets the historical versions for all projects."""
        for p in self.projects:
            self.api.get_versions(p, historical)

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

    def save(self, filepath: str = None) -> None:
        # file name is dataset name, if not provided by user
        filepath = filepath or (self.name + '.json')

        # convert the dataset to an input set json
        inputset = self.to_inputset()

        # save to disk
        print('Saving results to %s' % filepath)
        with open(filepath, 'w') as file:
            json.dump(inputset, file, indent=4)

    def to_inputset(self) -> dict:
        """Converts a dataset to an input set json."""

        # check that all necessary meta values have been set
        if not (self.name and self.version):
            # name and version are mandatory
            raise Exception('Dataset name and/or version are missing.')

        # jsonify the dataset's metadata
        d = dict()
        if self.name: d['name'] = self.name
        if self.version: d['version'] = self.version
        if self.description: d['description'] = self.description
        if self.readme: d['readme'] = self.readme
        if self.author: d['author'] = self.author
        if self.email: d['email'] = self.email

        # jsonify the projects & versions
        d['inputs'] = []
        for p in self.projects:
            d['inputs'].extend(p.to_inputset())

        return d

    def find_project(self, **kwargs) -> Optional[Project]:
        """Gets the first project with attributes matching all kwargs."""

        # build a temporary project containing the kwargs
        this_p = Project(**kwargs)

        # linear search function for now; potentially quite slow...
        for other_p in self.projects:
            # copy over the other project's meta lambda funcs so the two
            # projects can be compared (need to rebind the lambda func
            # to this_p instead of other_p--hence the __func__ ref)
            for k, func in other_p.meta_.items():
                this_p.meta_[k] = MethodType(func.__func__, this_p)

            if this_p == other_p:
                return other_p

        return None

    def __repr__(self):
        return 'Dataset(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
