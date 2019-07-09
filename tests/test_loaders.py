from structures import Dataset
from dotenv import load_dotenv


def test_json():
    # test github
    ds = Dataset('github')
    ds.set_meta('test', '1.0')
    ds.load_file('files/git_repo.json')
    test = ds.to_inputset()
    ds.load_file('files/git_repo_commit.json')
    ds.save('../test.json')

    # test npm
    ds = Dataset('npm')
    ds.set_meta('test', '1.0')
    ds.load_file('files/name_version.json')
    ds.save('../test.json')

    # test pypi
    ds = Dataset('pypi')
    ds.set_meta('test', '1.0')
    ds.load_file('files/name_version.json')
    ds.save('../test.json')

    # test vanilla
    ds = Dataset()
    ds.set_meta('test', '1.0')
    ds.load_file('files/http_url.json')
    ds.save('../test.json')

    temp = 5


def test_csv():
    # test github
    ds = Dataset('github')
    ds.set_meta('test', '1.0')
    ds.load_file('files/git_urls_commits.csv')
    ds.save('../test.json')

    # test npm
    ds = Dataset('npm')
    ds.set_meta('test', '1.0')
    ds.load_file('files/names_versions.csv')
    ds.save('../test.json')

    # test pypi
    ds = Dataset('pypi')
    ds.set_meta('test', '1.0')
    ds.load_file('files/names_versions.csv')
    ds.save('../test.json')

    # test vanilla
    ds = Dataset()
    ds.set_meta('test', '1.0')
    ds.load_file('files/urls.csv')
    ds.save('../test.json')

    temp = 5


def test_weblist():
    load_dotenv()

    # test github
    ds = Dataset('github')
    ds.set_meta('test', '1.0')
    ds.load_weblist('top1kstarred')
    ds.head(10)
    ds.get_project_versions('latest')
    ds.save('../test.json')

    # test pypi
    ds = Dataset('pypi')
    ds.set_meta('test', '1.0')
    ds.load_weblist('top5kyear')
    ds.head(10)
    ds.get_project_versions('latest')
    ds.save('../test.json')

    temp = 5
