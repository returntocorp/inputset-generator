from structures.versions import Version


class NpmVersion(Version):
    def check_guarantees(self) -> None:
        """Guarantees a version string."""
        assert 'version' in self.uuids_, \
            'Version string must be provided.'
