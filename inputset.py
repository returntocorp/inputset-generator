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
@option('--get', type=Choice(['latest', 'major', 'all']))
@option('--sort', cls=SortOption, multiple=True, help='Optional',
        type=Choice(['asc', 'desc', 'popularity', 'date', 'name']))
@option('--head', type=int, help='Optional')
@option('--sample', type=int, help='Optional')
@option('--name', prompt='Filename')
@option('--version', prompt='Version')
@option('--description', prompt='Description', default='', help='Optional')
@option('--readme', prompt='Readme', default='', help='Optional')
@option('--author', prompt='Author', default=get_user_name, help='Defaults to git user.name')
@option('--email', prompt='Email', default=get_user_email, help='Defaults to git user.email')
def generate_inputset(registry: str, source: str,
                      get: str, sort: tuple,
                      head: int, sample: int,
                      name: str, version: str,
                      description: str, readme: str,
                      author: str, email: str):
    """Generate an input set from one of the named source types."""
    temp = 5
    pass

    """
    Note: Possible email validator here:
    https://stackoverflow.com/questions/48679819/python-click-cli-library-retry-input-prompt-on-validation-error
    """


if __name__ == '__main__':
    generate_inputset()
