from typing import Union

from apis import Api
from structures.projects import NpmPackage
from structures.versions import NpmVersion


class Npm(Api):
    @property
    def _base_api_url(self):
        return 'https://registry.npmjs.com'

    def request(self, url, **kwargs) -> Union[dict, list]:
        """Manages API rate limitations before calling super().request()."""

        # Note: The npm registry json api states that rate limiting is
        # in effect, but only publicizes the limits for the download
        # counts endpoint, which we do not use. Consequently, no rate
        # limitation have been implemented here. See:
        # https://blog.npmjs.org/post/164799520460/api-rate-limiting-rolling-out#_=
        # https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
        # https://github.com/renovatebot/renovate/issues/754
        if self._base_api_url in url:
            # implement any internal rate limiting here...
            pass

        return super().request(url, **kwargs)

    @staticmethod
    def _make_api_url(project: NpmPackage) -> str:
        # get the package name and convert to api url
        if 'name' in project.uuids_:
            name = project.uuids_['name']()

        else:
            # extract the name from the url
            name = project.uuids_['url']().strip('/').split('/')[-1]

        return '%s/%s' % (Npm._base_api_url, name)

    def get_project(self, project: NpmPackage, **kwargs) -> None:
        """Gets a package's metadata."""

        # load the url from cache or the web
        url = self._make_api_url(project)
        data = self.request(url, **kwargs)

        # ignore version-related data
        data.pop('versions')

        # update the project
        project.update(**data)

    def get_versions(self, project: NpmPackage,
                     historical: str = 'all', **kwargs) -> None:
        """Gets a version's historical releases."""

        # load the url from cache or from the web
        url = self._make_api_url(project)
        data = self.request(url, **kwargs)
        versions = data['versions']

        if historical == 'latest':
            # trim the new versions data to the latest version only
            latest_key = data['dist-tags']['latest']
            versions = {latest_key: versions[latest_key]}

        for _, v_data in versions.items():
            version = project.find_version(**v_data)
            if historical == 'latest':
                # trim existing versions to the version release only
                project.versions = [version] if version else []

            if version:
                # update the existing version
                version.update(**v_data)

            else:
                # create a new version
                uuids = {
                    'version': lambda v: v.version
                }
                version = NpmVersion(uuids_=uuids, **v_data)
                project.versions.append(version)
