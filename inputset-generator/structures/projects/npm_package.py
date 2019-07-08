from structures.projects import Project


class NpmPackage(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name or a url."""
        if 'name' not in self.meta_ and 'url' not in self.meta_:
            raise Exception('Package name or url must be provided.')

    def to_inputset(self) -> list:
        """Converts npm packages/versions to PackageVersion dict."""
        if not self.versions:
            raise Exception('Npm package must have at least one version.')

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
