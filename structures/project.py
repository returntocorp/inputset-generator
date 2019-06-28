from typing import List

from structures import Version


class Project:
    def __init__(self, name: str = '', url: str = ''):
        # must have a name or url
        if not (name or url):
            raise Exception('Project must have a name or url.')

        self.name = name
        self.url = url

        self.versions: List[Version] = []
