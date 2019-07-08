from structures import Dataset
from dotenv import load_dotenv


def test_json():
    # test github
    ds = Dataset('github')
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/git_repo.json')
    test = ds.to_inputset()
    ds.load_file('../tests/files/git_repo_commit.json')
    test = ds.to_inputset()

    # test npm
    ds = Dataset('npm')
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/name_version.json')
    test = ds.to_inputset()

    # test pypi
    ds = Dataset('pypi')
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/name_version.json')
    test = ds.to_inputset()

    # test vanilla
    ds = Dataset()
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/http_url.json')
    test = ds.to_inputset()

    temp = 5


def test_csv():
    # test github
    ds = Dataset('github')
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/git_urls_commits.csv')
    test = ds.to_inputset()

    # test npm
    ds = Dataset('npm')
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/names_versions.csv')
    test = ds.to_inputset()

    # test pypi
    ds = Dataset('pypi')
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/names_versions.csv')
    test = ds.to_inputset()

    # test vanilla
    ds = Dataset()
    ds.set_meta('test', '1.0')
    ds.load_file('../tests/files/urls.csv')
    test = ds.to_inputset()

    temp = 5


def test_weblist():
    load_dotenv()

    # test github
    ds = Dataset('github')
    ds.set_meta('test', '1.0')
    ds.load_weblist('top1kstarred')
    ds.head(10)
    ds.get_project_versions('latest')
    test = ds.to_inputset()

    # test pypi
    ds = Dataset('pypi')
    ds.set_meta('test', '1.0')
    ds.load_weblist('top5kyear')
    ds.head(10)
    ds.get_project_versions('latest')
    test = ds.to_inputset()

    temp = 5
