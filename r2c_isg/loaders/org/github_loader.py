from tqdm import tqdm

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset


class GithubLoader(Loader):
    @classmethod
    def load(cls, org_name: str, **kwargs) -> Dataset:
        from r2c_isg.structures.projects import GithubRepo

        # initialize a dataset
        ds = Dataset(**kwargs)

        def load_url(url, api) -> dict:
            status, data = api.request(url)
            if status != 200:
                print('         Error downloading %s; is the url accessible?', url)
                return []

            return data

        # load the (paginated) list of repos for this organization
        all_data = []
        url = 'https://api.github.com/users/%s/repos?page=' % org_name
        page_num = 1
        while True:
            data = load_url(url + str(page_num), ds.api)
            all_data.extend(data)
            page_num += 1

            if len(data) == 0:
                break

        # map data keys to project keywords
        uuids = {
            'name': lambda p: p.name,
            'url': lambda p: p.html_url
        }
        meta = {
            'org': lambda p: p.url.split('/')[-2],
        }

        # create the projects
        ds.projects = [GithubRepo(uuids_=uuids, meta_=meta, **d)
                       for d in tqdm(all_data, desc='         Loading',
                                     unit='project', leave=False)]

        return ds
