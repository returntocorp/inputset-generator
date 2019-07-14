from structures.versions import Version


class GithubCommit(Version):
    def check_guarantees(self) -> None:
        """Guarantees a commit hash."""
        assert 'commit' in self.uuids_, 'Commit hash must be provided.'
