import csv

from structures import Dataset, DefaultProject, DefaultVersion
from structures.projects import project_map
from structures.versions import version_map
from loaders import Loader


class CsvLoader(Loader):
    def __init__(self):
        # set default headers for csv files
        self.headers = ['name', 'v.version']
        self.user_defined = False

    def load(self, ds: Dataset, filepath: str, headers: str = None) -> None:
        """Loads a csv file."""

        # remove any existing projects
        ds.projects = []

        # user-defined headers override default headers
        if headers:
            self.headers = headers.split()
            self.user_defined = True

        # load the file
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            csv_file = csv.reader(file, delimiter=',')
            for row in csv_file:
                if row[0].startswith('!'):
                    # read in a header row
                    if not self.user_defined:
                        # in-file headers override defaults
                        # (but not user-defined headers from the cli)
                        self.headers = [h[1:] for h in row]
                else:
                    # read in a data row
                    p_data, v_data = {}, {}
                    for i, val in enumerate(row):
                        attr = self.headers[i]

                        # add the data to the project or version
                        if attr.startswith('v.'):
                            v_data[attr[2:]] = val
                        else:
                            p_data[attr] = val

                    # get or create the new project
                    project = ds.find_project(**p_data)
                    if project:
                        # update the existing project
                        project.update(**p_data)

                    else:
                        # map csv headers to project keywords, as applicable
                        uuids, meta = {}, {}
                        if 'name' in p_data:
                            uuids['name'] = lambda p: p.name
                        if 'org' in p_data:
                            meta['org'] = lambda p: p.org
                        if 'url' in p_data:
                            uuids['url'] = lambda p: p.url

                        # create the new project & add it to the dataset
                        p_class = project_map.get(ds.registry, DefaultProject)
                        project = p_class(uuids_=uuids, meta_=meta, **p_data)
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
                            if 'commit' in v_data:
                                uuids['commit'] = lambda v: v.commit

                            # create the new version & add it to the project
                            v_class = version_map.get(ds.registry, DefaultVersion)
                            project.versions.append(v_class(uuids_=uuids, **v_data))
