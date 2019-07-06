from structures.projects import Project
from structures.versions import NpmVersion


class NpmPackage(Project):
    _url_format = 'https://www.npmjs.com/package/%s'
    _apiurl_format = 'https://registry.npmjs.com/%s'

    def update(self, data: dict) -> None:
        # The npm api provides package/version data in a combined json;
        # filter out the version info and initialize them separately
        version_data = (
            data.pop('_versions', None) or  # keyword for json/csv
            data.pop('versions', [])        # keyword for npm api
        )

        super().update(data)

        # add any versions to the package
        self.versions = []#NpmVersion(**d) for d in version_data]

    def check_guarantees(self):
        """A NpmPackage is guaranteed to contain *at least* a name, a
        package url, or an api url. Any one of these items can be used
        to determine the other two as needed via the get_ functions."""
        if not (self._name or self._url or self._apiurl):
            raise Exception('Package name, url, or api url '
                            'must be provided.')

    def get_name(self) -> str:
        if not self._name:
            # extract name from url/api url
            self._name = (self._url or self._apiurl).split('/')[-1]
        return self._name

    def get_url(self) -> str:
        if not self._url:
            # calculate url from name
            self._url = NpmPackage._url_format % self.get_name()
        return self._url

    def get_apiurl(self) -> str:
        if not self._apiurl:
            # calculate api url from org & name
            self._apiurl = NpmPackage._apiurl_format % self.get_name()
        return self._apiurl

    def to_inputset(self) -> list:
        """Converts npm packages/versions to PackageVersion dict."""
        temp = 5
