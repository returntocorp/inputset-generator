import json
from tqdm import tqdm
import dill as pickle
from typing import List, Optional
from types import MethodType
from pathlib import Path

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

        # set project metadata
        self.name = None
        self.version = None
        self.description = None
        self.readme = None
        self.author = get_name()
        self.email = get_email()
        self.update(**kwargs)

        # validate registry name (if provided) and set
        if registry and registry not in registry_map:
            raise Exception('Invalid registry type. Valid types are: '
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

    def update(self, **kwargs):
        """Updates a dataset's metadata."""

        # set default dataset metadata
        self.name = kwargs.pop('name', self.name)
        self.version = kwargs.pop('version', self.version)
        self.description = kwargs.pop('description', self.description)
        self.readme = kwargs.pop('readme', self.readme)
        self.author = kwargs.pop('author', self.author)
        self.email = kwargs.pop('email', self.email)

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
        ds = loader.load(filepath, registry=registry, **kwargs)

        print('    Loaded {:,} projects containing {:,} total versions.'
              .format(len(ds.projects),
                      sum([len(p.versions) for p in ds.projects])))

        return ds

    @classmethod
    def load_weblist(cls, weblist: str,
                     registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from a weblist."""
        from loaders.weblist import weblistloader_map

        # check if the name is valid
        loader = weblistloader_map.get(registry, None)
        assert loader, ('Invalid weblist for %s. Valid weblists are: '
                        '%s' % (registry, str(weblistloader_map)))

        # load initial data from the weblist
        ds = loader.load(weblist, registry=registry, **kwargs)

        print('    Loaded {:,} projects containing {:,} total versions.'
              .format(len(ds.projects),
                      sum([len(p.versions) for p in ds.projects])))

        return ds

    @classmethod
    def restore(cls, filepath: str) -> 'Dataset':
        """Factory method that restores a pickled dataset."""
        from loaders.core import DatasetLoader

        # check if the path is valid
        assert Path(filepath).is_file(), 'Invalid path; file does not exist.'

        # load the pickled dataset
        ds = DatasetLoader.load(filepath)

        print('    Restored {:,} projects containing {:,} total versions.'
              .format(len(ds.projects),
                      sum([len(p.versions) for p in ds.projects])))

        return ds

    def backup(self, filepath: str = None) -> None:
        """Pickles a dataset."""

        # file name is dataset name, if not provided by user
        filepath = filepath or (self.name + '.p')

        # save to disk
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

        print('    Backed up dataset to %s.' % filepath)

    @classmethod
    def import_inputset(cls, filepath: str,
                        registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from an R2C input set json."""
        from loaders.core import R2cLoader

        # check if the path is valid
        assert Path(filepath).is_file(), 'Invalid path; file does not exist.'

        # load the input set
        ds = R2cLoader.load(filepath, registry=registry, **kwargs)
        print('    Loaded {:,} projects containing {:,} total versions.'.format(
            len(ds.projects),
            sum([len(p.versions) for p in ds.projects])
        ))
        return ds

    def export_inputset(self, filepath: str = None) -> None:
        """Exports a dataset to an r2c input set json file."""

        # file name is dataset name, if not provided by user
        filepath = filepath or (self.name + '.json')

        # convert the dataset to an input set json
        inputset = self.to_inputset()

        # save to disk
        with open(filepath, 'w') as file:
            json.dump(inputset, file, indent=4)
        print('    Exported input set to %s' % filepath)

    def to_inputset(self) -> dict:
        """Converts a dataset to an input set json."""

        # name and version are mandatory
        if not (self.name and self.version):
            raise Exception('Dataset name and/or version are missing. '
                            "Set them using the 'meta' command.")

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
        for p in tqdm(self.projects, desc='    Exporting',
                      unit=' projects', leave=False):
            d['inputs'].extend(p.to_inputset())

        return d

    def get_projects_meta(self, **kwargs) -> None:
        """Gets the metadata for all projects."""

        for p in tqdm(self.projects, desc='    Getting project metadata:',
                      unit=' projects', leave=False):
            self.api.get_project(p, **kwargs)

        print('    Retrieved metadata for {:,} projects.'
              .format(len(self.projects)))

    def get_project_versions(self, **kwargs) -> None:
        """Gets the historical versions for all projects."""

        for p in tqdm(self.projects, unit=' projects', leave=False,
                      desc='    Getting %s versions'
                           % kwargs.get('historical', 'all')):
            self.api.get_versions(p, **kwargs)

        print('    Retrieved {:,} total versions of {:,} projects.'
              .format(sum([len(p.versions) for p in self.projects]),
                      len(self.projects)))

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
