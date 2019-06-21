#!/usr/bin/env python3

import argparse
import json

from commit_map import build_commit_map
from pypi import fetch_pypi_top_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "package_manager",
        help="The package manager to get repos for",
        type=str,
        choices=["npm", "pypi"],
    )
    parser.add_argument(
        "count", help="number of packages to create inputset for", type=int
    )
    parser.add_argument(
        "commit_selector",
        help="the commit selection strategy",
        type=str,
        choices=["head"],
    )
    parser.add_argument("name", help="inputset name field")
    parser.add_argument("version", help="inputset version field")
    parser.add_argument("--author", help="inputset author field", required=False)
    parser.add_argument("--description", help="inputset description", required=False)

    args = parser.parse_args()
    print(f"Fetching urls for top {args.count} packages on {args.package_manager}")

    if args.package_manager == "pypi":
        urls = fetch_pypi_top_urls(args.count)
    else:
        raise Exception("This script doesn't support npm yet. Please implement it?")

    print(f"Got {len(urls)} urls")

    if args.commit_selector == "head":
        print(f"Finding head commits for urls...")
        commit_map, errors = build_commit_map(urls)
        inputset = {
            "name": args.name,
            "version": args.version,
            "inputs": [
                {"input_type": "GitRepoCommit", "repo_url": k, "commit_hash": v[0]}
                for k, v in commit_map.items()
            ],
        }

        if args.description:
            inputset["description"] = args.description
        if args.author:
            inputset["author"] = args.author

        output_path = f"{args.package_manager}-{args.count}-{args.commit_selector}"
        print(f"Writing resulting inputset to {output_path}")
        with open(output_path, "w") as f:
            json.dump(inputset, f, indent=4)
