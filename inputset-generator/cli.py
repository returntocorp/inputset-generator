#!/usr/bin/env python3

import click
from copy import deepcopy
from click import argument, option, Choice
from click_shell import shell

import visualizations
from structures import Dataset
from util import get_name, get_email, get_dataset, handle_error


DEBUG = False
META_DICT, API_DICT = dict(), dict()


@shell(chain=True, prompt='r2c-isg> ')
@option('-d', '--debug', is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug):
    # set debug settings
    global DEBUG
    DEBUG = debug

    # create the ctx.obj dictionary
    ctx.ensure_object(dict)


@cli.command('and')
def spacer():
    """Does absolutely nothing, but sure does make command strings more
    readable! :)"""
    pass


@cli.command('load')
@argument('registry')
@argument('handle')
@option('-h', '--header', 'fileargs',
        help='Header string for csv file.')
@option('-p', '--parser', 'fileargs',
        help="Handle for a custom-build json parser.")
@click.pass_context
def load(ctx, registry, handle, fileargs):
    """Generates a dataset from a weblist or file."""
    try:
        if registry == 'noreg':
            registry = None

        if '.' in handle:
            # read in a file (fileargs is either a header string for csv
            # or a parser handle for json)
            ds = Dataset.load_file(handle, registry, fileargs=fileargs)
        else:
            # download a weblist
            ds = Dataset.load_weblist(handle, registry)

        ctx.obj['dataset'] = ds

    except Exception as e:
        handle_error(ctx, e, None, DEBUG)


@cli.command('restore')
@argument('filepath')
@click.pass_context
def restore(ctx, filepath):
    """Restores a pickled dataset file."""
    try:
        ds = Dataset.restore(filepath)
        ctx.obj['dataset'] = ds

    except Exception as e:
        handle_error(ctx, e, None, DEBUG)


@cli.command('backup')
@argument('filepath', default=None)
@click.pass_context
def backup(ctx, filepath):
    """Backups up a pickled version of the dataset."""
    try:
        ds = get_dataset(ctx)
        ds.backup(filepath)

    except Exception as e:
        handle_error(ctx, e, None, DEBUG)


@cli.command('import')
@argument('registry')
@argument('filepath')
@click.pass_context
def import_(ctx, registry, filepath):
    """Imports an input set json file."""
    try:
        if registry == 'noreg':
            registry = None

        ds = Dataset.import_inputset(filepath, registry)
        ctx.obj['dataset'] = ds

    except Exception as e:
        handle_error(ctx, e, None, DEBUG)


@cli.command('export')
@argument('filepath', default=None)
@click.pass_context
def export(ctx, filepath):
    """Export a dataset to an input set json."""
    try:
        ds = get_dataset(ctx)
        ds.export_inputset(filepath)

    except Exception as e:
        handle_error(ctx, e, None, DEBUG)


@cli.command('meta')
@option('-n', '--name', help='Dataset name.')
@option('-v', '--version', help='Dataset version.')
@option('-d', '--description', help='Description string.')
@option('-r', '--readme', help='Readme string.')
@option('-a', '--author', default=get_name,
        help='Author name. Defaults to git user.name.')
@option('-e', '--email', default=get_email,
        help='Author email. Defaults to git user.email.')
@click.pass_context
def meta(ctx, name, version, description, readme, author, email):
    """Sets dataset metadata."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        assert name or version or description or readme or author or email, \
            'Error setting metadata. You must provide a metadata value to set.'

        # override existing dataset metadata
        ds.name = name or ds.name
        ds.version = version or ds.version
        ds.description = description or ds.description
        ds.readme = readme or ds.readme
        ds.author = author or ds.author
        ds.email = email or ds.email

    except Exception as e:
        handle_error(ctx, e, backup_ds, debug=DEBUG)


@cli.command('api')
@option('-d', '--cache_dir')
@option('-t', '--cache_timeout')
@option('-n', '--nocache', is_flag=True)
@option('-g', '--github_pat')
@click.pass_context
def api(ctx, cache_dir, cache_timeout, nocache, github_pat):
    """Sets API settings."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        assert ds.api, 'Api has not been set for %s.' % ds.registry

        ds.api.update(cache_dir=cache_dir,
                      cache_timeout=cache_timeout,
                      nocache=nocache,
                      github_pat=github_pat)

    except Exception as e:
        handle_error(ctx, e, backup_ds, debug=DEBUG)


@cli.command('get')
@option('-m', '--metadata', is_flag=True,
        help='Download project metadata.')
@option('-v', '--versions', type=Choice(['all', 'latest']),
        help='Filter versions by historical order.')
@click.pass_context
def get(ctx, metadata, versions):
    """Downloads project and version information."""

    # get the dataset
    try:
        ds = get_dataset(ctx)
    except Exception as e:
        handle_error(ctx, e, None, debug=DEBUG)
        return

    # load project metadata
    if metadata:
        backup_ds = deepcopy(ds)
        try:
            ds.get_projects_meta()

        except Exception as e:
            handle_error(ctx, e, backup_ds, debug=DEBUG)

    # load project versions
    if versions:
        backup_ds = deepcopy(ds)
        try:
            ds.get_project_versions(historical=versions)

        except Exception as e:
            handle_error(ctx, e, backup_ds, debug=DEBUG)


@cli.command('trim')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@click.pass_context
def trim(ctx, n, on_projects):
    """Trims projects or versions from a dataset."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        ds.trim(n, on_projects)

    except Exception as e:
        handle_error(ctx, e, backup_ds, debug=DEBUG)


@cli.command('sort')
@argument('params', type=str)
@click.pass_context
def sort(ctx, params):
    """Sorts a dataset."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        ds.sort(params.split())

    except Exception as e:
        handle_error(ctx, e, backup_ds, debug=DEBUG)


@cli.command('sample')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@option('-s', '--seed')
@click.pass_context
def sample(ctx, n, on_projects, seed):
    """Samples projects or versions from a dataset."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        ds.sample(n, on_projects, seed)

    except Exception as e:
        handle_error(ctx, e, backup_ds, debug=DEBUG)


@cli.command('show')
@argument('n', type=int, default=5)
@option('-d', '--details', is_flag=True, default=False)
@click.pass_context
def show(ctx, n, details):
    """Shows the details of the first n projects."""
    try:
        ds = get_dataset(ctx)
        visualizations.show(ds, n, details)

    except Exception as e:
        handle_error(ctx, e, None, debug=DEBUG)


@cli.command('describe')
@argument('scope', type=Choice(['dataset', 'project', 'version']))
@click.pass_context
def describe(ctx, scope):
    """Describes the structure of the dataset/project/version."""
    try:
        ds = get_dataset(ctx)
        visualizations.describe(ds, scope)

    except Exception as e:
        handle_error(ctx, e, None, debug=DEBUG)


if __name__ == '__main__':
    cli()
