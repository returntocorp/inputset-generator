import re
from dataclasses import dataclass
from typing import Optional

from structures.core import Project, Version


@dataclass
class NpmVersion(Version):

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('version')


@dataclass
class NpmPackage(Project):

    def _name_from_url(self):
        url = self._get_metadata('url') or ''

        url_pattern = r'^.*npmjs.com/package/(?P<name>[\w-]+).*$'
        match = re.match(url_pattern, url)

        return match['name'] if match else None

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('name') or self._name_from_url()

    def to_inputset(self) -> dict:
        url = f'https://npmjs.com/package/{self.id}'
        pass
