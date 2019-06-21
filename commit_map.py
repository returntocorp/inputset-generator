#!/usr/bin/env python3
import json
import subprocess
import sys
from collections import defaultdict
from typing import Any, Dict, List

from utils import get_head


def save_json(obj: Any, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(obj, f, sort_keys=True, indent=4)


def build_commit_map(repo_urls):
    commit_map: Dict[str, List[str]] = defaultdict(list)
    errors = []

    for repo in repo_urls:
        try:
            head = get_head(repo)
            commit_map[repo].append(head)
        except Exception as e:
            errors.append(str(e))

    return commit_map, errors


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        repo_urls: List[str] = []
        with open(filename) as f:
            repo_urls = list({r for r in f.read().splitlines() if r})
            print(f"found {len(repo_urls)} repos")
        commit_map, errors = build_commit_map(repo_urls)
        cm_name = f"{filename}_commit_map.json"
        save_json(commit_map, cm_name)
        if errors:
            e_name = f"{filename}_errors.json"
            save_json(errors, e_name)
            print(
                f"there were {len(errors)} repos we couldn't find the commit hash for. See {e_name} for details"
            )
        print(f"done. Saved to {cm_name}")
    else:
        print("you must enter a file with repos")
        sys.exit(1)
