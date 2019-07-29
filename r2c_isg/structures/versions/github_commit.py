from r2c_isg.structures.versions import Version


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
