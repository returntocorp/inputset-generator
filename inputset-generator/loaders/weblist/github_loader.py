from structures import Dataset
from loaders import Loader


class GithubLoader(Loader):
    @classmethod
    def weblists(cls):
        return {
            'top1kstarred': {
                'getter': GithubLoader._get_top1kstarred,
                'parser': GithubLoader._parse_github
            },
            'top1kforked': {
                'getter': GithubLoader._get_top1kforked,
                'parser': GithubLoader._parse_github
            }
        }

    @classmethod
    def load(cls, weblist: str, **kwargs) -> Dataset:
        # initialize a registry
        ds = Dataset(**kwargs)

        # load the data
        data = cls.weblists()[weblist]['getter'](api=ds.api, **kwargs)

        # parse the data
        cls.weblists()[weblist]['parser'](ds, data)

        return ds

    @staticmethod
    def _get_top1kstarred(api, **kwargs) -> list:
        # url courtesy of: https://stackoverflow.com/questions/19855552/
        # how-to-find-out-the-most-popular-repositories-on-github
        url_format = 'https://api.github.com/search/repositories?' \
                     'q=stars%%3A>0&sort=stars&per_page=100&page=%d'

        # github limits results to the top 1k at 100 per page
        projects = []
        for url in [(url_format % d) for d in range(1, 11)]:
            # request the data via the github api
            status, data = api.request(url, **kwargs)
            assert status == 200, 'Error downloading %s; is the url accessible?'

            projects.extend(data['items'])

        return projects

    @staticmethod
    def _get_top1kforked(api, **kwargs) -> list:
        # url courtesy of: https://stackoverflow.com/questions/19855552/
        # how-to-find-out-the-most-popular-repositories-on-github
        url_format = 'https://api.github.com/search/repositories?' \
                     'q=forks%%3A>0&sort=forks&per_page=100&page=%d'

        # github limits results to the top 1k at 100 per page
        projects = []
        for url in [(url_format % d) for d in range(1, 11)]:
            # request the data via the github api
            status, data = api.request(url, **kwargs)
            assert status == 200, 'Error downloading %s; is the url accessible?'

            projects.extend(data['items'])

        return projects

    @staticmethod
    def _parse_github(ds: Dataset, data: list) -> None:
        from structures.projects import GithubRepo

        # map data keys to project keywords
        uuids = {
            'name': lambda p: p.name,
            'url': lambda p: p.html_url
        }
        meta = {
            'org': lambda p: p.url.split('/')[-2],
        }

        # create the projects
        ds.projects = [GithubRepo(uuids_=uuids, meta_=meta, **d) for d in data]
