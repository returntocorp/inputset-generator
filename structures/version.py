class Version:
    def __init__(self, **kwargs):
        self.version = None
        self.commit = None

        # caller must provide a version string or commit hash
        if not ('version' in kwargs or 'commit' in kwargs):
            raise Exception('Version must have a version or commit')

        # load all attributes into the version
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
