import json
from tqdm import tqdm

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset, DefaultProject, DefaultVersion
from r2c_isg.structures.projects import project_map
from r2c_isg.structures.versions import version_map


class R2cLoader(Loader):
    @classmethod
    def load(cls, filepath: str, **kwargs) -> Dataset:
        """Loads an r2c input set json file."""

        # initialize the dataset
        ds = Dataset(**kwargs)

        # load the file
        data = json.load(open(filepath))

        # remove any existing projects
        ds.projects = []

        # don't overwrite previously set metadata
        ds.name = ds.name or data['name']
        ds.version = ds.version or data['version']

        # grab any optional metadata
        ds.description = ds.description or data.get('description', None)
        ds.readme = ds.readme or data.get('readme', None)
        ds.author = ds.author or data.get('author', None)
        ds.email = ds.email or data.get('email', None)

        # generate the projects and versions
        for input_ in tqdm(data['inputs'], desc='         Importing',
                           unit=' inputs', leave=False):
            # split out project- vs. version-level information
            p_data, v_data = {}, {}
            p_keys = ['repo_url', 'url', 'package_name']
            v_keys = ['commit_hash', 'version']
            for k, val in input_.items():
                # add the attribute to the project or version
                if k in v_keys:
                    v_data[k] = val
                elif k in p_keys:
                    p_data[k] = val

            # get or create the new project
            project = ds.find_project(**p_data)
            if project:
                # update the existing project
                project.update(**p_data)

            else:
                # map json headers to project keywords, as applicable
                uuids = {}
                if 'package_name' in p_data:
                    uuids['name'] = lambda p: p.package_name
                if 'repo_url' in p_data:
                    uuids['url'] = lambda p: p.repo_url
                if 'url' in p_data:
                    uuids['url'] = lambda p: p.url

                # create the new project & add it to the dataset
                p_class = project_map.get(ds.registry, DefaultProject)
                project = p_class(uuids_=uuids, **p_data)
                ds.projects.append(project)

            # create the new version, if it doesn't already exist
            if v_data:
                version = project.find_version(**v_data)
                if version:
                    # update the existing version
                    version.update(**v_data)

                else:
                    # map csv headers to version keywords, as applicable
                    uuids = {}
                    if 'version' in v_data:
                        uuids['version'] = lambda v: v.version
                    if 'commit_hash' in v_data:
                        uuids['commit'] = lambda v: v.commit_hash

                    # create the new version & add it to the project
                    v_class = version_map.get(ds.registry, DefaultVersion)
                    project.versions.append(v_class(uuids_=uuids, **v_data))

        return ds
