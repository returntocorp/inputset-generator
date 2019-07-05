from ._version import Version
from .github_commit import GithubCommit
from .npm_version import NpmVersion
from .pypi_release import PypiRelease


# Note: This must have the same keys as the registries/projects mappings
versions_map = {
    'noreg': Version,
    'github': GithubCommit,
    'npm': NpmVersion,
    'pypi': PypiRelease
}
