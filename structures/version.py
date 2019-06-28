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
        return 'Version(%s)' % (self.version or self.commit)

    def __str__(self):
        return repr(self)
