from structures.projects import Project


class PypiProject(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name or a url."""
        assert 'name' in self.uuids_ or 'url' in self.uuids_, \
            'Project name or url must be provided.'

    def to_inputset(self) -> list:
        """Converts pypi projects/releases to PackageVersion dict."""
        assert self.versions, ('Pypi project must contain at least one '
                               'release before exporting to an input set.')

        if 'name' in self.uuids_:
            name = self.uuids_['name']()
        else:
            # pull the name from the url
            name = self.uuids_['url']().strip('/').split('/')[-1]

        ret = []
        for v in self.versions:
            ret.append({
                'input_type': 'PackageVersion',
                'package_name': name,
                'version': v.uuids_['version']()
            })

        return ret
