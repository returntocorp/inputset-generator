from structures import Dataset
from loaders import Loader


class PypiLoader(Loader):
    @classmethod
    def weblists(cls):
        return {
            'top5kmonth': {
                'getter': PypiLoader._get_top5kmonth,
                'parser': PypiLoader._parse_hugovk
            },
            'top5kyear': {
                'getter': PypiLoader._get_top5kyear,
                'parser': PypiLoader._parse_hugovk
            }
        }

    @classmethod
    def load(cls, name: str, **kwargs) -> Dataset:
        # initialize a registry
        ds = Dataset(**kwargs)

        # load the data
        data = cls.weblists()[name]['getter'](api=ds.api, **kwargs)

        # parse the data
        cls.weblists()[name]['parser'](ds, data)

        return ds

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


