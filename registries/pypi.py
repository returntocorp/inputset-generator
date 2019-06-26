import requests

from .abstract import Registry, Project


class PypiRegistry(Registry):
    name = 'pypi'
    url_format = 'https://pypi.python.org/pypi/%s/json'

    def sort(self, args):
        pass

    def get_meta(self):
        pass

    def get_versions(self):
        pass

    def load_file(self, path: str):
        pass

    def _parse_hugovk(self, data: dict):
        # hugovk datasets provide names and download counts
        self.projects = [Project(r['project']) for r in data['rows']]

    weblists = {
        '5k30days': {
            'url': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json',
            'parser': _parse_hugovk
        },
        '5kyear': {
            'url': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json',
            'parser': _parse_hugovk
        }
    }

    def load_weblist(self, name: str):
        weblist = self.weblists[name]
        r = requests.get(weblist['url'])
        d = weblist['parser'](self, r.json())
