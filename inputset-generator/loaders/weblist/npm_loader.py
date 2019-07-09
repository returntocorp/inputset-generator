from structures import Dataset
from loaders import Loader


class NpmLoader(Loader):
    def __init__(self):
        # add npm-specific weblists
        # try this? https://www.npmjs.com/browse/depended
        # https://stackoverflow.com/questions/34071621/query-npmjs-registry-via-api
        # https://github.com/npm/download-counts
        # https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md#get-v1search
        # https://stackoverflow.com/questions/48251633/list-all-public-packages-in-the-npm-registry

        # idea: hit the /all endpoint to download all packages, then hit
        # the /downloads/point with a comma-separated list of packages
        # to get the downloads count?
        # https://replicate.npmjs.com/_all_docs
        # https://api.npmjs.org/downloads/point/last-year/npm,express,lodash,requests,bob
        self.weblists = {}

    def load(self, ds: Dataset, name: str, **_) -> None:
        # load the data
        data = self.weblists[name]['getter'](api=ds.api)

        # parse the data
        self.weblists[name]['parser'](ds, data)
