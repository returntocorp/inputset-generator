from ._project import Project
from .github_repo import GithubRepo
from .npm_package import NpmPackage
from .pypi_project import PypiProject


class_map = {
    'github': GithubRepo,
    'npm': NpmPackage,
    'pypi': PypiProject,
}
