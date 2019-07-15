from structures.versions import Version


class PypiRelease(Version):
    def check_guarantees(self) -> None:
        """Guarantees a version string."""
        assert 'version' in self.uuids_, \
            'Release version string must be provided.'

    def to_inputset(self) -> dict:
        self.check_guarantees()
        return {'version': self.uuids_['version']()}
