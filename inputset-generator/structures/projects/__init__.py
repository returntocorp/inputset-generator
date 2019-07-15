from ._project import Project
from .default_project import DefaultProject
from .github_repo import GithubRepo
from .npm_package import NpmPackage
from .pypi_project import PypiProject


project_map = {
    'github': GithubRepo,
    'npm': NpmPackage,
    'pypi': PypiProject
}
