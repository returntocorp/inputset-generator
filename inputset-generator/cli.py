#!/usr/bin/env python3

import click
import json
from copy import deepcopy
from datetime import timedelta
from click import argument, option, Choice
from click_shell import shell

import visualizations
from structures import Dataset
from util import get_dataset, print_error


DEBUG = False
# store meta/api settings if a dataset hasn't yet been loaded
TEMP_SETTINGS = dict()


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

        global TEMP_SETTINGS

        if '.' in handle:
            # read in a file (fileargs is either a header string for csv
            # or a parser handle for json)
            ds = Dataset.load_file(handle, registry,
                                   fileargs=fileargs, **TEMP_SETTINGS)

        else:
            # download a weblist
            ds = Dataset.load_weblist(handle, registry, **TEMP_SETTINGS)

        ctx.obj['dataset'] = ds

        # reset the temporary api/metadata dict
        TEMP_SETTINGS = dict()

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('restore')
@argument('filepath')
@click.pass_context
def restore(ctx, filepath):
    """Restores a pickled dataset file."""
    try:
        ds = Dataset.restore(filepath)
        ctx.obj['dataset'] = ds

        # reset the temporary api/metadata dict
        global TEMP_SETTINGS
        TEMP_SETTINGS = dict()

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('backup')
@argument('filepath', default=None)
@click.pass_context
def backup(ctx, filepath):
    """Backups up a pickled version of the dataset."""
    try:
        ds = get_dataset(ctx)
        ds.backup(filepath)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('import')
@argument('registry')
@argument('filepath')
@click.pass_context
def import_(ctx, registry, filepath):
    """Imports an input set json file."""
    try:
        if registry == 'noreg':
            registry = None

        global TEMP_SETTINGS

        ds = Dataset.import_inputset(filepath, registry, **TEMP_SETTINGS)
        ctx.obj['dataset'] = ds

        # reset the temporary api/metadata dict
        TEMP_SETTINGS = dict()

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('export')
@argument('filepath', default=None)
@click.pass_context
def export(ctx, filepath):
    """Export a dataset to an input set json."""
    try:
        ds = get_dataset(ctx)
        ds.export_inputset(filepath)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('meta')
@option('-n', '--name', help='Dataset name.')
@option('-v', '--version', help='Dataset version.')
@option('-d', '--description', help='Description string.')
@option('-r', '--readme', help='Readme string.')
@option('-a', '--author',
        help='Author name. Defaults to git user.name.')
@option('-e', '--email',
        help='Author email. Defaults to git user.email.')
@click.pass_context
def meta(ctx, name, version, description, readme, author, email):
    """Sets dataset metadata."""
    try:
        ds = ctx.obj.get('dataset', None)

        if ds:
            # update dataset's metadata
            ds.update(name=name, version=version, description=description,
                      readme=readme, author=author, email=email)

        else:
            global TEMP_SETTINGS
            if name: TEMP_SETTINGS['name'] = name
            if version: TEMP_SETTINGS['version'] = version
            if description: TEMP_SETTINGS['description'] = description
            if readme: TEMP_SETTINGS['readme'] = readme
            if author: TEMP_SETTINGS['author'] = author
            if email: TEMP_SETTINGS['email'] = email

        # print the outcome
        settings = []
        if name: settings.append('name')
        if version: settings.append('version')
        if description: settings.append('description')
        if readme: settings.append('readme')
        if author: settings.append('author')
        if email: settings.append('email')
        set_str = ', '.join([s for s in settings if s])
        print("    Set the dataset's %s." % set_str)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('api')
@option('-d', '--cache_dir')
@option('-t', '--cache_timeout', type=int)
@option('-n', '--nocache', is_flag=True)
@option('-g', '--github_pat')
@click.pass_context
def api(ctx, cache_dir, cache_timeout, nocache, github_pat):
    """Sets API settings."""

    # convert cache timeout string to timedelta
    if cache_timeout:
        cache_timeout = timedelta(days=cache_timeout)

    try:
        ds = ctx.obj.get('dataset', None)
        if ds and ds.api:
            # update the api
            ds.api.update(cache_dir=cache_dir,
                          cache_timeout=cache_timeout,
                          nocache=nocache,
                          github_pat=github_pat)

        else:
            # no ds/api; save the settings for when there is one
            global TEMP_SETTINGS
            if cache_dir: TEMP_SETTINGS['cache_dir'] = cache_dir
            if cache_timeout: TEMP_SETTINGS['cache_timeout'] = cache_timeout
            if nocache: TEMP_SETTINGS['nocache'] = nocache
            if github_pat: TEMP_SETTINGS['github_pat'] = github_pat

        # print the outcome
        settings = []
        if cache_dir: settings.append('cache_dir')
        if cache_timeout: settings.append('cache_timeout')
        if nocache: settings.append('nocache')
        if github_pat: settings.append('github_pat')
        set_str = ', '.join([s for s in settings if s])
        print("    Set the api's %s." % set_str)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('get')
@option('-m', '--metadata', is_flag=True,
        help='Download project metadata.')
@option('-v', '--versions', type=Choice(['all', 'latest']),
        help='Filter versions by historical order.')
@click.pass_context
def get(ctx, metadata, versions):
    """Downloads project and version information."""
    backup_ds = None

    # load project metadata
    if metadata:
        try:
            ds = get_dataset(ctx)
            ds.get_projects_meta()
            backup_ds = deepcopy(ds)

        except Exception as e:
            print_error(e, DEBUG)

            # roll back the db
            ctx.obj['dataset'] = backup_ds
            print('    The dataset is unchanged.')

    # load project versions
    if versions:
        try:
            ds = get_dataset(ctx)
            ds.get_project_versions(historical=versions)
            backup_ds = deepcopy(ds)

        except Exception as e:
            print_error(e, DEBUG)

            # roll back the db
            ctx.obj['dataset'] = backup_ds
            print('    The dataset is unchanged.')


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
        print_error(e, DEBUG)

        # roll back the db
        ctx.obj['dataset'] = backup_ds
        print('    The dataset is unchanged.')


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
        print_error(e, DEBUG)

        # roll back the db
        ctx.obj['dataset'] = backup_ds
        print('    The dataset is unchanged.')


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
        print_error(e, DEBUG)

        # roll back the db
        ctx.obj['dataset'] = backup_ds
        print('    The dataset is unchanged.')


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
        print_error(e, DEBUG)


@cli.command('describe')
@argument('scope', type=Choice(['dataset', 'project', 'version']))
@click.pass_context
def describe(ctx, scope):
    """Describes the structure of the dataset/project/version."""
    try:
        ds = get_dataset(ctx)
        visualizations.describe(ds, scope)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('jsonify')
@argument('filepath', default=None)
@click.pass_context
def jsonify(ctx, filepath):
    """Prints the complete dataset to json for easier review."""
    try:
        ds = get_dataset(ctx)
        data_dict = ds.to_json()

        # file name is dataset name, if not provided by user
        filepath = filepath or (ds.name + '_tmp.json')

        # save to disk
        with open(filepath, 'w') as file:
            json.dump(data_dict, file, indent=4)
        print('    Dumped dataset json to %s.' % filepath)

    except Exception as e:
        print_error(e, DEBUG)


if __name__ == '__main__':
    cli()
