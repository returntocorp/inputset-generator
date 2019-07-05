from ._registry import Registry
from .github import Github
from .npm import Npm
from .pypi import Pypi


# Note: This must have the same keys as the projects/versions mappings
registries_map = {
    'noreg': None,
    'github': Github(),
    'npm': Npm(),
    'pypi': Pypi()
}
