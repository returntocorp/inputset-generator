from structures.projects import Project


class GithubRepo(Project):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set the metadata
        self.meta_name = kwargs.get('name', None)
        self.meta_org = kwargs.get('organization', None) or \
                        kwargs.get('owner', dict()).get('login', None)
        self.meta_url = kwargs.get('repo_url', None) or \
                        kwargs.get('html_url', None)
        self.meta_apiurl = kwargs.get('api_url', None) or \
                           kwargs.get('url', None)

        #if not ((self.meta_name and self.meta_org) or self.meta_url or self.meta_apiurl):


        temp = 5

    def to_inputset(self) -> list:
        """Converts github repos/commits to a list of input set dicts."""
        lst = []

        if len(self.versions) > 0:
            # return input set type GitRepoCommit
            pass

        else:
            # return input set type GitRepo
            pass

        return lst
