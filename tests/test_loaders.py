from structures import Dataset


def test_json():
    # test github
    ds = Dataset('github')
    ds.load_file('../tests/files/git_repo.json')
    ds.load_file('../tests/files/git_repo_commit.json')

    # test npm
    ds = Dataset('npm')
    ds.load_file('../tests/files/name_version.json')

    # test pypi
    ds = Dataset('pypi')
    ds.load_file('../tests/files/name_version.json')

    # test noreg
    ds = Dataset()
    ds.load_file('../tests/files/http_url.json')


def test_csv():
    # test github
    ds = Dataset('github')
    ds.load_file('../tests/files/git_urls_commits.csv')

    # test npm
    ds = Dataset('npm')
    ds.load_file('../tests/files/names_versions.csv')

    # test pypi
    ds = Dataset('pypi')
    ds.load_file('../tests/files/names_versions.csv')

    # test noreg
    ds = Dataset()
    ds.load_file('../tests/files/names_versions.csv')


def test_weblist():
    # test github
    ds = Dataset('github')
    ds.load_weblist('top100starred')

    # test pypi
    ds = Dataset('pypi')
    ds.load_weblist('top5kyear')
