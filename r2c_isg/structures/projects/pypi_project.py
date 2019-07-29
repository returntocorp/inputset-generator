from r2c_isg.structures.projects import Project


class PypiProject(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name or a url."""
        assert 'name' in self.uuids_ or 'url' in self.uuids_, \
            'Pypi project guarantees not met; project name or ' \
            'url must be provided.'

    def get_name(self) -> str:
        """Returns the project's name."""
        if 'name' in self.uuids_:
            return self.uuids_['name']()

        # pull the name from the url
        return self.uuids_['url']().strip('/').split('/')[-1]

    def to_inputset(self) -> list:
        """Converts pypi projects/releases to PackageVersion dict."""
        self.check_guarantees()

        if not self.versions:
            raise Exception('Pypi project %s must contain at least one '
                            'version before it can be exported to an '
                            'input set.' % self.get_name())

        return [{
            'input_type': 'PackageVersion',
            'package_name': self.get_name(),
            **v.to_inputset()
        } for v in self.versions]
