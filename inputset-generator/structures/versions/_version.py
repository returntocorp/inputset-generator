from types import MethodType


class Version:
    def __init__(self, uuids_: dict = {}, **kwargs):
        # set the attr functions as method types (to autopass self)
        self.uuids_ = {}
        for attr, func in uuids_.items():
            self.uuids_[attr] = MethodType(func, self)

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

    def __eq__(self, other):
        # the two versions are equal if one of the uuids matches
        for k, val in self.uuids_.items():
            if val() == other.uuids_[k]():
                return True
        return False

    def __repr__(self):
        # only return version identifiers
        return 'Version(%s)' % ', '.join([
            '%s' % func() for k, func in self.uuids_.items()
        ])
