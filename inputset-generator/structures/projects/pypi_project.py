from structures.projects import Project


class PypiProject(Project):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        tmp = 5


    def to_inputset(self) -> list:
        """Converts pypi projects/releases to a list of input set dicts."""
        temp = 5

