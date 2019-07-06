class Version:
    def __init__(self, **kwargs):
        """ The init function first checks if any child class has set a
        '_[name]' variable. Failing that, it looks for json/csv keywords
        for version string ('version_string', 'version') and commit hash
        ('commit_hash')."""

        self._version_string = (
            kwargs.get('_version_str', None) or    # if set by caller
            kwargs.get('version_string', None) or  # keyword for csv
            kwargs.get('version', None)            # keyword for json
        )
        self._commit_hash = (
            kwargs.get('_commit_hash', None) or  # if set by caller
            kwargs.get('commit_hash', None)      # keyword for csv/json
        )

        # load all attributes into the version
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        """Populates the version with data from a dictionary."""
        for k, val in kwargs.items():
            setattr(self, k, val)

        # make sure all guarantees are met
        self.check_guarantees()

    def check_guarantees(self):
        """A vanilla Version is guaranteed to contain *at least* a
        version string or a commit hash."""
        if not (self._version_string or self._commit_hash):
            raise Exception('Version string or commit hash'
                            'must be provided.')

    def __repr__(self):
        return 'Version(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
