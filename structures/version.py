class Version:
    def __init__(self, version_string: str = '', commit_hash: str = ''):
        # must have a version string or commit hash
        if not (version_string or commit_hash):
            raise Exception('Version must have a version string '
                            'or commit hash.')

        self.version_string = version_string
        self.commit_hash = commit_hash
