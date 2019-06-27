from .pypi import PypiRegistry

# create a central mapping of all registries
registries = {'pypi': PypiRegistry()}

# generate a mapping of registry names to available weblist names
# (used to generate intelligent weblist name suggestions to click)
sources = {k: [s for s in r.weblists] for k, r in registries.items()}
