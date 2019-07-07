import csv

from structures import Dataset, Project
from structures.projects import class_map
from loaders import Loader


class CsvLoader(Loader):
    def __init__(self):
        # set default headers for csv files
        self.headers = ['name', 'v.version']
        self.user_defined = False

    def load(self, ds: Dataset, filepath: str, headers: str = None) -> None:
        """Loads a csv file."""

        """
        Note: During initialization, all Project classes recognize the
        following csv header keywords:
            '!name'
            '!project_url'
            '!api_url'

        The GithubRepo class recognizes:
            '!organization'
            
        The NpmVersion and PypiRelease version classes recognize:
            '!v.version_string'

        The GithubCommit version class recognizes:
            '!v.commit_hash'
        """

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
                    # in-file headers override default/user-defined
                    self.headers = [h[1:] for h in row]
                else:
                    # read in a data row
                    data = {}
                    for i, val in enumerate(row):
                        header = self.headers[i]
                        if header.startswith('v.'):
                            # val is a version attribute
                            data.setdefault('_versions', [{}])
                            data['_versions'][0][header[2:]] = val
                        else:
                            # val is a project attribute
                            data[header] = val

                    # figure out which type of project to create
                    # (default is the vanilla Project)
                    project_cls = class_map.get(ds.registry, Project)

                    # create the new project & add versions to it
                    project = project_cls(**data)

                    # add the project (& versions) to the dataset
                    ds.projects.append(project)
