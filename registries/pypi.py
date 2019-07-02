import requests

from registries import Registry
from structures import Dataset, Project


class PypiRegistry(Registry):
    def __init__(self):
        super().__init__()

        # set project registry name and url format
        self.name = 'pypi'
        self.url_format = 'https://pypi.python.org/pypi/%s/json'

        self.weblists = {
            'top5kmonth': {
                'loader': self._load_top5kmonth,
                'parser': self._parse_hugovk
            },
            'top5kyear': {
                'loader': self._load_top5kyear,
                'parser': self._parse_hugovk
            }
        }

    def load_project_metadata(self, project: Project) -> None:
        """Retrieves all project data from the registry."""
        if not getattr(self, 'notified', None):
            print('Note: For PyPi registry, project metadata and '
                  'project versions come from the same url. To avoid '
                  'duplicate requests, please use only one of the '
                  "'-m' and '-v' flags.")
            self.notified = True

        # default to loading all versions
        self.load_project_versions(project, 'all')


    def load_project_versions(self, project: Project,
                              historical: str = 'all') -> None:
        """Retrieves all version data from the registry."""

        # get the project info
        name = getattr(project, 'package_name')
        data = requests.get(self.url_format % name).json()

        # pull out version-level data
        version_data = data.pop('releases')

        # populate the project with the remaining data
        info = data.pop('info')  # break out info dict for easier sort
        data.update(info)
        project.populate(data)

        # add versions to the project (overwrite any existing versions)
        # NOTE: Pypi occasionally has versions with multiple releases.
        # This appears to be due to having a whl and tar.gz distribution
        # of the same release. For now, just take the first release.
        project.versions = []
        for version_str, data in version_data.items():
            kwargs = {'version': version_str}
            if len(data) > 0:
                kwargs.update(data[0])
            version = project.get_or_add_version(**kwargs)
            version.historical = version_str

        # filter the versions for specific tags/releases
        hist_types = ['latest', 'major', 'minor', 'all']

        if historical not in hist_types:
            raise Exception("Unrecognized historical selection '%s'. "
                            "Valid selections are: %s" % (historical,
                                                          str(hist_types)))

        # Todo: Complete historical version filtering.

    @staticmethod
    def _load_top5kyear() -> dict:
        url = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json'
        return requests.get(url).json()

    @staticmethod
    def _load_top5kmonth() -> dict:
        url = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json'
        return requests.get(url).json()

    @staticmethod
    def _parse_hugovk(dataset: Dataset, data: dict):
        # hugovk datasets provide names and download counts
        dataset.projects = [Project(package_name=r['project'])
                            for r in data['rows']]
