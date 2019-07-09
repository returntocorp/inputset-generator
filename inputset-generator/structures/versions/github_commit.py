from structures.versions import Version


class GithubCommit(Version):
    def check_guarantees(self) -> None:
        """Guarantees a commit hash."""
        if 'commit' not in self.uuids_:
            raise Exception('Commit hash must be provided.')
