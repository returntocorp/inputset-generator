from ._project import Project
from .github_repo import GithubRepo
from .npm_package import NpmPackage
from .pypi_project import PypiProject


# Note: This must have the same keys as the registries/versions mappings
projects_map = {
    'noreg': Project,
    'github': GithubRepo,
    'npm': NpmPackage,
    'pypi': PypiProject,
}
