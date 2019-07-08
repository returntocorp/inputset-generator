from structures.projects import Project


class PypiProject(Project):
    def check_guarantees(self) -> None:
        """Guarantees a name or a url."""
        if 'name' not in self.meta_ and 'url' not in self.meta_:
            raise Exception('Project name or url must be provided.')

    def to_inputset(self) -> list:
        """Converts pypi projects/releases to PackageVersion dict."""
        temp = 5
