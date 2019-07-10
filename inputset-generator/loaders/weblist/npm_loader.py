from structures import Dataset
from loaders import Loader


class NpmLoader(Loader):
    def __init__(self):
        self.weblists = {
            'allbydownloads': {
                'getter': self._get_allbydownloads,
                'parser': self._parse_npm
            }
        }

    def load(self, ds: Dataset, name: str, **kwargs) -> None:
        # load the data
        data = self.weblists[name]['getter'](api=ds.api, **kwargs)

        # parse the data
        self.weblists[name]['parser'](ds, data)

    @staticmethod
    def _get_allbydownloads(api, **kwargs) -> list:
        # load a list of projects
        url = 'https://replicate.npmjs.com/_all_docs'
        package_list = api.request(url, **kwargs)['rows']

        # get the downloads count
        packages = []
        for start_at in range(0, len(package_list), 128):
            # build the bulk request to the downloads count endpoint
            # Note: Up to 128 packages may be requested at a time. See:
            # https://github.com/npm/registry/blob/master/docs/download-counts.md#limits
            names = ','.join([
                p['id'] for p in package_list[start_at: start_at + 128]
            ])
            url = 'https://api.npmjs.org/downloads/point/last-month/%s' % names

            # request the data from the api (cache/web)
            data_dict = api.request(url, **kwargs)
            packages.extend(list(data_dict.values()))

        return packages

    # https://api-docs.npms.io/
    # https://www.npmjs.com/browse/depended
    # https://github.com/npm/download-counts
    # https://gist.github.com/anvaka/8e8fa57c7ee1350e3491
    # https://stackoverflow.com/questions/34071621/query-npmjs-registry-via-api
    # https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md#get-v1search
    # https://stackoverflow.com/questions/48251633/list-all-public-packages-in-the-npm-registry

    @staticmethod
    def _parse_npm(ds: Dataset, data: list):
        from structures.projects import NpmPackage

        # map data keys to package keywords
        uuids = {
            'name': lambda p: p.package
        }

        # create the projects
        ds.projects = [NpmPackage(uuids_=uuids, **d) for d in data]
