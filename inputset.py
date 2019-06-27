#!/usr/bin/env python3

from click import Choice, argument, command, option
from click_custom import SourceArgument, SortOption
from util import get_user_name, get_user_email
from registries import registries, sources



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
@argument('registry', type=Choice(registries))
@argument('source', cls=SourceArgument, sources=sources)
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
    registry = registries[registry]

    if source['type'] == 'weblist':
        # download the weblist
        registry.load_weblist(source['value'])
    else:
        # load the file
        registry.load_file(source['value'])

    print('Success!!!')

    # Todo: add email validator?
    # see https://stackoverflow.com/questions/48679819/python-click-cli-library-retry-input-prompt-on-validation-error


if __name__ == '__main__':
    generate_inputset()
