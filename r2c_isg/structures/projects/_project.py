from typing import List, Optional
from types import MethodType

from r2c_isg.structures.versions import Version


class Project(object):
    def __init__(self, uuids_: dict = {}, meta_: dict = {}, **kwargs):
        # a project contains versions
        self.versions: List[Version] = []

        # set the uuid/meta functions as method types (to autopass self)
        self.uuids_ = {}
        for attr, func in uuids_.items():
            self.uuids_[attr] = MethodType(func, self)
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

    def get_name(self) -> str:
        """Returns the project's name."""
        # child functions can override this to calculate the name--
        # eg, extracting it from a url
        return self.uuids_.get('name', '')

    def find_version(self, **kwargs) -> Optional[Version]:
        """Gets a version matching all kwargs or returns None."""

        # build a temporary project containing the kwargs
        this_v = Version(**kwargs)

        # linear search function for now; potentially quite slow...
        for other_v in self.versions:
            # copy over the other project's uuid lambda funcs so the two
            # projects can be compared (need to rebind the lambda func
            # to this_p instead of other_p--hence the __func__ ref)
            for k, func in other_v.uuids_.items():
                this_v.uuids_[k] = MethodType(func.__func__, this_v)

            if this_v == other_v:
                return other_v

        return None

    def to_inputset(self) -> list:
        """Vanilla project can't be converted to an r2c input set."""
        # Note: The only time a vanilla Project is used is in the function
        # Dataset.find_project(), which never calls to_inputset(). As such,
        # this function should never be called. Instead, it's effectively
        # an abstract method that child classes must implement.
        raise Exception('Project class has no associated R2C input set type.')

    def __eq__(self, other):
        # the two projects are equal if one of the uuids matches
        for k, val in self.uuids_.items():
            if val() == other.uuids_[k]():
                return True
        return False

    def __repr__(self):
        # only return project identifiers
        cls = str(type(self).__name__)
        uuids = [str(func()) for _, func in self.uuids_.items()]
        versions = [repr(v) for v in self.versions]
        return '%s(%s, versions=[%s])' % (cls,
                                          ', '.join(uuids),
                                          ', '.join(versions))
