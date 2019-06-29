from registries import Registry
from structures import Dataset, Project


class NpmRegistry(Registry):
    def __init__(self):
        super().__init__()

        # set project registry name and url format
        self.name = 'npm'
        self.url_format = '???'

        # add pypi-specific weblists
        self.loaders = {
            '???': {
                'url': '???',
                'parser': 'self._???'
            }
        }

    def get_meta(self, project: Project):
        pass

    def get_versions(self, project: Project):
        pass
