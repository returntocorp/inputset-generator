import re
from dataclasses import dataclass
from typing import Optional

from structures.core import Project, Version


@dataclass
class GithubCommit(Version):

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('sha')


@dataclass
class GithubRepo(Project):

    def _name_from_url(self):
        url = self._get_metadata('html_url') or ''

        url_pattern = r'^.*github.com/(?P<name>[\w-]+/[\w-]+).*$'
        match = re.match(url_pattern, url)

        return match['name'] if match else None

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('full_name') or self._name_from_url() or super().id

    def to_inputset(self) -> dict:
        url = f'https://github.com/{self.id}'
        pass
