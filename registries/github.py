from registries import Registry
from structures import Dataset, Project


class GithubRegistry(Registry):
    def __init__(self):
        super().__init__()

        # set project registry name and url format
        self.name = 'github'
        self.url_format = '???'

        # add pypi-specific weblists
        # see: https://stackoverflow.com/questions/19855552/how-to-find-out-the-most-popular-repositories-on-github
        self.loaders = {
            '1kstarred': {
                'url': 'https://api.github.com/search/repositories?q=stars%3A%3E0&sort=stars&per_page=100',
                'parser': 'self._???'
            }
        }

    def get_meta(self, project: Project):
        pass

    def get_versions(self, project: Project):
        pass
