class Version:
    def __init__(self, **kwargs):
        """ The init function first checks if any child class has set a
        '_[name]' variable. Failing that, it looks for json/csv keywords
        for name ('name', 'package_name'), url ('url', 'repo_url'), and
        api url ('api_url')."""

        '''
        self._version = (
            kwargs.get('_name', None) or      # if set by caller
            kwargs.get('name', None) or       # keyword for csv
            kwargs.get('package_name', None)  # keyword for json
        )
        self._url = (
            kwargs.get('_url', None) or   # if set by caller
            kwargs.get('url', None) or    # keyword for csv & some json
            kwargs.get('repo_url', None)  # keyword for other json
        )
        '''

        # load all attributes into the project
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        """Populates the version with data from a dictionary."""
        for k, val in kwargs.items():
            setattr(self, k, val)

    def __repr__(self):
        return 'Version(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
