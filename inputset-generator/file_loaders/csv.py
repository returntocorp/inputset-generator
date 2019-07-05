import csv

from structures import Dataset
from file_loaders import FileLoader


class CsvLoader(FileLoader):
    def __init__(self):
        # set default headers for csv files
        self.headers = ['name', 'v.version']
        self.user_defined = False

    def load(self, ds: Dataset, filepath: str,
             headers: str = None) -> None:
        """Loads a csv file."""

        # user-defined headers override default headers
        if headers:
            self.headers = headers.split()
            self.user_defined = True

        # load the file
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            csv_file = csv.reader(file, delimiter=',')
            for row in csv_file:
                # aggregate version and project data
                p_data, v_data = {}, {}

                if row[0].startswith('!'):
                    # read in a header row
                    # in-file headers override default/user-defined
                    self.headers = [h[1:] for h in row]
                else:
                    # read in a data row
                    for i, val in enumerate(row):
                        header = self.headers[i]
                        if header.startswith('v.'):
                            # val is a version attribute
                            v_data[header[2:]] = val
                        else:
                            # val is a project attribute
                            p_data[header] = val

                    # create/update the projects and versions
                    project_cls = ds.types['project']
                    project = ds.get_or_add_project(project_cls, **p_data)
                    if len(v_data) > 0:
                        version_cls = ds.types['version']
                        project.get_or_add_version(version_cls, **v_data)
