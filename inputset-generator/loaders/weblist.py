from structures import Dataset
from loaders import Loader


class Weblist(Loader):
    def __init__(self):
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

    @staticmethod
    def _load_top5kyear() -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-365-days.json'
        return requests.get(url).json()['rows']

    @staticmethod
    def _load_top5kmonth() -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-30-days.json'
        return requests.get(url).json()['rows']

    @staticmethod
    def _parse_hugovk(ds: Dataset, data: list) -> None:
        Project = ds.types['project']
        ds.projects = [Project(package_name=d['project'],
                               downloads=d['download_count'])
                       for d in data]
