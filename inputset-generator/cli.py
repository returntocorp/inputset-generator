#!/usr/bin/env python3

import click
from click import argument, option, Choice
from click_shell import shell

from structures import Dataset
from util import get_user_name, get_user_email


def get_dataset(ctx) -> Dataset:
    """Checks that the dataset has been loaded."""
    ds = ctx.obj.get('dataset', None)

    assert ds, 'Dataset has not been loaded.'

    return ds


@shell(chain=True, prompt='r2c-isg> ')
@click.pass_context
def cli(ctx):
    # create the ctx.obj dictionary
    ctx.ensure_object(dict)


@cli.command('meta')
@option('-n', '--name', help='Dataset name.')
@option('-v', '--version', help='Dataset version.')
@option('-d', '--description', help='Description string.')
@option('-r', '--readme', help='Readme string.')
@option('-a', '--author', default=get_user_name,
        help='Author name. Defaults to git user.name.')
@option('-e', '--email', default=get_user_email,
        help='Author email. Defaults to git user.email.')
@click.pass_context
def meta(ctx, name, version, description, readme, author, email):
    ds = get_dataset(ctx)
    ds.set_meta(name, version, description, readme, author, email)


@cli.command('load')
@argument('registry')
@argument('handle')
@option('-h', '--header', 'fileargs',
        help='Header string for csv file.')
@option('-p', '--parser', 'fileargs',
        help="Handle for a custom-build json parser.")
@click.pass_context
def load(ctx, registry, handle, fileargs):
    # initialize a dataset and add it to the context
    if registry == 'noreg':
        registry = None

    if '.' in handle:
        # read in a file (fileargs is either a header string for csv
        # or a parser handle for json)
        ds = Dataset.load_file(handle, registry)
    else:
        # download a weblist
        ds = Dataset.load_weblist(handle, registry)

    ctx.obj['dataset'] = ds


@cli.command('restore')
@argument('filepath')
@click.pass_context
def restore(ctx, filepath):
    # restore the dataset from file
    ds = Dataset.restore(filepath)
    ctx.obj['dataset'] = ds


@cli.command('backup')
@argument('filepath', default=None)
@click.pass_context
def backup(ctx, filepath):
    ds = get_dataset(ctx)
    ds.backup(filepath)


@cli.command('import')
@argument('registry')
@argument('filepath')
@click.pass_context
def import_(ctx, registry, filepath):
    # initialize a dataset and add it to the context
    if registry == 'noreg':
        registry = None
    ds = Dataset.import_inputset(filepath, registry)
    ctx.obj['dataset'] = ds


@cli.command('export')
@argument('filepath', default=None)
@click.pass_context
def export(ctx, filepath):
    ds = get_dataset(ctx)
    ds.export_inputset(filepath)


@cli.command('get')
@option('-m', '--metadata', is_flag=True,
        help='Download project metadata.')
@option('-v', '--versions', type=Choice(['all', 'latest']),
        help='Filter versions by historical order.')
@click.pass_context
def get(ctx, metadata, versions):
    ds = get_dataset(ctx)

    if metadata:
        # load project metadata
        ds.get_projects_meta()

    if versions:
        # load project versions
        ds.get_project_versions(versions)


@cli.command('trim')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@click.pass_context
def trim(ctx, n, on_projects):
    ds = get_dataset(ctx)
    ds.trim(n, on_projects)


@cli.command('sort')
@argument('params', type=str)
@click.pass_context
def sort(ctx, params):
    ds = get_dataset(ctx)
    ds.sort(params.split())


@cli.command('sample')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@click.pass_context
def sample(ctx, n, on_projects):
    ds = get_dataset(ctx)
    ds.sample(n, on_projects)


@cli.command('head')
@argument('n', type=int, default=5)
@option('-d', '--details', is_flag=True, default=False)
@click.pass_context
def print_head(ctx, n, details):
    ds = get_dataset(ctx)
    ds.head(n, details)


@cli.command('describe')
@argument('scope', type=Choice(['dataset', 'project', 'version']))
@click.pass_context
def print_structure(ctx, scope):
    ds = get_dataset(ctx)
    ds.describe(scope)


if __name__ == '__main__':
    cli()
