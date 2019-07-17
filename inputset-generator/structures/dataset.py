import os
import json
import dill as pickle
from typing import List, Optional
from types import MethodType
from pathlib import Path
from dill.source import getsource

from structures.projects import Project


class Dataset(object):
    def __init__(self, registry: str = None, **kwargs):
        from apis import api_map
        from structures.projects import project_map as registry_map
        from structures import Project
        from functions import function_map
        from util import get_name, get_email

        # a dataset contains projects
        self.projects: List[Project] = []

        # set default dataset metadata
        self.name = kwargs.pop('name', None)
        self.version = kwargs.pop('version', None)
        self.description = kwargs.pop('description', None)
        self.readme = kwargs.pop('readme', None)
        self.author = kwargs.pop('author', None) or get_name()
        self.email = kwargs.pop('email', None) or get_email()

        # validate registry name (if provided) and set
        if registry:
            assert registry in registry_map, (
                    'Invalid registry type. Valid types are: '
                    '%s' % list(registry_map))
        self.registry = registry

        # set up the api
        self.api = None
        api_class = api_map.get(self.registry, None)
        if api_class:
            self.api = api_class(**kwargs)

        # register the various transformation functions
        for name, function in function_map.items():
            setattr(self, name, MethodType(function, self))

    @classmethod
    def load_file(cls, filepath: str,
                  registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from a file."""
        from loaders.file import fileloader_map

        # check if the path is valid
        assert Path(filepath).is_file(), 'Invalid path; file does not exist.'

        # check if the filetype is valid
        extension = Path(filepath).suffix
        loader = fileloader_map.get(extension, None)
        assert loader, ("Invalid input file type '%s'. Valid types"
                        'are: %s.' % (extension, list(fileloader_map)))

        # load initial data from the file
        print('Loading %s' % filepath)
        return loader.load(filepath, registry=registry, **kwargs)

    @classmethod
    def load_weblist(cls, name: str,
                     registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from a weblist."""
        from loaders.weblist import weblistloader_map

        # check if the name is valid
        loader = weblistloader_map.get(registry, None)
        assert loader, ('Invalid weblist for %s. Valid weblists are: '
                        '%s' % (registry, str(weblistloader_map)))

        # load initial data from the weblist
        print('Loading %s %s' % (registry, name))
        return loader.load(name, registry=registry, **kwargs)

    @classmethod
    def restore(cls, filepath: str) -> 'Dataset':
        """Factory method that restores a pickled dataset."""
        from loaders.core import DatasetLoader

        # check if the path is valid
        assert Path(filepath).is_file(), 'Invalid path; file does not exist.'

        # load the pickled dataset
        return DatasetLoader.load(filepath)

    def backup(self, filepath: str = None) -> None:
        """Pickles a dataset."""

        # file name is dataset name, if not provided by user
        filepath = filepath or (self.name + '.p')

        # save to disk
        print('Saving dataset to %s' % filepath)
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def import_inputset(cls, filepath: str,
                        registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from an R2C input set json."""
        from loaders.core import R2cLoader

        # check if the path is valid
        assert Path(filepath).is_file(), 'Invalid path; file does not exist.'

        # load the input set
        print('Loading %s input set from %s' % (registry, filepath))
        return R2cLoader.load(filepath, registry=registry, **kwargs)

    def export_inputset(self, filepath: str = None) -> None:
        """Exports a dataset to an r2c input set json file."""

        # file name is dataset name, if not provided by user
        filepath = filepath or (self.name + '.json')

        # convert the dataset to an input set json
        inputset = self.to_inputset()

        # save to disk
        print('Exporting input set to %s' % filepath)
        with open(filepath, 'w') as file:
            json.dump(inputset, file, indent=4)

    def set_meta(self, name: str = None, version: str = None,
                 description: str = None, readme: str = None,
                 author: str = None, email: str = None) -> None:
        """Sets dataset metadata."""
        assert (name or version or description or readme or author
                or email), ('Error setting metadata. Must provide at '
                            'least one of name, version, description, '
                            'readme, author, or email.')

        # override existing data only if the override is not None
        self.name = name or self.name
        self.version = version or self.version
        self.description = description or self.description
        self.readme = readme or self.readme
        self.author = author or self.author
        self.email = email or self.email

    def to_inputset(self) -> dict:
        """Converts a dataset to an input set json."""

        # name and version are mandatory
        assert self.name and self.version, (
            'Dataset name and/or version are missing. Set them using '
            "the 'meta' command.")

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

    def get_projects_meta(self, **kwargs) -> None:
        """Gets the metadata for all projects."""
        for p in self.projects:
            self.api.get_project(p, **kwargs)

    def get_project_versions(self, **kwargs) -> None:
        """Gets the historical versions for all projects."""
        for p in self.projects:
            self.api.get_versions(p, **kwargs)

    def find_project(self, **kwargs) -> Optional[Project]:
        """Gets the first project with attributes matching all kwargs."""

        # build a temporary project containing the kwargs
        this_p = Project(**kwargs)

        # linear search function for now; potentially quite slow...
        for other_p in self.projects:
            # copy over the other project's uuid lambda funcs so the two
            # projects can be compared (need to rebind the lambda func
            # to this_p instead of other_p--hence the __func__ ref)
            for k, func in other_p.uuids_.items():
                this_p.uuids_[k] = MethodType(func.__func__, this_p)

            if this_p == other_p:
                return other_p

        return None

    def __repr__(self):
        return 'Dataset(%s' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a, None)
               and a is not 'projects'             # ignore projects list
               and not a.startswith('__')          # ignore dunders
               and not callable(getattr(self, a))  # ignore functions
        ]) + ', projects=[%s])' % ('...' if self.projects else '')
