from registries import Registry
from structures import Project


class Npm(Registry):
    def __init__(self):
        super().__init__()

        # set project registry name and url format
        self.name = 'npm'
        self.url_format = '???'

        # add pypi-specific weblists
        # try this? https://www.npmjs.com/browse/depended
        # https://stackoverflow.com/questions/34071621/query-npmjs-registry-via-api
        # https://github.com/npm/download-counts
        # https://registry.npmjs.org/lodash
        self.loaders = {
            '???': {
                'url': '???',
                'parser': 'self._???'
            }
        }

    def load_project_metadata(self, project: Project) -> None:
        pass

    def load_project_versions(self, project: Project,
                              historical: str = 'all') -> None:
        pass
