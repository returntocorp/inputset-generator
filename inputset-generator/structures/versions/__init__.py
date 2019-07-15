from ._version import Version
from ._version import Version as DefaultVersion
from .github_commit import GithubCommit
from .npm_version import NpmVersion
from .pypi_release import PypiRelease

version_map = {
    'github': GithubCommit,
    'npm': NpmVersion,
    'pypi': PypiRelease
}
