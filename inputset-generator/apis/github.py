import os
from typing import Union

from apis import Api
from structures.projects import GithubRepo
from structures.versions import GithubCommit


class Github(Api):
    def request(self, url: str, **_) -> Union[dict, list]:
        """Manages API rate limitations before calling super().request()."""

        # Note: Github's api limits requests to 5,000/hour if the
        # requester is authenticated, and 60/hour if not. See:
        # https://developer.github.com/v3/#rate-limiting

        # add github personal access token to header
        github_pat = os.getenv('github_pat')
        return super().request(url, Authorization='token %s' % github_pat)

    @staticmethod
    def _make_api_url(project: GithubRepo) -> str:
        if 'name' in project.meta_ and 'org' in project.meta_:
            name = project.meta_['name']()
            org = project.meta_['org']()

        else:
            # extract the name/org from the url
            url = project.meta_['url']()
            name = url.strip('/').split('/')[-1]
            org = url.strip('/').split('/')[-2]

        return 'https://api.github.com/repos/%s/%s' % (org, name)

    def get_project(self, project: GithubRepo) -> None:
        """Gets a repo's metadata."""

        # load the url from cache or the web
        data = self.request(self._make_api_url(project))

        # the 'url' key actually relates to the api; indicate as much
        data['api_url'] = data.pop('url')

        # update the project
        project.update(**data)

    def get_versions(self, project: GithubRepo, hist: str = 'all') -> None:
        """Gets a commit's historical releases."""

        # github commit json is paginated--30 commits per page
        api_url = self._make_api_url(project)
        for i in range(1, 99999999):
            # load the url from cache or from the web
            data = self.request('%s/commits?page=%d' % (api_url, i))
            if not data:
                # no more pages; break
                break

            for v_data in data:
                commit = project.find_version(**v_data)
                if not commit:
                    # create a new commit
                    meta = {
                        'commit': lambda v: v.sha
                    }
                    commit = GithubCommit(meta_=meta, **v_data)
                    project.versions.append(commit)

                else:
                    # update the existing commit
                    commit.update(**v_data)
