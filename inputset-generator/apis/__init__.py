from ._api import Api
from .github import Github
from .npm import Npm
from .pypi import Pypi

api_map = {
    'github': Github,
    'npm': Npm,
    'pypi': Pypi
}
