from typing import Optional, Union

from apis import Api
from structures.projects import NpmPackage
from structures.versions import NpmVersion


class Npm(Api):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set the base url for npm's api
        self._base_api_url = 'https://registry.npmjs.com'

    def request(self, url, **kwargs) -> (int, Optional[Union[dict, list]]):
        """Manages API rate limitations before calling super().request()."""

        # get the response code/data
        status, data = super().request(url, **kwargs)

        # Note: The npm registry json api states that rate limiting is
        # in effect, and the api will return a 429 code if you send too
        # many requests. It only publicizes the limits for the download
        # counts endpoint though, which we do not use. Consequently, we
        # can't take any proactive measures; we can only tell the user
        # if they've been rate limited after the fact. See:
        # https://blog.npmjs.org/post/164799520460/api-rate-limiting-rolling-out#_=
        # https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
        # https://github.com/renovatebot/renovate/issues/754
        if self._base_api_url in url:
            # rate limiting--critical error
            if status == 429:
                raise Exception('The npm registry is limiting your request rate'
                                ' (HTTP %d). Please try again later.' % status)

        return status, data

    def _make_api_url(self, project: NpmPackage) -> str:
        # get the package name and convert to api url
        if 'name' in project.uuids_:
            name = project.uuids_['name']()

        else:
            # extract the name from the url
            name = project.uuids_['url']().strip('/').split('/')[-1]

        return '%s/%s' % (self._base_api_url, name)

    def get_project(self, project: NpmPackage, **kwargs) -> None:
        """Gets a package's metadata."""

        # load the url from cache or the web
        url = self._make_api_url(project)
        status, data = self.request(url, **kwargs)

        # skip this project if non-200 response (just return now)
        if status != 200:
            uuid = project.uuids_.get('name', None) or \
                   project.uuids_.get('url', None)
            print('Warning: Unexpected response from npm registry (HTTP %d); '
                  'failed to retrieve metadata for %s.' % (status, uuid()))
            return

        # ignore version-related data
        data.pop('versions')

        # update the project
        project.update(**data)

    def get_versions(self, project: NpmPackage,
                     historical: str = 'all', **kwargs) -> None:
        """Gets a version's historical releases."""

        # load the url from cache or from the web
        url = self._make_api_url(project)
        status, data = self.request(url, **kwargs)

        # skip this project if non-200 response (just return now)
        if status != 200:
            uuid = project.uuids_.get('name', None) or \
                   project.uuids_.get('url', None)
            print('Warning: Unexpected response from npm registry (HTTP %d); '
                  'failed to retrieve versions for %s.' % (status, uuid()))
            return

        # get the versions list from the data
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
