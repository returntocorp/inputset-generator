from typing import List, Optional
from types import MethodType

from structures.versions import Version


class Project:
    def __init__(self, meta_: dict = {}, **kwargs):
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

        # build a temporary project containing the kwargs
        this_v = Version(**kwargs)

        # linear search function for now; potentially quite slow...
        for other_v in self.versions:
            # copy over the other project's meta lambda funcs so the two
            # projects can be compared (need to rebind the lambda func
            # to this_p instead of other_p--hence the __func__ ref)
            for k, func in other_v.meta_.items():
                this_v.meta_[k] = MethodType(func.__func__, this_v)

            if this_v == other_v:
                return other_v

        return None

    def to_inputset(self) -> list:
        """Vanilla project can't be converted to an r2c input set."""
        raise Exception('Project class has no associated R2C input set type.')

    def __eq__(self, other):
        # the two projects are equal if one of the uuids matches
        for k, val in self.meta_.items():
            if val() == other.meta_[k]():
                return True
        return False

    def __repr__(self):
        # only return project identifiers
        return 'Project(%s' % ', '.join([
            '%s=%s' % (k, func()) for k, func in self.meta_.items()
        ]) + ', versions=[%s], ...)' % ('...' if self.versions else '')
