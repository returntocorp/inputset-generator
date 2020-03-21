from dataclasses import dataclass, field
from typing import Optional

from structures.core import Project, Version
from util import get_str, name_from_url, url_from_name


@dataclass(eq=False)
class NpmVersion(Version):

    def get_ids(self) -> dict:
        ids = dict()
        if self.version:
            ids['version'] = self.version
        return ids

    @property
    def version(self) -> Optional[str]:
        return (
            get_str('version', self.data)
            or get_str('version', self.metadata)
        ) or None

    version: str = field(default=version, init=False)


@dataclass(eq=False)
class NpmPackage(Project):

    def get_ids(self) -> dict:
        ids = dict()
        if self.name:
            ids['name'] = self.name
        if self.url:
            ids['url'] = self.url
        return ids

    @property
    def name(self) -> Optional[str]:
        pattern = r'^.*npmjs.com/package/(?P<name>[\w-]+).*$'

        return (
            get_str('name', self.data)
            or name_from_url(get_str('url', self.data), pattern)
            or get_str('name', self.metadata)
        ) or None

    name: str = field(default=name, init=False)

    @property
    def url(self) -> Optional[str]:
        url_literal = 'https://npmjs.com/package/{name}'

        return (
            get_str('url', self.data)
            or url_from_name(get_str('name', self.data), url_literal)
            or url_from_name(get_str('name', self.metadata), url_literal)
        ) or None

    url: str = field(default=url, init=False)

    def to_inputset(self, include_invalid: bool = False) -> list:
        if not self.name and not include_invalid:
            # skip this project
            # TODO: log a warning...
            return []

        inputs = []
        for v in self.versions:
            if not isinstance(v, NpmVersion):
                # version is wrong object type
                # TODO: log an exception...
                continue

            if not v.version and not include_invalid:
                # skip this version
                # TODO: log a warning...
                continue

            inputs.append({
                'input_type': 'PackageVersion',
                'package_name': self.name,
                'version': v.version,
            })

        return inputs
