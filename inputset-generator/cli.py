#!/usr/bin/env python3

import click
from click import argument, option, Choice
from click_shell import shell
from dotenv import load_dotenv

from structures import Dataset
from util import get_user_name, get_user_email


def get_dataset(ctx) -> Dataset:
    """Checks that the dataset has been loaded."""
    ds = ctx.obj.get('dataset', None)

    if not ds:
        raise Exception('Error: Dataset has not been loaded.')

    return ds


@shell(chain=True, prompt='inputset-generator > ',
       intro='Starting input set generator')
@click.pass_context
def cli(ctx):
    # pull in any environment vars
    load_dotenv()

    # create the ctx.obj dictionary
    ctx.ensure_object(dict)


@cli.command('load')
@argument('registry')
@argument('handle')
@option('-h', '--header', 'fileargs',
        help='Header string for csv file.')
@option('-s', '--structure', 'fileargs',
        help="Json file structure (eg, 'r2c').")
@click.pass_context
def load(ctx, registry, handle, fileargs):
    # initialize a dataset and add it to the context
    if registry == 'noreg':
        ds = Dataset()
    else:
        ds = Dataset(registry)
    ctx.obj['dataset'] = ds

    if '.' in handle:
        # read in a file (fileargs is either a header string for csv
        # or a file structure handle--eg, 'r2c'--for json)
        ds.load_file(handle, fileargs)
    else:
        # download a weblist
        ds.load_weblist(handle)


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


@cli.command('save')
@argument('filepath')
@click.pass_context
def save(ctx, filepath):
    ds = get_dataset(ctx)
    ds.save(filepath)


@cli.command('head')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@click.pass_context
def head(ctx, n, on_projects):
    ds = get_dataset(ctx)
    ds.head(n, on_projects)


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


if __name__ == '__main__':
    cli()
