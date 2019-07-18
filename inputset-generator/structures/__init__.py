from .dataset import Dataset
from .projects import Project, DefaultProject, project_map
from .versions import Version, DefaultVersion, version_map


# check to ensure project/version map keys match
assert project_map.keys() == version_map.keys(), (
    'R2C input set generator init failure: '
    'Project_map and version_map must have the same map keys.')
