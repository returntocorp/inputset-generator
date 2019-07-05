from .github_loader import GithubLoader
from .npm_loader import NpmLoader
from .pypi_loader import PypiLoader


weblist_loaders = {
    'github': GithubLoader,
    'npm': NpmLoader,
    'pypi': PypiLoader
}
