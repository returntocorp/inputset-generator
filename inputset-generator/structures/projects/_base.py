from typing import List

from structures.versions import Version


class Project:
    def __init__(self, **kwargs):
        # load all attributes into the project
        self.update(kwargs)

        # a project contains versions
        self.versions: List[Version] = []

        # project data guarantees
        self.meta_name = None
        self.meta_url = None
        self.meta_apiurl = None

    def update(self, data: dict) -> None:
        """Populates the project with data from a dictionary."""
        for k, val in data.items():
            setattr(self, k, val)

    def get_name(self):
        pass

    def get_url(self):
        pass

    def get_apiurl(self):
        pass

    def find_version(self, **kwargs):
        """Gets a version matching all parameters or returns None."""

        # linear search function; potential for being slow...
        for v in self.versions:
            match = True
            for param, val in kwargs.items():
                if getattr(v, param, None) != val:
                    match = False
                    break
            if match:
                return v

        return None

    def find_or_add_version(self, version_cls, **kwargs):
        """Finds a matching version or adds a new one of type Version."""
        version = self.find_version(**kwargs)
        if not version:
            version = version_cls(**kwargs)
            self.versions.append(version)

        return version

    def to_inputset(self) -> list:
        """Converts noreg projects/versions to a list of input set dicts."""
        temp = 5

    def __repr__(self):
        return 'Project(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
