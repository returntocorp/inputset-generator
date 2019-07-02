from pydriller import RepositoryMining

from registries import Registry
from structures import Dataset, Project


class GithubRegistry(Registry):
    def __init__(self):
        super().__init__()

        self.name = 'github'
        self.url_format = 'https://github.com/%s/%s'
        self.weblists = {
            'top1kstarred': {
                'loader': self._load_top1kstarred,
                'parser': self._parse_github
            }
        }
        # more: https://stackoverflow.com/questions/19855552/how-to-find-out-the-most-popular-repositories-on-github

    def load_project_metadata(self, project: Project) -> None:
        """Retrieves all project data from github."""

        # get the project url or organization/name
        url = getattr(project, 'repo_url', None)
        org = getattr(project, 'organization', None)
        name = getattr(project, 'name', None)
        if not url and not (org and name):
            raise Exception('Error loading project details. Project '
                            "must have attribute 'repo_url' or "
                            "attributes 'name' and 'organization'.")

        # download the project info from github
        repo = RepositoryMining(url or self.url_format % (org, name))

        temp = 5


        # https://buildmedia.readthedocs.org/media/pdf/pydriller/latest/pydriller.pdf
        # RepositoryMining('https://github.com/pigigaldi/Pock').traverse_commits()

        # Note: need to define repo_url
        temp = 5

    def load_project_versions(self, project: Project,
                              historical: str = 'all') -> None:
        """Retrieves all version data from github."""

        # Note: need to define commit_hash
        # add versions to the project (overwrite any existing versions)
        project.versions = []


        temp = 5

        # filter the versions based on historical flag
        hist_types = ['latest', 'tagged', 'all']
        if historical not in hist_types:
            raise Exception("Unrecognized historical selection '%s'. "
                            "Valid selections are: %s" % (historical,
                                                          str(hist_types)))

        # Todo: Complete historical version filtering.

    def _load_top1kstarred() -> dict:
        url = 'https://api.github.com/search/repositories?q=stars%3A%3E0&sort=stars&per_page=100'
        pass

    def _parse_github(ds: Dataset, data: dict):
        pass
