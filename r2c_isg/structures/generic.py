from dataclasses import dataclass
from typing import Optional

from structures.core import Project, Version
from util import get_str


@dataclass
class GenericVersion(Version):

    @property
    def version(self) -> Optional[str]:
        return get_str('version', self.data) or None


@dataclass
class GenericProject(Project):

    @property
    def name(self) -> Optional[str]:
        return get_str('name', self.data) or None

    @property
    def url(self) -> Optional[str]:
        return get_str('url', self.data) or None

    def to_inputset(self, include_invalid: bool = False) -> list:
        if not self.url and not include_invalid:
            # skip this project
            # TODO: log a warning...
            return []

        return [{
            'input_type': 'HttpUrl',
            'url': self.url,
        }]
