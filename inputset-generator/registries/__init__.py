from ._base import Registry
from .pypi import Pypi
from .github import Github


registries = {
    'pypi': Pypi(),
    'github': Github()
}
