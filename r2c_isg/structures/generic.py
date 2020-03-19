from dataclasses import dataclass
from typing import Optional

from structures.core import Project, Version


@dataclass
class GenericVersion(Version):

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('version')


@dataclass
class GenericProject(Project):

    @property
    def id(self) -> Optional[str]:
        return self._get_metadata('name') or self._get_metadata('url')

    def to_inputset(self) -> dict:
        pass
