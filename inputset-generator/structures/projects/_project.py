from typing import List, Optional
from types import MethodType

from structures.versions import Version


class Project:
    def __init__(self, meta_: dict = None, **kwargs):
        # a project contains versions
        self.versions: List[Version] = []

        # set the attr functions as method types (to autopass self)
        self.meta_ = {}
        for attr, func in meta_.items():
            self.meta_[attr] = MethodType(func, self)

        # load all attributes into the project
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        """Populates the project with data from a dictionary."""
        for k, val in kwargs.items():
            setattr(self, k, val)

        # make sure all guarantees are met
        self.check_guarantees()

    def check_guarantees(self) -> None:
        """Guarantees nothing (vanilla Project knows nothing about its
        contents)."""
        pass

    def find_version(self, **kwargs) -> Optional[Version]:
        """Gets a version matching all kwargs or returns None."""

        # linear search function for now; potentially quite slow...
        for v in self.versions:
            match = True
            for param, val in kwargs.items():
                if getattr(v, param, None) != val:
                    match = False
                    break
            if match:
                return v

        return None

    def to_inputset(self) -> list:
        """Vanilla project can't be converted to an r2c input set."""
        raise Exception('Project class has no associated R2C input set type.')

    def __repr__(self):
        return 'Project(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
