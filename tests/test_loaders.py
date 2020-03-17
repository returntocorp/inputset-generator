import os
from dotenv import load_dotenv

from dataset import Dataset


load_dotenv()

CACHE_DIR = '../.requests_cache'


def test_import_inputset():
    # test github
    ds = Dataset.import_inputset(
        'files/git_repo.json',
        registry='github',
        cache_dir=CACHE_DIR,
        debug=True,
        github_pat=os.getenv('GITHUB_PAT')
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    ds = Dataset.import_inputset(
        'files/git_repo_commit.json',
        registry='github',
        cache_dir=CACHE_DIR,
        debug=True,
        github_pat=os.getenv('GITHUB_PAT')
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test npm
    ds = Dataset.import_inputset(
        'files/name_version.json',
        registry='npm',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test pypi
    ds = Dataset.import_inputset(
        'files/name_version.json',
        registry='pypi',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test vanilla
    ds = Dataset.import_inputset(
        'files/http_url.json',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # cleanup files
    os.remove('../test.p')
    os.remove('../test.json')


def test_load_file():
    # test github
    ds = Dataset.load_file(
        'files/git_urls_commits.csv',
        registry='github',
        cache_dir=CACHE_DIR,
        debug=True,
        github_pat=os.getenv('GITHUB_PAT')
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test npm
    ds = Dataset.load_file(
        'files/names_versions.csv',
        registry='npm',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test pypi
    ds = Dataset.load_file(
        'files/names_versions.csv',
        registry='pypi',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test vanilla
    ds = Dataset.load_file(
        'files/urls.csv',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # cleanup files
    os.remove('../test.p')
    os.remove('../test.json')


def test_load_weblist():
    # test github
    ds = Dataset.load_web(
        'top1kstarred',
        registry='github',
        from_type='list',
        cache_dir=CACHE_DIR,
        debug=True,
        github_pat=os.getenv('GITHUB_PAT')
    )
    ds.trim(10)
    ds.get_projects_meta()
    ds.get_project_versions(historical='latest')
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test npm
    ds = Dataset.load_web(
        'allbydependents',
        registry='npm',
        from_type='list',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.trim(10)
    ds.get_projects_meta()
    ds.get_project_versions(historical='latest')
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # test pypi
    ds = Dataset.load_web(
        'top4kyear',
        registry='pypi',
        from_type='list',
        cache_dir=CACHE_DIR,
        debug=True
    )
    ds.trim(10)
    ds.get_projects_meta()
    ds.get_project_versions(historical='latest')
    ds.update(**{'name': 'test', 'version': '1.0'})
    ds.backup('../test.p')
    ds = Dataset.restore('../test.p')
    ds.export_inputset('../test.json')

    # cleanup files
    os.remove('../test.p')
    os.remove('../test.json')
