from .core import Project, Version
from .generic import GenericProject, GenericVersion
from .github import GithubRepo, GithubCommit
from .npm import NpmPackage, NpmVersion
from .pypi import PypiProject, PypiRelease


project_map = {
    'github': GithubRepo,
    'npm': NpmPackage,
    'pypi': PypiProject
}

version_map = {
    'github': GithubCommit,
    'npm': NpmVersion,
    'pypi': PypiRelease
}
