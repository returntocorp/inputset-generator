from types import MethodType


class Version(object):
    def __init__(self, uuids_: dict = {}, meta_: dict = {}, **kwargs):
        # set the uuid/meta functions as method types (to autopass self)
        self.uuids_ = {}
        for attr, func in uuids_.items():
            self.uuids_[attr] = MethodType(func, self)
        self.meta_ = {}
        for attr, func in meta_.items():
            self.meta_[attr] = MethodType(func, self)

        # load all attributes into the version
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        """Populates the version with data from a dictionary."""
        for k, val in kwargs.items():
            setattr(self, k, val)

        # make sure all guarantees are met
        self.check_guarantees()

    def check_guarantees(self) -> None:
        """Guarantees nothing (vanilla Version knows nothing about its
        contents)."""
        pass

    def to_inputset(self) -> dict:
        """Extracts input set relevant attributes from the version."""
        # Note: The vanilla project is never used, even as a DefaultVersion.
        # As such, this function should never be called. Instead, it's
        # effectively an abstract method that child classes must implement.
        raise Exception('Version class has no associated R2C input set type.')

    def __eq__(self, other):
        # the two versions are equal if one of the uuids matches
        for k, val in self.uuids_.items():
            if val() == other.uuids_[k]():
                return True
        return False

    def __repr__(self):
        # only return version identifiers
        cls = str(type(self).__name__)
        uuids = [str(func()) for _, func in self.uuids_.items()]
        return '%s(%s)' % (cls, ', '.join(uuids))
