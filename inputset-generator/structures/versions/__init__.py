from ._base import Version
from .github_commit import GithubCommit
from .npm_version import NpmVersion
from .pypi_release import PypiRelease


# Note: This must have the same keys as the registries/projects mappings
mapping = {
    'noreg': Version,
    'github': GithubCommit,
    'npm': NpmVersion,
    'pypi': PypiRelease
}
