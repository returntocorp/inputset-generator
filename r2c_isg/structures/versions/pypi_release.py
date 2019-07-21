from r2c_isg.structures.versions import Version


class PypiRelease(Version):
    def check_guarantees(self) -> None:
        """Guarantees a version string."""
        assert 'version' in self.uuids_, \
            'Pypi release guarantees not met; ' \
            'version string must be provided.'

    def to_inputset(self) -> dict:
        """Extracts input set relevant attributes from the release."""
        self.check_guarantees()
        return {'version': self.uuids_['version']()}
