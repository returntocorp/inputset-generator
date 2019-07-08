from structures.projects import Project


class GithubRepo(Project):
    def check_guarantees(self):
        """Guarantees a name/org or a url."""
        if 'url' not in self.meta_ and ('name' not in self.meta_ or
                                        'org' not in self.meta_):
            raise Exception('Repo name/org, url, or api url '
                            'must be provided.')

    def to_inputset(self) -> list:
        """Converts github repos/commits to GitRepo/GitRepoCommit dict."""
        lst = []

        if len(self.versions) > 0:
            # return input set type GitRepoCommit
            pass

        else:
            # return input set type GitRepo
            pass

        return lst
