from dataclasses import dataclass
from typing import Optional

from structures.core import Project, Version
from util import get_str, name_from_url, url_from_name


@dataclass
class GithubCommit(Version):

    @property
    def commit(self) -> Optional[str]:
        return (
            get_str('commit', self.data)
            or get_str('sha', self.metadata)
        ) or None


@dataclass
class GithubRepo(Project):

    @property
    def url(self) -> Optional[str]:
        url_literal = 'https://github.com/{name}'

        org = get_str('org', self.data)
        name = get_str('name', self.data)
        data_fullname = f'{org}/{name}' if org and name else ''

        meta_fullname = get_str('full_name', self.metadata)

        return (
            get_str('url', self.data)
            or url_from_name(name, url_literal) if '/' in name else None
            or url_from_name(data_fullname, url_literal)
            or get_str('html_url', self.metadata)
            or url_from_name(meta_fullname, url_literal)
        ) or None

    @property
    def full_name(self) -> Optional[str]:
        pattern: str = r'^.*github.com/(?P<name>[\w-]+/[\w-]+).*$'

        org = get_str('org', self.data)
        name = get_str('name', self.data)
        data_fullname = f'{org}/{name}' if org and name else None

        data_url = get_str('url', self.data)
        meta_url = get_str('html_url', self.metadata)

        return (
            name if '/' in name else None
            or data_fullname
            or name_from_url(data_url, pattern)
            or get_str('full_name', self.metadata)
            or name_from_url(meta_url, pattern)
        ) or None

    def to_inputset(self, include_invalid: bool = False) -> list:
        if not self.url and not include_invalid:
            # skip this project
            # TODO: log a warning...
            return []

        if not self.versions:
            return [{
                'input_type': 'GitRepo',
                'repo_url': self.url,
            }]

        inputs = []
        for v in self.versions:
            if not isinstance(v, GithubCommit):
                # version is wrong object type
                # TODO: log an exception...
                continue

            if not v.commit and not include_invalid:
                # skip this version
                # TODO: log a warning...
                continue

            inputs.append({
                'input_type': 'GitRepoCommit',
                'repo_url': self.url,
                'commit_hash': v.commit,
            })

        return inputs
