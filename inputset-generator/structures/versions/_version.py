from types import MethodType


class Version:
    def __init__(self, meta_: dict = {}, **kwargs):
        # set the attr functions as method types (to autopass self)
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

    def __eq__(self, other):
        # the two versions are equal if one of the uuids matches
        for k, val in self.meta_.items():
            if val() == other.meta_[k]():
                return True
        return False

    def __repr__(self):
        # only return version identifiers
        return 'Version(%s' % ', '.join([
            '%s=%s' % (k, func()) for k, func in self.meta_.items()
        ]) + ', [...])'
