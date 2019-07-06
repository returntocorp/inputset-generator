from structures.projects import Project
from structures.versions import PypiRelease


class PypiProject(Project):
    _url_format = 'https://pypi.org/project/%s'
    _apiurl_format = 'https://pypi.org/pypi/%s/json'

    def update(self, **kwargs) -> None:
        # The pypi api provides package/version data in a combined json;
        # filter out the version info and initialize them separately
        version_data = (
            kwargs.pop('_versions', None) or  # keyword for json/csv
            kwargs.pop('releases', [])        # keyword for pypi api
        )

        super().update(**kwargs)

        # add any versions to the package
        self.versions = [PypiRelease(**d) for d in version_data]

    def check_guarantees(self):
        """A PypiProject is guaranteed to contain *at least* a name, a
        project url, or an api url. Any one of these items can be used
        to determine the other two as needed via the get_ functions."""
        if not (self._name or self._url or self._apiurl):
            raise Exception('Project name, url, or api url '
                            'must be provided.')

    def get_name(self) -> str:
        if not self._name:
            # extract name from url/api url
            if self._url:
                self._name = self._url.split('/')[-1]
            else:
                self._name = self._apiurl.split('/')[-2]

        return self._name

    def get_url(self) -> str:
        if not self._url:
            # calculate url from name
            self._url = PypiProject._url_format % self.get_name()
        return self._url

    def get_apiurl(self) -> str:
        if not self._apiurl:
            # calculate api url from org & name
            self._apiurl = PypiProject._apiurl_format % self.get_name()
        return self._apiurl

    def to_inputset(self) -> list:
        """Converts pypi projects/releases to PackageVersion dict."""
        temp = 5
