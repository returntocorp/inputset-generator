from structures import Dataset
from loaders import Loader


class NpmLoader(Loader):
    def __init__(self):
        # add pypi-specific weblists
        # try this? https://www.npmjs.com/browse/depended
        # https://stackoverflow.com/questions/34071621/query-npmjs-registry-via-api
        # https://github.com/npm/download-counts
        # https://registry.npmjs.org/lodash
        self.weblists = {}
