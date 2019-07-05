from structures.projects import Project


class NpmPackage(Project):
    def to_inputset(self) -> list:
        """Converts npm packages/versions to a list of input set dicts."""
        temp = 5
