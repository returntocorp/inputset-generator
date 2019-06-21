import json
import os
import pickle
import re
import subprocess
import sys
from typing import Set

import requests

DOT_GIT_REGEX = re.compile("[.]git$")


def clean_url(url):
    """
        Cleans all possible git "url" formats into format: https://domain/org/repo_name

        e.g. from git@github.com:terinjokes/gulp-uglify
            to https://github.com/terinjokes/gulp-uglify/
    """
    try:
        stripped_url = DOT_GIT_REGEX.sub("", url)
        cleaned_url = (
            stripped_url.replace(" ", "")
            .replace("git+", "")
            .replace("git:", "")
            .replace("www.", "")
            .replace("git@", "")
            .replace("https://", "")
            .replace("http://", "")
            .replace("ssh://", "")
            .replace("git://", "")
            .replace("github.com:", "github.com/")
            .replace("github:", "github.com/")
            .replace("bitbucket:", "bitbucket.org/")
            .replace("gitlab:", "gitlab.com/")
            .rstrip("/")
        )
        parts = cleaned_url.split("/")
        if len(parts) < 2:
            print(f"url {url} is too short")
            return None
        elif len(parts) == 2:
            # we assume github.com for things like 'palantir/blueprint'
            cleaned_url = "github.com/" + cleaned_url
        elif len(parts) == 3:
            # ok
            pass
        else:
            print(f"url {url} is too long")
            return None

        # Handle Format git+https://isaacs@github.com/npm/cli.git
        parts = cleaned_url.split("@")
        cleaned_url = parts[-1]
        return "https://" + cleaned_url

    except Exception as e:
        print(f"unable to clean url '{url}', {e}")
        return None


def normalize_full_repo_url(url):
    GITHUB_REGEX = re.compile(
        r"""(github\.com[\/][A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+)#?([\/A-Za-z0-9_.-]+)?"""
    )
    url = url.replace("github.com:", "github.com/", 1).replace(
        "github:", "github.com/", 1
    )
    matches = re.search(GITHUB_REGEX, url)
    if matches:
        gh = matches.group(1)
        gh_suffix = matches.group(2)
        if gh.endswith("."):
            gh = gh[:-1]
        return "https://" + gh
    return None


def get_head(repo):
    value = subprocess.check_output(
        ["git", "ls-remote", "--symref", repo, "HEAD"], env={"GIT_TERMINAL_PROMPT": "0"}
    )
    lines = value.decode("utf-8").splitlines()
    sha_hash = lines[-1].split("\t")[0]
    return sha_hash
