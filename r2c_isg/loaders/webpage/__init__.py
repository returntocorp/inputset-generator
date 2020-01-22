from .github_loader import GithubLoader
from .npm_loader import NpmLoader
from .pypi_loader import PypiLoader


webpageloader_map = {
    'github': GithubLoader,
    'npm': NpmLoader,
    'pypi': PypiLoader
}
