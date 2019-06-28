from typing import List

from .version import Version


class Project:
    def __init__(self, name: str = '', url: str = ''):
        # must have a name or url
        if not (name or url):
            raise Exception('Project must have a name or url.')

        self.name = name
        self.url = url

        self.versions: List[Version] = []

    def get_version(self, params: dict):
        pass
