from structures import Dataset
from dotenv import load_dotenv


def test_import_inputset():
    # test github
    ds = Dataset.import_inputset(
        'files/git_repo.json',
        registry='github',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    ds = Dataset.import_inputset(
        'files/git_repo_commit.json',
        registry='github',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test npm
    ds = Dataset.import_inputset(
        'files/name_version.json',
        registry='npm',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test pypi
    ds = Dataset.import_inputset(
        'files/name_version.json',
        registry='pypi',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test vanilla
    ds = Dataset.import_inputset(
        'files/http_url.json',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    temp = 5


def test_load_file():
    # test github
    ds = Dataset.load_file(
        'files/git_urls_commits.csv',
        registry='github',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test npm
    ds = Dataset.load_file(
        'files/names_versions.csv',
        registry='npm',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test pypi
    ds = Dataset.load_file(
        'files/names_versions.csv',
        registry='pypi',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test vanilla
    ds = Dataset.load_file(
        'files/urls.csv',
        cache_dir='../cache'
    )
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    temp = 5


def test_load_weblist():
    load_dotenv()

    # test github
    ds = Dataset.load_weblist(
        'top1kstarred',
        registry='github',
        cache_dir='../cache'
    )
    ds.trim(10)
    ds.get_project_versions('latest')
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test npm
    ds = Dataset.load_weblist(
        'allbydependents',
        registry='npm',
        cache_dir='../cache'
    )
    ds.trim(10)
    ds.get_project_versions('latest')
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test pypi
    ds = Dataset.load_weblist(
        'top5kyear',
        registry='pypi',
        cache_dir='../cache'
    )
    ds.trim(10)
    ds.get_project_versions('latest')
    ds.set_meta('test', '1.0')
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    temp = 5
