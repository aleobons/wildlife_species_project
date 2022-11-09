"""Setup script for package."""
from setuptools import find_packages
from setuptools import setup

# What packages are required for this module to be executed?
def list_reqs(fname="requirements.txt"):
    with open(fname) as fd:
        return fd.read().splitlines()


setup(
    name="project",
    version="0.1.0",
    install_requires=list_reqs(),
    packages=find_packages(include=["project", "project.*"]),
    description="project Library",
    entry_points={},
)
