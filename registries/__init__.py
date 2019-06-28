from ._base import Registry
from .pypi import PypiRegistry


registries = {
    'pypi': PypiRegistry()
}
