from structures.projects import Project


class DefaultProject(Project):
    def check_guarantees(self) -> None:
        """Guarantees a url."""
        if 'url' not in self.uuids_:
            raise Exception('Project url must be provided.')

    def to_inputset(self) -> list:
        """Converts default project to HttpUrl dict."""
        return [{
            'input_type': 'HttpUrl',
            'url': self.uuids_['url']()
        }]
