import subprocess


def get_user_name():
    """Loads the default user name."""

    # only check git user.name for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.name']
        ).decode("utf-8").strip()
    except Exception:
        return None


def get_user_email():
    """Loads the default user email."""

    # only check git user.email for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.email']
        ).decode("utf-8").strip()
    except Exception:
        return None
