from ._base import Registry
from .pypi import PypiRegistry
from .github import GithubRegistry


registries = {
    'pypi': PypiRegistry(),
    'github': GithubRegistry()
}
