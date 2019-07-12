import json

from loaders import Loader
from structures import Dataset, DefaultProject, DefaultVersion
from structures.projects import project_map
from structures.versions import version_map
from apis import api_map


class DatasetLoader(Loader):
    def load(self, ds: Dataset, filepath: str, **_) -> None:
        """Loads a complete dataset from a json file."""

        # load the file
        data = json.load(open(filepath))

        # remove any existing projects
        ds.projects = []

        # set dataset attributes
        for attr, val in data.items():
            if attr == 'projects':
                continue

            # add the attribute to the dataset
            setattr(ds, attr, val)

            if attr == 'registry':
                # add an api to the dataset
                ds.api = api_map.get(val, None)

        # set projects & versions
        projects = []
        for p_data in data['projects']:
            # figure out project/version classes
            p_class = project_map.get(ds.registry, DefaultProject)
            v_class = version_map.get(ds.registry, DefaultVersion)

            # create the versions list
            versions = []
            v_list = p_data.pop('versions')
            for v_data in v_list:
                # convert uuids/meta from strings to functions
                for key, func in v_data['uuids_'].items():
                    v_data['uuids_'][key] = eval(func)
                for key, func in v_data['meta_'].items():
                    v_data['meta_'][key] = eval(func)

                # initialize the version
                versions.append(v_class(**v_data))

            # convert uuids/meta from strings to functions
            for key, func in p_data['uuids_'].items():
                p_data['uuids_'][key] = eval(func)
            for key, func in p_data['meta_'].items():
                p_data['meta_'][key] = eval(func)

            # initialize the project, add the versions
            project = p_class(**p_data)
            project.versions = versions
            projects.append(project)

        # add the projects to the dataset
        ds.projects = projects
