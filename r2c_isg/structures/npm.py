from r2c_isg.structures.core import Project, Version


class NpmVersion(Version):
    def check_guarantees(self) -> None:
        """Guarantees a version string."""
        assert 'version' in self.uuids_, \
            'Npm version guarantees not met; ' \
            'version string must be provided.'

    def to_inputset(self) -> dict:
        """Extracts input set relevant attributes from the version."""
        self.check_guarantees()
        return {'version': self.uuids_['version']()}


class NpmPackage(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name or a url."""
        assert 'name' in self.uuids_ or 'url' in self.uuids_, \
            'Npm package guarantees not met; package name or ' \
            'url must be provided.'

    def get_name(self) -> str:
        """Returns the project's name."""
        if 'name' in self.uuids_:
            return self.uuids_['name']()

        # pull the name from the url
        return self.uuids_['url']().strip('/').split('/')[-1]

    def to_inputset(self) -> list:
        """Converts npm packages/versions to PackageVersion dict."""
        self.check_guarantees()

        if not self.versions:
            raise Exception('Npm package %s must contain at least one '
                            'version before it can be exported to an '
                            'input set.' % self.get_name())

        return[{
            'input_type': 'PackageVersion',
            'package_name': self.get_name(),
            **v.to_inputset()
        } for v in self.versions]
