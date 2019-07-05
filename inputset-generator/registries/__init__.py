from ._registry import Registry
from .github import Github
from .npm import Npm
from .pypi import Pypi


registries = {
    'noreg': None,
    'github': Github(),
    'npm': Npm(),
    'pypi': Pypi()
}
