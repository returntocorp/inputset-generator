from tqdm import tqdm

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset


class NpmLoader(Loader):
    @classmethod
    def weblists(cls) -> dict:
        """
        Other possible sources/useful links:
        - Realtime list of the top 108 most depended-upon packages:
          https://www.npmjs.com/browse/depended

        - List of the top 1k most depended upon, most dependencies, and
          highest PageRank score packages as of December 2018:
          https://gist.github.com/anvaka/8e8fa57c7ee1350e3491

        - Other projects by nice-registry:
          https://github.com/nice-registry/ghub.io
          https://github.com/nice-registry/nice-package
          https://github.com/nice-registry/all-the-package-repos

        - Discussions of npm api options:
          https://stackoverflow.com/questions/34071621/query-npmjs-registry-via-api
          https://stackoverflow.com/questions/48251633/list-all-public-packages-in-the-npm-registry
        """

        return {
            'allbydependents': {
                'getter': NpmLoader._get_allbydependents,
                'parser': NpmLoader._parse_niceregistry
            }
        }

    @classmethod
    def load(cls, weblist: str, **kwargs) -> Dataset:
        # initialize a registry
        ds = Dataset(**kwargs)

        # select the correct weblist loader/parser
        weblists = cls.weblists()
        if weblist not in weblists:
            raise Exception('Unrecognized npm weblist name. Valid '
                            'options are: %s' % list(weblists))

        # load the data
        data = weblists[weblist]['getter'](api=ds.api, **kwargs)

        # parse the data
        weblists[weblist]['parser'](ds, data)

        return ds

    @staticmethod
    def _get_allbydependents(api, **kwargs) -> list:
        url = 'https://github.com/nice-registry/all-the-package-names/raw/master/names.json'

        status, data = api.request(url, **kwargs)
        if status != 200:
            raise Exception('Error downloading %s; '
                            'is the url accessible?' % url)

        return data

    @staticmethod
    def _parse_niceregistry(ds: Dataset, data: list):
        from r2c_isg.structures.projects import NpmPackage

        # map data keys to package keywords
        uuids = {
            'name': lambda p: p.name
        }

        # create the projects
        # Note: data list is ordered from most dependents to fewest
        ds.projects = [NpmPackage(uuids_=uuids, **{
            'name': d,
            'dependents_rank': i + 1  # package with rank 1 has the most dependents
        }) for i, d in enumerate(tqdm(data, desc='         Loading',
                                      unit='project', leave=False))]

    '''
    @staticmethod
    def _get_[incomplete--see problem in approach #4](api, **kwargs) -> list:
        """
        Approach:
        1. Download list of all 1.02M NPM packages from npmjs.

        2. Split list into scoped packages (names contain a '/') and
           non-scoped packages

        3. Request non-scoped packages from npmjs downloads endpoint
           (128/request; ~6,700 requests). Mark 'source' in all packages
           as 'npmjs'.

        4. Request the 172k scoped packages from npms.io (250/request;
           ~700 requests). Mark 'source' in all packages as 'npms.io'.

           Problem: npmjs includes new packages that npms.io has not yet
           found. When npms.io is asked for packages it doesn't have, it
           responds with a 500 internal server error, but does not list
           the offending package, making it practically impossible to
           determine *which* package was the problem (short of using
           some sort of tree search). An issue has been submitted; see:
           https://github.com/npms-io/npms-api/issues/88

        5. Combine and return the two lists.

        6. When parsing, use the 'source' attribute to determine how to
           handle the data (npms.io returns a lot more data than npm).
        """

        # load a list of projects
        url = 'https://replicate.npmjs.com/_all_docs'
        package_list = api.request(url, **kwargs)['rows']

        packages = []

        # GET FROM NPMJS API...
        for start_at in range(0, len(package_list), 128):
            # build the bulk request to the npm downloads count endpoint
            # Note: Up to 128 packages may be requested at a time. See:
            # https://github.com/npm/registry/blob/master/docs/download-counts.md#limits
            names = ','.join([
                p['id'] for p in package_list[start_at: start_at + 128]
            ])
            url = 'https://api.npmjs.org/downloads/point/last-month/%s' % names

            # submit the request
            data = api.request(url, **kwargs)

            # add the response data to the list of packages
            packages.extend(list(data.values()))

        # ...OR GET FROM NPMS.IO API
        for start_at in range(0, len(package_list), 250):
            # build a mget (multiple get) request to the npms.io api
            # Note: Up to 250 packages may be requested at a time.
            # api docs at: https://api-docs.npms.io/
            url = 'https://api.npms.io/v2/package/mget'

            # overwrite any headers/data attrs in kwargs
            h_args = {'content-type': 'application/json'}
            d_args = [p['id'] for p in package_list[start_at: start_at + 250]]

            # one month cache timeout, as it's thousands of requests otherwise
            timeout = timedelta(weeks=4)

            # submit the request
            data = api.request(url, request_type='post', cache_timeout=timeout,
                               headers=h_args, data=d_args, **kwargs)

            # add the response data to the list of packages
            packages.extend(list(data.values()))

        return packages
    '''
