from structures.projects import Project


class NpmPackage(Project):
    def to_inputset(self) -> list:
        """Converts npm packages/versions to PackageVersion dict."""
        temp = 5
