#!/usr/bin/env python3

import json
import os
import pickle
import re
import subprocess
import sys
import traceback
from typing import Set

import requests

from utils import clean_url, normalize_full_repo_url

PYPI_URL = "https://pypi.python.org/pypi/%s/json"
URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json"


def fetch_pypi_top_urls(count=None):
    resp = requests.get(URL).json()

    findings: Set[str] = set([])
    searched: Set[str] = set([])

    rows = resp["rows"][:count]
    for i, row in enumerate(rows):
        print("entry %d/%d" % (i, len(rows)), file=sys.stderr)
        project = row["project"]

        if project in searched:
            continue

        # get meta
        try:
            meta = requests.get(PYPI_URL % project).json()
            homepage = meta["info"]["home_page"]
            desc = meta["info"]["description"]
            searched.add(project)
            if homepage and ("github" in homepage or "git" in homepage):
                url = normalize_full_repo_url(homepage)
                if url:
                    findings.add(url)
                else:
                    findings.add(url)
            elif desc and ("github" in desc or "git" in desc):
                url = normalize_full_repo_url(desc)
                if url:
                    findings.add(url)
                else:
                    findings.add(clean_url(desc))
            else:
                print("no git url found for %s" % project, file=sys.stderr)
        except Exception as e:
            print("failed for %s" % project, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    return findings


if __name__ == "__main__":
    print(fetch_pypi_top_urls())
