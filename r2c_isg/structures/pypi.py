import re
from dataclasses import dataclass
from typing import Optional

from structures.core import Project, Version


@dataclass
class PypiRelease(Version):

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('version')


@dataclass
class PypiProject(Project):

    def _name_from_url(self):
        url = self._get_metadata('project_url') or ''

        url_pattern = r'^.*pypi.org/project/(?P<name>[\w-]+).*$'
        match = re.match(url_pattern, url)

        return match['name'] if match else None

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('name') or self._name_from_url()

    def to_inputset(self) -> dict:
        url = f'https://pypi.org/project/{self.id}'
        pass
