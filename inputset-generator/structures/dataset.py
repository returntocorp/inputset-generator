import json
import dill as pickle
from typing import List, Optional
from types import MethodType
from pathlib import Path
from dill.source import getsource

from structures.projects import Project


class Dataset(object):
    def __init__(self, registry: str = None, **kwargs):
        from apis import api_map as apis_list
        from structures import Project
        from functions import function_map
        from util import get_user_name, get_user_email

        # validate registry name (if provided) and set
        assert registry and registry in apis_list, \
            'Invalid registry type. Valid types are: %s' % list(apis_list)
        self.registry = registry

        # set up the api
        api_class = apis_list.get(self.registry, None)
        cache_dir = kwargs.get('cache_dir', None)
        cache_timeout = kwargs.get('cache_timeout', None)
        self.api = None if not api_class \
            else api_class(cache_dir=cache_dir, cache_timeout=cache_timeout)

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
    def restore(cls, filepath: str, **kwargs) -> 'Dataset':
        """Factory method that restores a pickled dataset."""
        from loaders.core import DatasetLoader

        # check if the path is valid
        assert Path(filepath).is_file(), 'Invalid path; file does not exist.'

        # load the pickled dataset
        return DatasetLoader.load(filepath, **kwargs)

    def backup(self, filepath: str = None) -> None:
        """Pickles a dataset."""

        # file name is dataset name, if not provided by user
        filepath = filepath or (self.name + '.pickle')

        # save to disk
        print('Saving dataset to %s' % filepath)
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    def to_json(self) -> dict:
        """Converts a complete dataset to a json."""

        # grab dataset attributes
        data = {
            attr: val for attr, val in vars(self).items()
            if attr not in ['api', 'projects']
               and not callable(val)
        }

        # add project (& version) attributes
        data['projects'] = [p.to_json() for p in self.projects]

        return data

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

    def get_projects_meta(self, nocache: bool = False) -> None:
        """Gets the metadata for all projects."""
        for p in self.projects:
            self.api.get_project(p, nocache=nocache)

    def get_project_versions(self, historical: str = 'all',
                             nocache: bool = False) -> None:
        """Gets the historical versions for all projects."""
        for p in self.projects:
            self.api.get_versions(p, historical=historical, nocache=nocache)

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

    def head(self, n: int = 5, details: bool = False):
        """Summarizes the key data of the first n projects."""
        for p in self.projects[:n]:
            project_type = str(type(p).__name__)
            attr_indent = len(project_type) + 5
            val_indent = 11

            # print project uuids
            print('%s(%s' % (
                (' ' * 4) + project_type,
                ('\n' + ' ' * attr_indent).join([
                    '%s = %s' % (
                        a.ljust(val_indent - 3),
                        str(func())) for a, func in p.uuids_.items()
                ])
            ))

            # print versions
            print('%s = [%s])' % (
                (' ' * attr_indent) + 'versions',
                ('\n' + ' ' * (attr_indent + val_indent + 1)).join([
                    repr(v) for v in p.versions
                ])
            ))

    def describe(self, scope: str = 'dataset'):
        """Describes the dataset/project/version structures."""
        from structures import DefaultProject, DefaultVersion
        from structures.projects import project_map
        from structures.versions import version_map

        '''
        https://stackoverflow.com/questions/9989334/create-nice-column-output-in-python        
        table_data = [
            ['a', 'b', 'c'],
            ['aaaaaaaaaa', 'b', 'c'],
            ['a', 'bbbbbbbbmsk', 'c']
        ]
        for row in table_data:
            print("{: <20} {: <20} {: <20}".format(*row))
        '''

        if scope == 'dataset':
            # describe the dataset
            col_width = 13

            # print the attributes in the following order:
            attrs = ['registry', 'name', 'version',
                     'description', 'readme', 'author', 'email']
            for a in attrs:
                val = getattr(self, a, None)
                print('    %s%s' % (a.ljust(col_width), val))

            # print projects summary info
            print('    projects')
            project_type = project_map.get(self.registry,
                                           DefaultProject).__name__
            print('    %s%s' % ('    type'.ljust(col_width),
                                'list(%s)' % project_type))
            print('    %s%d' % ('    len'.ljust(col_width),
                                len(self.projects)))

        elif scope in ['project', 'version']:
            # describe a project or version
            obj = self.projects[0]
            if scope == 'version':
                obj = self.projects[0].versions[0]

            # calculate the width of the first columne
            col_width = max([len(a) for a in vars(obj)]) + 2

            # print uuids & meta vars
            for key in ['uuids', 'meta']:
                print('    %s' % key)
                key_dict = getattr(obj, key + '_')
                if len(key_dict) == 0:
                    print('    none')
                for a, func in key_dict.items():
                    # convert the lambda function code to a string
                    func_str = getsource(func).split(': ', 1)[1].strip()
                    print('    %s%s' % (
                        ('    ' + a).ljust(col_width),
                        func_str
                    ))

            # print all the attributes
            special_attrs = ['uuids_', 'meta_', 'versions']
            for a in sorted(vars(obj)):
                if a in special_attrs:
                    continue

                print('    %s%s' % (
                    a.ljust(col_width),
                    type(getattr(obj, a)).__name__
                ))

            if scope == 'project':
                # print versions summary info, if applicable
                print('    versions')
                version_type = version_map.get(self.registry,
                                               DefaultVersion).__name__
                print('    %s%s' % (
                    '    type'.ljust(col_width),
                    'list(%s)' % version_type
                ))
                print('    %s%d' % (
                    '    len'.ljust(col_width),
                    len(obj.versions)
                ))

    def __repr__(self):
        return 'Dataset(%s' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a, None)
               and a is not 'projects'             # ignore projects list
               and not a.startswith('__')          # ignore dunders
               and not callable(getattr(self, a))  # ignore functions
        ]) + ', projects=[%s])' % ('...' if self.projects else '')
