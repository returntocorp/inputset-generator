## R2C `0.4.x` Data Structures

### Overview

At a high level, an R2C ISG `Dataset` contains a list of `Project` objects which
in turn contain lists of `Version` objects. While different registries give
these objects different names (eg, Pypi's "project" and "release" vs. Github's
"repo" and "commit"), the fundamental relationships are the same.

The `0.4.x` base `Project` and `Version` classes are intended to be lightweight
and flexible, and are then extended and customized for each registry. The
registry-specific classes are as follows:

- Github: `GithubRepo` and `GithubCommit`
- Npm: `NpmPackage` and `NpmVersion`
- Pypi: `PypiProject` and `PypiRelease`

These structures provide the following functionality: 

- A `metadata` dictionary for storing data from authoritative sources, namely
data obtained from a registry api.
- A `data` dictionary for storing data from non-authoritative sources such as
files, weblists, and user-provided data.
- A `get_ids()` function which returns a dictionary of name:value pairs of
unique project/version identifiers. Typically, unique identifiers include `name`
and `url` for projects and `version` or `commit` for versions. This function is
used for project/version comparison, and must be implemented by each registry's
structures.
- _(Project-only)_ A `to_inputset()` function to generate a list of input set
items. This function's implementation is unique to each registry.
- Each registry structure may also add its own custom properties. For example,
`GithubRepo` provides `full_name` and `url` properties.


### Improvements vs. `0.3.x`

The `0.4.x` structures have significant advantages over the older structures.
A dataset typically goes through the following 4-step life cycle. At each step,
the new structures improve on the old.

1. Populate the dataset with a list of projects obtained from a weblist, file,
or other non-authoritative source.

    The new structures include a custom `__eq__()` comparator that depends on
    the previously-discussed `get_ids()` function and considers two structures
    to be equal if:
    
    - they are of the same type,
    - they share at least one id key, and
    - they do not disagree on any values of shared id keys.

    This provides a mechanism for merging projects/versions into an existing
    list, something the older structures do not support.
    
2. Retrieve project/version data an authoritaive source (the registry API).
 
    Separating out non-authoritative, editable information from data from
    authoritative sources that should generally not be edited makes it much
    clearer where the data came from and whether it can (should) be edited.
    This also removes the possibility of accidentally overwriting a value from
    a different source. For example, non-authoritative and authoritative sources
    both commonly provide a `url` attribute, so storing them in separate
    dictionaries avoids the possibility of one overwriting the other. 

3. Manipulate the dataset.

    Previous structures relied on a complex system of uuids that involved lambda
    functions and could not be easily exported to json. As such, the json files
    built using the `show` command could not be easily edited and re-imported.
    Swapping to using jsonifiable dataclasses eliminates this problem, providing
    much stronger support for exporting datasets to json, editing them, and
    re-importing them.

4. Export the dataset to an input set.

    Previous structures relied on having a guaranteed set of attributes needed
    for exporting a project/version pair to an input set item. This would then
    fail if the guarantees were not met. The new structures replace this with a
    more flexible system, allowing for invalid project/version pairs to be
    exported if the user so desires.

    This functionality is complemented with support for a more robust system for
    logging warnings and errors, making it easier for users to quickly identify
    invalid data in their datasets.


### Notes

- Values in a project or version's `data` dict take precedence over any values
in the `metadata` dict, and little validation is performed on these values, as
the ISG assumes the user is inputting valid data. As such, if the `data` dict of
a`GithubRepo`, `NpmPackage`, or `PypiProject` contains a malformed url, the
metadata/versions retrieval process will fail. While this may seem drastic, it
is an intentional design decision based on the following factors:

    - A structure's attributes should be relatively invariant throughout its
    life, to avoid breaking any external mappings built by users. For example,
    if a user has built a mapping of attr:project, retrieving the project's
    metadata should not change the attribute, thereby breaking the mapping.
    Since, as mentioned previously, the typical life cycle of a structure is
    that first its `data` dict is populated, then its `metadata` dict is
    populated from that, it seems reasonable to prioritize `data` attrs over
    `metadata` attrs.

    - Input validation code is inherently "magical", and would have to be custom
    built for each structure. This adds substantial debugging and maintenance
    overhead, and there's already enough of that with the `name_from_url()` and
    `url_from_name()` utility functions.

    Given these circumstances, Python's "we're all adults here" philosophy seems
    appropriate. ISG allows users to provide invalid data, contenting itself
    with providing extensive and informative logging when such errors do occur.

- The `Project` attribute functions (eg, `PypiProject`'s `name` and `url`)
should never need to refer to metadata, since in order to get the metadata in
the first place the data dict must have contained sufficient identifying
information for the metadata to be retrieved in the first place. It doesn't hurt
to leave the extra fallback methods in the `Project` attrs though, and Future
registries may may not have the same interchangeability between a project's name
and url that Github, NPM, and Pypi share.

    The same cannot be said of `Version` though, as its metadata is obtained
    based on the `Project` class's data dict, not its own data dict. 
