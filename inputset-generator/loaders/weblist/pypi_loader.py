import requests

from structures import Dataset
from loaders import Loader


class PypiLoader(Loader):
    def __init__(self):
        self.weblists = {
            'top5kmonth': {
                'getter': self._get_top5kmonth,
                'parser': self._parse_hugovk
            },
            'top5kyear': {
                'getter': self._get_top5kyear,
                'parser': self._parse_hugovk
            }
        }

    def load(self, ds: Dataset, name: str, **kwargs) -> None:
        # load the data
        data = self.weblists[name]['getter'](api=ds.api, **kwargs)

        # parse the data
        self.weblists[name]['parser'](ds, data)

    @staticmethod
    def _get_top5kyear(api, **kwargs) -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-365-days.json'
        return api.request(url, **kwargs)['rows']

    @staticmethod
    def _get_top5kmonth(api, **kwargs) -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-30-days.json'
        return api.request(url, **kwargs)['rows']

    @staticmethod
    def _parse_hugovk(ds: Dataset, data: list) -> None:
        from structures.projects import PypiProject

        # map data keys to project keywords
        uuids = {
            'name': lambda p: p.project
        }

        # create the projects
        ds.projects = [PypiProject(uuids_=uuids, **d) for d in data]
