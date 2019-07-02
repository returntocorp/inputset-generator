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

    def load_details(self, project: Project) -> None:
        """Retrieves all project data from the registry."""

        # get the project info
        name = getattr(project, 'package_name')
        data = requests.get(self.url_format % name).json()

        # ignore version-level data
        data.pop('releases')

        # populate the project with the remaining data
        # break out info dict for easier sort
        info = data.pop('info')
        data.update(info)
        project.populate(data)

    def load_versions(self, project: Project, historical: str = 'all') -> None:
        """Retrieves all version data from the registry."""

        # get the versions list
        name = getattr(project, 'package_name')
        data = requests.get(self.url_format % name).json()
        version_data = data.get('releases')

        # add versions to the project (overwrite any existing versions)
        # NOTE: Pypi occasionally has versions with multiple releases.
        # This appears to be due to having a whl and tar.gz distribution
        # of the same release. For now, just take the first release.
        project.versions = []
        for version_str, data in version_data.items():
            kwargs = {'version': version_str}
            if len(data) > 0:
                kwargs.update(data[0])
            version = project._get_or_add_version(**kwargs)
            version.historical = version_str

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
