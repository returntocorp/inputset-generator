from structures.versions import Version


class PypiRelease(Version):
    def check_guarantees(self) -> None:
        """Guarantees a version string."""
        if 'version' not in self.uuids_:
            raise Exception('Release version string must be provided.')
