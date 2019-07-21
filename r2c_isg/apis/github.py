from typing import Optional, Union
from itertools import count
from tqdm import tqdm

from r2c_isg.apis import Api
from r2c_isg.structures.projects import GithubRepo
from r2c_isg.structures.versions import GithubCommit


class Github(Api):
    def __init__(self, **kwargs):
        # set base url for github's api
        self._base_api_url = 'https://api.github.com'

        # set the default github personal access token
        self.github_pat = None

        super().__init__(**kwargs)

    def update(self, **kwargs):
        """Populates the github api with data from a dictionary."""
        super().update(**kwargs)

        # set the personal access token
        self.github_pat = kwargs.pop('github_pat', None) or self.github_pat

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
                        'You can provide a github personal access token '
                        '(using the command "set-api --github_pat TOKEN") to '
                        'obtain a significantly higher request rate limit. '
                        'See instructions at https://help.github.com/en/'
                        'articles/creating-a-personal-access-token-for-'
                        'the-command-line.'
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
            print(' ' * 9 + 'Warning: Unexpected response from github api '
                            '(HTTP %d); failed to retrieve metadata for %s.'
                  % (status, project.get_name()))
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
        desc = '             %s' % project.get_name()
        iterator = tqdm(count(start=1), leave=False, unit='page', desc=desc)
        for i in iterator:
            # load the url from cache or from the web
            url = '%s/commits?page=%d' % (api_url, i)
            status, data = self.request(url, **kwargs)
            i += 1

            # skip this page if non-200 response
            if status != 200:
                print(' ' * 9 + 'Warning: Unexpected response from github '
                      'api (HTTP %d); failed to retrieve some of the versions '
                      'of %s (%s).' % (status, project.get_name(), url))
                continue

            if not data:
                # no more pages; break
                iterator.close()
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

            if historical == 'latest':
                # stop after the first page of results
                iterator.close()
                break
