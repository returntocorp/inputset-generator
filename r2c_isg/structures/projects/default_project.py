from r2c_isg.structures.projects import Project


class DefaultProject(Project):
    def check_guarantees(self) -> None:
        """Guarantees a url."""
        assert 'url' in self.uuids_, \
            'Default project guarantees not met; ' \
            'project url must be provided.'

    def to_inputset(self) -> list:
        """Converts default project to HttpUrl dict."""
        self.check_guarantees()
        return [{
            'input_type': 'HttpUrl',
            'url': self.uuids_['url']()
        }]
