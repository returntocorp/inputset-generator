from tqdm import tqdm

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset


class PypiLoader(Loader):
    @classmethod
    def weblists(cls) -> dict:
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
    def load(cls, weblist: str, **kwargs) -> Dataset:
        # initialize a registry
        ds = Dataset(**kwargs)

        # select the correct weblist loader/parser
        weblists = cls.weblists()
        if weblist not in weblists:
            raise Exception('Unrecognized pypi weblist name. Valid '
                            'options are: %s' % list(weblists))

        # load the data
        data = weblists[weblist]['getter'](api=ds.api, **kwargs)

        # parse the data
        weblists[weblist]['parser'](ds, data)

        return ds

    @staticmethod
    def _get_top5kmonth(api, **kwargs) -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-30-days.json'

        status, data = api.request(url, **kwargs)
        if status != 200:
            raise Exception('Error downloading %s; is the url accessible?', url)

        return data['rows']

    @staticmethod
    def _get_top5kyear(api, **kwargs) -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-365-days.json'

        status, data = api.request(url, **kwargs)
        if status != 200:
            raise Exception('Error downloading %s; '
                            'is the url accessible?' % url)

        return data['rows']

    @staticmethod
    def _parse_hugovk(ds: Dataset, data: list) -> None:
        from r2c_isg.structures.projects import PypiProject

        # map data keys to project keywords
        uuids = {
            'name': lambda p: p.project
        }

        # create the projects
        ds.projects = [PypiProject(uuids_=uuids, **d)
                       for d in tqdm(data, desc='         Loading',
                                     unit='project', leave=False)]


