from typing import List

from structures.versions import Version


class Project:
    def __init__(self, **kwargs):
        # a project contains versions
        self.versions: List[Version] = []

        """ The init function first checks if any child class has set a
        '_[name]' variable. Failing that, it looks for json/csv keywords
        for name ('name', 'package_name'), url ('url', 'repo_url'), and
        api url ('api_url')."""

        self._name = (
            kwargs.get('_name', None) or      # if set by caller
            kwargs.get('name', None) or       # keyword for csv
            kwargs.get('package_name', None)  # keyword for json
        )
        self._url = (
            kwargs.get('_url', None) or   # if set by caller
            kwargs.get('url', None) or    # keyword for csv & some json
            kwargs.get('repo_url', None)  # keyword for other json
        )
        self._apiurl = (
            kwargs.get('_apiurl', None) or  # if set by caller
            kwargs.get('api_url', None)     # keyword for csv
        )

        # load all attributes into the project
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        """Populates the project with data from a dictionary."""
        for k, val in kwargs.items():
            setattr(self, k, val)

        # make sure all guarantees are met
        self.check_guarantees()

    def check_guarantees(self):
        """A vanilla Project is guaranteed to contain *at least* a name
        or a url. """
        if not (self._name or self._url):
            raise Exception('Project name or url must be provided.')

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_apiurl(self):
        return self._apiurl

    '''
    def find_version(self, **kwargs):
        """Gets a version matching all parameters or returns None."""

        # linear search function; potential for being slow...
        for v in self.versions:
            match = True
            for param, val in kwargs.items():
                if getattr(v, param, None) != val:
                    match = False
                    break
            if match:
                return v

        return None

    def find_or_add_version(self, version_cls, **kwargs):
        """Finds a matching version or adds a new one of type Version."""
        version = self.find_version(**kwargs)
        if not version:
            version = version_cls(**kwargs)
            self.versions.append(version)

        return version
    '''

    def to_inputset(self) -> list:
        """Converts vanilla projects/versions to HttpUrl dict."""
        temp = 5

    def __repr__(self):
        return 'Project(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
