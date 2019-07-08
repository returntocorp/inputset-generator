from structures.projects import Project


class PypiProject(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name or a url."""
        if 'name' not in self.meta_ and 'url' not in self.meta_:
            raise Exception('Project name or url must be provided.')

    def to_inputset(self) -> list:
        """Converts pypi projects/releases to PackageVersion dict."""
        if not self.versions:
            raise Exception('Pypi project must have at least one release.')

        if 'name' in self.meta_:
            name = self.meta_['name']()
        else:
            # pull the name from the url
            name = self.meta_['url']().strip('/').split('/')[-1]

        ret = []
        for v in self.versions:
            ret.append({
                'input_type': 'PackageVersion',
                'package_name': name,
                'version': v.meta_['version']()
            })

        return ret
