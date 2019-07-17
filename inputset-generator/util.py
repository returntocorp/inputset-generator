import subprocess
import traceback

from structures import Dataset


def get_name():
    """Loads the default user name."""

    # only check git user.name for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.name']
        ).decode("utf-8").strip()
    except:
        return None


def get_email():
    """Loads the default user email."""

    # only check git user.email for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.email']
        ).decode("utf-8").strip()
    except:
        return None


def get_dataset(ctx) -> Dataset:
    """Gets the dataset from the CLI context."""
    ds = ctx.obj.get('dataset', None)

    assert ds, 'You must load a dataset before using this command.'

    return ds


def handle_error(ctx, err, backup_ds, debug=False) -> None:
    """Handles all CLI errors."""

    # print the exception info
    if debug:
        traceback.print_tb(err.__traceback__)
    print(err)

    # roll back the dataset, if applicable
    if isinstance(err, AssertionError):
        ctx.obj['dataset'] = backup_ds
        print('The dataset has been reverted.')

