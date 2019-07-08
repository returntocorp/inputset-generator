from structures.projects import Project


class PypiProject(Project):
    def to_inputset(self) -> list:
        """Converts pypi projects/releases to PackageVersion dict."""
        temp = 5
