from tqdm import tqdm

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset


class PypiLoader(Loader):
    @classmethod
    def weblists(cls) -> dict:
        return {
            'top4kmonth': {
                'getter': PypiLoader._get_top4kmonth,
                'parser': PypiLoader._parse_hugovk
            },
            'top4kyear': {
                'getter': PypiLoader._get_top4kyear,
                'parser': PypiLoader._parse_hugovk
            }
        }

    @classmethod
    def load(cls, name: str, **kwargs) -> Dataset:
        # get the request type (weblist vs. organization)
        from_type = kwargs.pop('from_type')
        if from_type == 'org':
            raise Exception('Pypi does not support loading project lists from org names.')

        # initialize a registry
        ds = Dataset(**kwargs)

        # select the correct weblist loader/parser
        weblists = cls.weblists()
        if name not in weblists:
            raise Exception('Unrecognized pypi weblist name. Valid '
                            'options are: %s' % list(weblists))

        # load the data
        data = weblists[name]['getter'](api=ds.api, **kwargs)

        # parse the data
        weblists[name]['parser'](ds, data)

        return ds

    @staticmethod
    def _get_top4kmonth(api, **kwargs) -> list:
        url = 'https://hugovk.github.io/top-pypi-packages/' \
              'top-pypi-packages-30-days.json'

        status, data = api.request(url, **kwargs)
        if status != 200:
            raise Exception('Error downloading %s; is the url accessible?', url)

        return data['rows']

    @staticmethod
    def _get_top4kyear(api, **kwargs) -> list:
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


