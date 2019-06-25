#!/usr/bin/env python3

from click import Choice, argument, command, option
from click_custom import SourceArgument, SortOption
from util import get_user_name, get_user_email

registries = {
    'npm': {
        'url': '',
        'lists': {}
    },
    'git': {
        'url': '',
        'lists': {}
    },
    'pypi': {
        'url': '',
        'lists': {
            '5k30days': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json',
            '5kyear': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json'
        }
    }
}
sources = {t: [s for s in data['lists']] for t, data in registries.items()}


@command()
@argument('registry', type=Choice(registries.keys()))
@argument('source', cls=SourceArgument, sources=sources)
@option('--get', type=Choice(['latest', 'major', 'all']), default='all',
        help='Which versions/commits to obtain. Defaults to all.')
@option('--sort', cls=SortOption, multiple=True,
        type=Choice(['asc', 'desc', 'popularity', 'date', 'name']),
        help='OPTIONAL Sort the list of versions/commits, performed '
             'immediately after --get.')
@option('--head', type=int,
        help='OPTIONAL Trim to the first n projects.')
@option('--sample', type=int,
        help='OPTIONAL Randomly sample n projects.')
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
def generate_inputset(registry: str, source: str,
                      get: str, sort: tuple,
                      head: int, sample: int,
                      name: str, version: str,
                      description: str, readme: str,
                      author: str, email: str):
    """Generate an input set from one of the named source types."""
    print('Success!!!')
    pass

    """
    Note: Possible email validator here:
    https://stackoverflow.com/questions/48679819/python-click-cli-library-retry-input-prompt-on-validation-error
    """


if __name__ == '__main__':
    generate_inputset()
