#!/usr/bin/env python3
from click import Choice, argument, command, option

from click_custom import SourceArgument, SortOption
from structures import Dataset
from registries import registries


# generate a mapping of registry names to available weblist names
# (used to generate intelligent weblist name suggestions to click)
source_args = {k: [s for s in r.weblists] for k, r in registries.items()}

# add a 'noreg' registry argument so click doesn't complain when the
# user doesn't want to specify a registry
registry_args = registries
registry_args['noreg'] = None



'''
@option('--name', prompt='Filename',
        help='Input set name and file name.')
@option('--version', prompt='Version',
        help='Input set version (uses semantic versioning).')
@option('--description', prompt='Description', default='',
        help='OPTIONAL Input set description.')
@option('--readme', prompt='Readme', default='',
        help='OPTIONAL Input set markdown readme.')
@option('--author', prompt='Author', default=get_user_name,
        help='Author name. Defaults to git user.name.')
@option('--email', prompt='Email', default=get_user_email,
        help='Author email. Defaults to git user.email.')
'''
'''
name: str, version: str,
description: str, readme: str,
author: str, email: str):
'''


@command()
@argument('registry', type=Choice(registry_args))
@argument('source', cls=SourceArgument, sources=source_args)
@option('--get', type=Choice(['latest', 'major', 'monthly', 'all']),
        default='all', help='Which versions/commits to obtain. '
                            'Defaults to all.')
@option('--sort', cls=SortOption, multiple=True,
        type=Choice(['asc', 'desc', 'popularity', 'date', 'name']),
        help='OPTIONAL Sort the list of versions/commits, performed '
             'immediately after --get.')
@option('--head', type=int,
        help='OPTIONAL Trim to the first n projects.')
@option('--sample', type=int,
        help='OPTIONAL Randomly sample n projects.')
def generate_inputset(registry: str, source: dict,
                      get: str, sort: tuple,
                      head: int, sample: int):
    """Generate an input set from one of the named source types."""

    # get the appropriate registry
    ds = Dataset(registry)

    # load the initial data
    if source['type'] == 'file':
        # read in a file
        ds.load_file(source['path'])
    else:
        # download the weblist
        ds.load_weblist(source['name'])

    # Todo: perform transformations

    # save the result to disk
    ds.save()


if __name__ == '__main__':
    generate_inputset()
