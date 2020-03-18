import json
import random
import dill as pickle
from dill.source import getsource
from tqdm import tqdm
from typing import List, Optional
from types import MethodType
from pathlib import Path

from r2c_isg.structures.core import Project


class Dataset(object):
    def __init__(self, registry: str = None, **kwargs):
        from r2c_isg.apis import api_map
        from r2c_isg.structures import project_map as registry_map
        from r2c_isg.structures import Project
        from r2c_isg.util import get_name, get_email

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
            raise Exception('Invalid registry type name. Valid types '
                            'are: %s' % list(registry_map))
        self.registry = registry

        # set up the api
        self.api = None
        api_class = api_map.get(self.registry, None)
        if api_class:
            self.api = api_class(**kwargs)

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
        from r2c_isg.loaders.file import fileloader_map

        # check if the path is valid
        if not Path(filepath).is_file():
            raise Exception('Invalid path; file does not exist.')

        # check if the filetype is valid
        extension = Path(filepath).suffix
        loader = fileloader_map.get(extension, None)
        if not loader:
            raise Exception("Invalid input file type '%s'. Valid file types "
                            'are: %s.' % (extension, list(fileloader_map)))

        # load initial data from the file
        ds = loader.load(filepath, registry=registry, **kwargs)

        print('         Loaded {:,} projects containing {:,} total versions.'
              .format(len(ds.projects),
                      sum([len(p.versions) for p in ds.projects])))

        return ds

    @classmethod
    def load_web(cls, name: str,
                 registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from a weblist or org name (github only)."""
        from r2c_isg.loaders.weblist import webloader_map

        # check if the registry is valid
        loader = webloader_map.get(registry)
        if not loader:
            raise Exception('Invalid registry name. Valid registries are %s'
                            % str(webloader_map.keys()))

        # load data from the weblist/org projects list
        ds = loader.load(name, registry=registry, **kwargs)

        print('         Loaded {:,} projects containing {:,} total versions.'
              .format(len(ds.projects),
                      sum([len(p.versions) for p in ds.projects])))

        return ds

    @classmethod
    def restore(cls, filepath: str) -> 'Dataset':
        """Factory method that restores a pickled dataset."""
        from r2c_isg.loaders import DatasetLoader

        # check if the path is valid
        if not Path(filepath).is_file():
            raise Exception('Invalid path; file does not exist.')

        # load the pickled dataset
        ds = DatasetLoader.load(filepath)

        print('         Restored {:,} projects containing {:,} total versions.'
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

        print('         Backed up dataset to %s.' % filepath)

    @classmethod
    def import_inputset(cls, filepath: str,
                        registry: str = None, **kwargs) -> 'Dataset':
        """Factory method that builds a dataset from an R2C input set json."""
        from r2c_isg.loaders import R2cLoader

        # check if the path is valid
        if not Path(filepath).is_file():
            raise Exception('Invalid path; file does not exist.')

        # load the input set
        ds = R2cLoader.load(filepath, registry=registry, **kwargs)
        print('         Loaded {:,} projects containing {:,} total versions.'.format(
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
        print('         Exported input set to %s.' % filepath)

    def sample(self, n: int, on_versions: bool = True, seed: str = None):
        """Samples n projects in place."""

        # seed random, if a seed was provided
        if seed:
            random.seed(seed)

        # select a sample of versions in each project
        if on_versions:
            dropped = 0
            for project in self.projects:
                dropped += len(project.versions)
                if len(project.versions) > n:
                    project.versions = random.sample(project.versions, n)
                dropped -= len(project.versions)

            print('         Sampled {:,} versions from each of {:,} projects ({:,} '
                  'total versions dropped).'.format(n, len(self.projects), dropped))

        # select a sample of projects
        elif len(self.projects) > n:
            orig_count = len(self.projects)
            self.projects = random.sample(self.projects, n)
            print('         Sampled {:,} projects from {:,} (dropped {:,}).'
                  .format(n, orig_count, max(orig_count - n, 0)))

        else:
            # this should never happen...
            raise Exception('Dataset has no projects; cannot sample.')

    def sort(self, params: List[str]) -> None:
        """Sorts the projects/versions based on the given parameters."""
        # useful url: https://realpython.com/python-sort/

        # organize the params list--sort by last param first
        # default sort order is ascending
        if params[0] not in ['asc', 'desc']:
            params.insert(0, 'asc')
        # reverse the list
        params = params[::-1]
        # re-insert the sort orders before their associated sort keys
        insert_at = 0
        for i in range(len(params)):
            if params[i] in ['asc', 'desc']:
                param = params.pop(i)
                params.insert(insert_at, param)
                insert_at = i + 1

        # sort the dataset
        reverse = True
        for param in params:
            if param in ['asc', 'desc']:
                # set the sort order
                reverse = (param == 'desc')

            else:
                # sort on this parameter
                # Note: Parameter strings can follow these formats:
                #   'attr'               sort on project attribute
                #   'uuids.key'          sort on project uuid
                #   'meta.key'           sort on project meta
                #   'v.attr'             sort on version attribute
                #   'v.uuids.key'   sort on version uuid
                #   'v.meta.key'         sort on version meta

                p_list = param.split('.')

                # determine if we're sorting on project or version
                on_project = True
                if p_list[0] == 'v':
                    on_project = False
                    p_list.pop(0)

                # build a sort function
                attr = p_list[0]
                if attr == 'uuids':
                    # sort on a uuid value
                    def sort_uuid(o: object):
                        if not key in o.uuids_:
                            raise Exception('Nonexistent sort key.')

                        return o.uuids_[key]()

                    key = p_list[1]
                    sort_func = lambda o: sort_uuid(o)

                elif attr == 'meta':
                    # sort on a meta value
                    def sort_meta(o: object):
                        if not key in o.meta_:
                            raise Exception('Nonexistent sort key.')

                        return o.meta_[key]()

                    key = p_list[1]
                    sort_func = lambda o: sort_meta(o)

                else:
                    # sort on a regular attribute
                    def sort_attr(o: object):
                        if not hasattr(o, attr):
                            print("         Warning: Sort key '%s' was not "
                                  'found in all projects/versions; assuming '
                                  "'' for those items." % attr)

                        # get & clean up the attribute
                        val = getattr(o, attr, '')
                        if isinstance(val, str):
                            val = val.lower()

                        return val

                    sort_func = lambda o: sort_attr(o)

                # perform the sort
                if on_project:
                    # sort on project
                    self.projects.sort(key=sort_func, reverse=reverse)
                else:
                    # sort on version
                    for project in self.projects:
                        project.versions.sort(key=sort_func, reverse=reverse)

        total_versions = sum([len(p.versions) for p in self.projects])
        print('         Sorted {:,} projects and {:,} versions by {}.'
              .format(len(self.projects), total_versions, str(params)))

    def trim(self, n: int, on_versions: bool = False) -> None:
        """Keep only the first n projects inplace."""

        # select a sample of versions in each project
        if on_versions:
            dropped = 0
            for project in self.projects:
                dropped += len(project.versions)
                project.versions = project.versions[:n]
                dropped -= len(project.versions)

            print('         Trimmed to first {:,} versions in each project '
                  '({:,} total versions dropped).'.format(n, dropped))

        # select a sample of projects
        else:
            orig_count = len(self.projects)
            self.projects = self.projects[:n]
            print('         Trimmed to first {:,} projects ({:,} dropped).'
                  .format(n, max(orig_count - n, 0)))

    def to_inputset(self) -> dict:
        """Converts a dataset to an input set json."""

        # name and version are mandatory
        if not (self.name and self.version):
            raise Exception('The dataset must have a name and version. '
                            "Set them using the 'set-meta -n NAME -v "
                            "VERSION' command.")

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
        for p in tqdm(self.projects, desc='         Exporting',
                      unit='project', leave=False):
            d['inputs'].extend(p.to_inputset())

        return d

    def to_json(self) -> dict:
        """Converts a dataset into json and saves to disk."""

        def extract_vars(obj: object) -> dict:
            """Extracts attributes from a dataset/project/version."""
            vars_dict = {}
            for attr, val in vars(obj).items():
                if callable(val):
                    # function; skip
                    pass

                elif attr in ['uuids_', 'meta_']:
                    # convert lambda functions to strings
                    vars_dict[attr] = {
                        key: getsource(func).split(': ', 1)[1].strip(',\n')
                        for key, func in val.items()
                    }

                elif attr not in ['api', 'projects', 'versions']:
                    # regular attr, add to dict
                    vars_dict[attr] = val

            return vars_dict

        # convert the entire dataset into a vars dict
        data_dict = extract_vars(self)
        data_dict['projects'] = []

        # convert all projects to vars dicts
        for project in tqdm(self.projects, desc='         Jsonifying',
                            unit='project', leave=False):
            p_dict = extract_vars(project)
            p_dict['versions'] = []
            data_dict['projects'].append(p_dict)

            # convert all versions to vars dicts
            for version in project.versions:
                v_dict = extract_vars(version)
                p_dict['versions'].append(v_dict)

        return data_dict

    def get_projects_meta(self, **kwargs) -> None:
        """Gets the metadata for all projects."""

        if not self.api:
            raise Exception('No API is associated with this dataset; '
                            'cannot get project metadata.')

        for p in tqdm(self.projects, unit='project', leave=False,
                      desc='         Getting project metadata',):

            self.api.get_project(p, **kwargs)

        print('         Retrieved metadata for {:,} projects.'
              .format(len(self.projects)))

    def get_project_versions(self, **kwargs) -> None:
        """Gets the historical versions for all projects."""

        if not self.api:
            raise Exception('No API is associated with this dataset; '
                            'cannot get project versions.')

        for p in tqdm(self.projects, unit='project', leave=False,
                      desc='         Getting %s version'
                           % kwargs.get('historical', 'all')):
            self.api.get_versions(p, **kwargs)

        print('         Retrieved {:,} total versions of {:,} projects.'
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
               and a is not 'projects'                  # ignore projects list
               and not a.startswith('__')          # ignore dunders
               and not callable(getattr(self, a))  # ignore functions
        ]) + ', projects=[%s])' % ('...' if self.projects else '')
