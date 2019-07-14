from structures.projects import Project


class GithubRepo(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name/org or a url."""
        assert ('url' in self.uuids_ or (
                'name' in self.uuids_ and 'org' in self.meta_)
                ), 'Repo name/org or url must be provided.'

    def to_inputset(self) -> list:
        """Converts github repos/commits to GitRepo/GitRepoCommit dict."""

        if 'url' in self.uuids_:
            url = self.uuids_['url']()
        else:
            # generate the url using the name/org
            url = 'https://github.com/%s/%s' % (self.meta_['org'](),
                                                self.uuids_['name']())

        if len(self.versions) == 0:
            # return input set type GitRepo
            return [{
                'input_type': 'GitRepo',
                'repo_url': url
            }]

        # return input set type GitRepoCommit
        ret = []
        for v in self.versions:
            ret.append({
                'input_type': 'GitRepoCommit',
                'repo_url': url,
                'commit_hash': v.uuids_['commit']()
            })

        return ret
