import csv

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset, DefaultProject, DefaultVersion
from r2c_isg.structures.projects import project_map
from r2c_isg.structures.versions import version_map


class CsvLoader(Loader):
    @classmethod
    def load(cls, filepath: str, **kwargs) -> Dataset:
        """Loads a csv file."""

        # user-defined headers override default headers
        headers = kwargs.pop('fileargs', None)
        if headers:
            user_defined = True
            headers = headers.split()
        else:
            user_defined = False
            # default headers are name and version string
            headers = ['name', 'v.version']

        # initialize a dataset
        ds = Dataset(**kwargs)

        # load the file
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            csv_file = csv.reader(file, delimiter=',')
            for row in csv_file:
                if row[0].startswith('!'):
                    # read in a header row
                    if not user_defined:
                        # in-file headers override defaults
                        # (but not user-defined headers from the cli)
                        headers = [h[1:] for h in row]
                else:
                    # ensure we have as many headers as cells in the row
                    if len(row) > len(headers):
                        raise Exception('A column is missing a header. Review '
                                        "the input file's column headers.")

                    # read in a data row
                    p_data, v_data = {}, {}
                    for i, val in enumerate(row):
                        attr = headers[i]

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

        return ds
