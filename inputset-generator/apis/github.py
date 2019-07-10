import os
from typing import Union

from apis import Api
from structures.projects import GithubRepo
from structures.versions import GithubCommit


class Github(Api):
    def request(self, url: str, headers: dict = {}, **kwargs) -> Union[dict, list]:
        """Manages API rate limitations before calling super().request()."""

        # Note: Github's api limits requests to 5,000/hour if the
        # requester is authenticated, and 60/hour if not. See:
        # https://developer.github.com/v3/#rate-limiting

        # add github personal access token to request headers
        github_pat = os.getenv('github_pat')
        headers['Authorization'] = 'token %s' % github_pat

        return super().request(url, headers=headers, **kwargs)

    @staticmethod
    def _make_api_url(project: GithubRepo) -> str:
        if 'name' in project.uuids_ and 'org' in project.meta_:
            name = project.uuids_['name']()
            org = project.meta_['org']()

        else:
            # extract the name/org from the url
            url = project.uuids_['url']()
            name = url.strip('/').split('/')[-1]
            org = url.strip('/').split('/')[-2]

        return 'https://api.github.com/repos/%s/%s' % (org, name)

    def get_project(self, project: GithubRepo, **kwargs) -> None:
        """Gets a repo's metadata."""

        # load the url from cache or the web
        url = self._make_api_url(project)
        data = self.request(url, **kwargs)

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
            data = self.request(url, **kwargs)
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
