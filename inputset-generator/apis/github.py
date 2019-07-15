from typing import Optional, Union

from apis import Api
from structures.projects import GithubRepo
from structures.versions import GithubCommit


class Github(Api):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set base url for github's api
        self._base_api_url = 'https://api.github.com'

        # set the personal access token
        self.github_pat = kwargs.get('github_pat', None)

    def request(self, url: str, headers: dict = {},
                **kwargs) -> (int, Optional[Union[dict, list]]):
        """Manages API rate limitations before calling super().request()."""

        # add github personal access token to request headers
        if self.github_pat:
            headers['Authorization'] = 'token %s' % self.github_pat

        # get the response code/data
        status, data = super().request(url, headers=headers, **kwargs)

        # Note: Github's api limits requests to 5,000/hour if the
        # requester is authenticated, and 60/hour if not. See:
        # https://developer.github.com/v3/#rate-limiting
        if self._base_api_url in url:
            if status == 401:
                # invalid personal access token--critical error
                raise Exception('Incorrect/invalid personal access token. '
                                'Please double check your token and try again')
            elif status == 403:
                # rate limiting--critical error
                raise Exception(
                    'The github api is limiting your request rate (HTTP %d). '
                    '%s' % (
                        status,
                        'Please try again in an hour.' if self.github_pat else
                        'Provide a github personal access token to obtain '
                        'a higher request rate limit.'
                    ))

        return status, data

    def _make_api_url(self, project: GithubRepo) -> str:
        if 'name' in project.uuids_ and 'org' in project.meta_:
            name = project.uuids_['name']()
            org = project.meta_['org']()

        else:
            # extract the name/org from the url
            url = project.uuids_['url']()
            name = project.get_name()
            org = url.strip('/').split('/')[-2]

        return '%s/repos/%s/%s' % (self._base_api_url, org, name)

    def get_project(self, project: GithubRepo, **kwargs) -> None:
        """Gets a repo's metadata."""

        # load the url from cache or the web
        url = self._make_api_url(project)
        status, data = self.request(url, **kwargs)

        # skip this project if non-200 response (just return now)
        if status != 200:
            print('Warning: Unexpected response from github api (HTTP %d); '
                  'failed to retrieve metadata for %s.' % (status,
                                                           project.get_name()))
            return

        # the 'url' key actually relates to the api; indicate as much
        data['api_url'] = data.pop('url')

        # update the project
        project.update(**data)

    def get_versions(self, project: GithubRepo,
                     historical: str = 'all', **kwargs) -> None:
        """Gets a commit's historical releases."""

        # github commit json is paginated--30 commits per page
        api_url = self._make_api_url(project)
        end_page = 1 if historical == 'latest' else 999999
        for i in range(1, end_page + 1):
            # load the url from cache or from the web
            url = '%s/commits?page=%d' % (api_url, i)
            status, data = self.request(url, **kwargs)

            # skip this page if non-200 response
            if status != 200:
                print('Warning: Unexpected response from pypi api (HTTP '
                      '%d); failed to retrieve some of the versions of '
                      '%s (%s).' % (status, project.get_name(), url))
                continue

            if not data:
                # no more pages; break
                break

            if historical == 'latest':
                # trim the new versions data to the latest commit only
                data = data[:1]

            for v_data in data:
                commit = project.find_version(**v_data)
                if historical == 'latest':
                    # trim existing commits to the latest commit only
                    project.versions = [commit] if commit else []

                if commit:
                    # update the existing commit
                    commit.update(**v_data)

                else:
                    # create a new commit
                    uuids = {
                        'commit': lambda v: v.sha
                    }
                    commit = GithubCommit(uuids_=uuids, **v_data)
                    project.versions.append(commit)
