from registries import Registry
from structures import Dataset, Project


class PypiRegistry(Registry):
    def __init__(self):
        super().__init__()

        # set project registry name and url format
        self.name = 'pypi'
        self.url_format = 'https://pypi.python.org/pypi/%s/json'

        # add pypi-specific weblists
        self.weblists.update({
            '5k30days': {
                'url': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json',
                'parser': self._parse_hugovk
            },
            '5kyear': {
                'url': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json',
                'parser': self._parse_hugovk
            }
        })

    def get_meta(self, project: Project):
        pass

    def get_versions(self, project: Project):
        pass

    @staticmethod
    def _parse_hugovk(dataset: Dataset, data: dict):
        # hugovk datasets provide names and download counts
        dataset.projects = [Project(package_name=r['project'])
                            for r in data['rows']]
