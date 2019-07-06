import requests

from structures import Dataset
from loaders import Loader


class GithubLoader(Loader):
    def __init__(self):
        self.weblists = {
            'top100starred': {
                'getter': self._get_top1kstarred,
                'parser': self._parse_github
            },
            'top100forked': {
                'getter': self._get_top1kforked,
                'parser': self._parse_github
            }

        }

    def load(self, ds: Dataset, name: str, **_) -> None:
        # load the data
        data = self.weblists[name]['getter']()

        # parse the data
        self.weblists[name]['parser'](ds, data)

    @staticmethod
    def _get_top1kstarred() -> list:
        # url courtesy of: https://stackoverflow.com/questions/19855552/
        # how-to-find-out-the-most-popular-repositories-on-github
        url = 'https://api.github.com/search/repositories?' \
              'q=stars%%3A>0&sort=stars&per_page=100&page=%d'

        # results are limited to 100 per page; load & merge 10 pages
        projects = []
        for u in [(url % d) for d in range(1, 2)]:
            projects += requests.get(u).json()['items']

        return projects

    @staticmethod
    def _get_top1kforked() -> list:
        # url courtesy of: https://stackoverflow.com/questions/19855552/
        # how-to-find-out-the-most-popular-repositories-on-github
        url = 'https://api.github.com/search/repositories?' \
              'q=forks%%3A>0&sort=forks&per_page=100&page=%d'

        # results are limited to 100 per page; load & merge 10 pages
        projects = []
        for u in [(url % d) for d in range(1, 2)]:
            projects += requests.get(u).json()['items']

        return projects

    @staticmethod
    def _parse_github(ds: Dataset, data: list):
        from structures.projects import GithubRepo

        ds.projects = [GithubRepo(**d) for d in data]
