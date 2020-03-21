from dataclasses import dataclass, field
from typing import Optional

from structures.core import Project, Version
from util import get_str


@dataclass(eq=False)
class GenericVersion(Version):

    def get_ids(self) -> dict:
        ids = dict()
        if self.version:
            ids['version'] = self.version
        return ids

    @property
    def version(self) -> Optional[str]:
        return get_str('version', self.data) or None

    version: str = field(default=version, init=False)


@dataclass(eq=False)
class GenericProject(Project):

    def get_ids(self) -> dict:
        ids = dict()
        if self.name:
            ids['name'] = self.name
        if self.url:
            ids['url'] = self.url
        return ids

    @property
    def name(self) -> Optional[str]:
        return get_str('name', self.data) or None

    name: str = field(default=name, init=False)

    @property
    def url(self) -> Optional[str]:
        return get_str('url', self.data) or None

    url: str = field(default=url, init=False)

    def to_inputset(self, include_invalid: bool = False) -> list:
        if not self.url and not include_invalid:
            # skip this project
            # TODO: log a warning...
            return []

        return [{
            'input_type': 'HttpUrl',
            'url': self.url,
        }]
