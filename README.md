# Input Set Generator

```
cd inputset-generator
source venv/bin/activate
./inputset.py COMMANDS
```

## COMMANDS
- **setreg** name
Sets the package registry to the specified name.

	**Arguments:**
	- __name__: The name of the registry. Valid: pypi, npm *(incomplete)*, github *(incomplete)*.

	---

- **load** [-m] [-v type] [-h "header_string"] handle
Loads the dataset from file/weblist.

	**Arguments:**
	- __handle__: Path to json/csv file or name of weblist (eg, 'top5kyear'). Weblist requires that registry be set.

	**Options:**
	- __-m/-\-metadata__: The dataset will load project metadata from the registry. Registry must be set.
	- __-v/-\-versions__: The dataset will load project versions of the specified type. Valid types depend on the registry, but may include all *(default)*, releases, tags, major, minor. *Incomplete.*
	- __-h/-\-header__: A whitespace-separated string of words representing column headers in a csv. Words are by default assumed to relate to project attributes; for version attributes, prepend "v." to the beginning.
	Example: "name v.version_str" would read in the first column as project.name and the second column as version.version_str.

	---

- **meta** [-n name] [-v version] [-d description] [-r readme] [-a author] [-e email]
Sets the dataset's metadata.

	**Options:**
	- __-n/-\-name__: Dataset name.
	- __-v/-\-version__: Dataset version.
	- __-d/-\-description__: Dataset description *(string)*.
	- __-r/-\-readme__: Markdown readme *(string)*.
	- __-a/-\-author__: Author's name. Defaults to git user.name.
	- __-e/-\-email__: Author's email. Defaults to git user.email.

	---

- **save** filepath
Saves the dataset to a json file. *Note: The registry must be set, as the current save function examines the registry to determine which json output type to save.*

	**Arguments:**
	- __filepath__: Path to the json file to be created/overwritten.

	---

- **head** N [-p/-v]
Trims all but the first N projects or versions.

	**Arguments:**
	- __N__: The number of projects/versions to keep.
	
	**Options:**
	- __[-p/-\-projects | -v/-\-versions]__: Specifies if the dataset should trim projects or if each project should trim versions.

	---

- **sample** N [-p/-v]
Samples N projects or versions without replacement.

	**Arguments:**
	- __N__: The number of projects/versions to sample.
	
	**Options:**
	- __[-p/-\-projects | -v/-\-versions]__: Specifies if the dataset should pick a sample of projects or if each project should pick a sample of versions.

	---

- **sort** "sort_str"
Sorts the dataset's projects and versions by the given sort string.

	**Arguments:**
	- __sort_str__: A whitespace-separated string of words representing various project/version attributes. Words are by default assumed to relate to project attributes; for version attributes, prepend "v." to the beginning. Sort order is ascending by default; order can be specified using "asc"/"desc".
		Example: "name desc v.version_str" would sort first on ascending project.name, then descending version.version_str.

## To Do
- Complete github registry. Still looking for a library that'll let us download project metadata. [Pydriller](https://github.com/ishepard/pydriller) only provides version info.

- Complete npm registry. Still looking for a list of top npm projects. Maybe [npm rank](https://gist.github.com/anvaka/8e8fa57c7ee1350e3491)?

- Consider moving historical to its own command, where you have to specify which attribute to filter on and the type of attribute it is? eg, "historical v.version semver". This would be nice, but would result in dataset.get_versions() loading ALL versions on the outset, even if you're then going to filter to just the latest version. Pulling all versions can be extremely slow.

- Consider revising the save code so that it's not dependent looking at the dataset.registry.name. Instead, justincludeargument that indicates what output type you want (eg, 'gitrepo' or 'gitrepocommit')? Could then get rid of the mandatory registry.name attr, as only the json.save() code depends on it.

- Clean up documentation and add help text to the CLI.
