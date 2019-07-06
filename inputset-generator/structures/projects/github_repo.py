from structures.projects import Project


class GithubRepo(Project):
    _url_format = 'https://github.com/%s/%s'
    _apiurl_format = 'https://api.github.com/repos/%s/%s'

    def __init__(self, **kwargs):
        # GithubRepo also recognizes the '_org'/'organization' keywords
        self._org = (
            kwargs.get('_org', None) or       # if set by caller
            kwargs.get('organization', None)  # keyword for csv
        )

        # The Project init assumes the 'url' key relates to the project
        # url, but if the data came from the github api, that value
        # relates to the api url instead, and the repo url is stored as
        # 'html_url'. Preempt that confusion by adding a '_url' keyword
        # to the kwargs if the 'html_url' keyword exists.
        html_url = kwargs.get('html_url', None)
        if html_url:
            kwargs['_url'] = kwargs.get('html_url', None)

        super().__init__(**kwargs)

    def check_guarantees(self):
        """A GithubRepo is guaranteed to contain *at least* a name and
        organization name, a repo url, or an api url. Any one of these
        functions can be used to determine the other two as needed via
        the get_ functions."""
        if not ((self._org and self._name) or self._url or self._apiurl):
            raise Exception('Repo name/org, url, or api url '
                            'must be provided.')

    def get_name(self) -> str:
        if not self._name:
            # extract name from url/api url
            self._name = (self._url or self._apiurl).split('/')[-1]
        return self._name

    def get_org(self) -> str:
        if not self._org:
            # extract org name from url/api url
            self._org = (self._url or self._apiurl).split('/')[-2]
        return self._org

    def get_url(self) -> str:
        if not self._url:
            # calculate url from org & name
            self._url = GithubRepo._url_format % (self.get_org(),
                                                  self.get_name())
        return self._url

    def get_apiurl(self) -> str:
        if not self._apiurl:
            # calculate api url from org & name
            self._apiurl = GithubRepo._apiurl_format % (self.get_org(),
                                                        self.get_name())
        return self._apiurl

    def to_inputset(self) -> list:
        """Converts github repos/commits to GitRepo/GitRepoCommit dict."""
        lst = []

        if len(self.versions) > 0:
            # return input set type GitRepoCommit
            pass

        else:
            # return input set type GitRepo
            pass

        return lst
