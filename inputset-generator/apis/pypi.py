from typing import Union

from apis import Api
from structures.projects import PypiProject
from structures.versions import PypiRelease


class Pypi(Api):
    def request(self, url: str, **_) -> Union[dict, list]:
        """Manages API rate limitations before calling super().request()."""

        # Note: The pypi json api does not currently have any sort of
        # rate limiting policies in effect. See:
        # https://warehouse.readthedocs.io/api-reference/#rate-limiting

        return super().request(url)

    @staticmethod
    def _make_api_url(project: PypiProject) -> str:
        # get the package name and convert to api url
        if 'name' in project.meta_:
            name = project.meta_['name']()

        else:
            # extract the name from the url
            name = project.meta_['url']().strip('/').split('/')[-2]

        return 'https://pypi.org/pypi/%s/json' % name

    def get_project(self, project: PypiProject) -> None:
        """Gets a project's metadata."""

        # load the url from cache or the web
        data = self.request(self._make_api_url(project))

        # ignore version-related data
        data.pop('releases')

        # break out the contents of the 'info' dict
        data.update(data.pop('info'))

        # update the project
        project.update(**data)

    def get_versions(self, project: PypiProject, hist: str = 'all') -> None:
        """Gets a project's historical releases."""

        # load the url from cache or from the web
        data = self.request(self._make_api_url(project))

        for v_str, v_data in data['releases'].items():
            # Note: The pypi api returns versions as a dict mapping of
            # version strings to lists of dicts of versions (ie, a single
            # release could have more than one release in a version; eg,
            # a tar.gz and a wheel dist). For now, we'll just take the
            # first dict in the list.
            if v_data:
                v_data = v_data[0]
            else:
                # some releases are missing all info other than their
                # version string
                v_data = {}

            # add the version string to the data dict
            v_data['version'] = v_str

            # add the data to the version
            release = project.find_version(**v_data)
            if not release:
                # create a new release
                meta = {
                    'version': lambda v: v.version
                }
                release = PypiRelease(meta_=meta, **v_data)
                project.versions.append(release)

            else:
                # update the existing release
                release.update(**v_data)
