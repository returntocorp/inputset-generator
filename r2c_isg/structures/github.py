from r2c_isg.structures.core import Project, Version


class GithubCommit(Version):
    def check_guarantees(self) -> None:
        """Guarantees a commit hash."""
        assert 'commit' in self.uuids_, \
            'Github commit guarantees not met; ' \
            'commit hash must be provided.'

    def to_inputset(self) -> dict:
        """Extracts input set relevant attributes from the commit."""
        self.check_guarantees()
        return {'commit_hash': self.uuids_['commit']()}


class GithubRepo(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name/org or a url."""
        assert ('url' in self.uuids_ or (
                'name' in self.uuids_ and 'org' in self.meta_)
                ), 'Github repo guarantees not met; name/org or ' \
                   'url must be provided.'

    def get_name(self) -> str:
        """Returns the project's name."""
        if 'name' in self.uuids_:
            return self.uuids_['name']()

        # pull the name from the url
        return self.uuids_['url']().strip('/').split('/')[-1]

    def to_inputset(self) -> list:
        """Converts github repos/commits to GitRepo/GitRepoCommit dict."""
        self.check_guarantees()

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
        return[{
            'input_type': 'GitRepoCommit',
            'repo_url': url,
            **v.to_inputset()
        } for v in self.versions]
