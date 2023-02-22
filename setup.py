from os import path

from setuptools import find_packages, setup

pkg_name = "workflow_volume"
here = path.abspath(path.dirname(__file__))

long_description = """
# Workflow for volumetric data
"""

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, "version.py")) as f:
    exec(f.read())

setup(
    name="workflow-volume",
    version=__version__,  # noqa: F821
    description="DataJoint Workflow for Element Volume",
    long_description=long_description,
    author="DataJoint",
    author_email="info@datajoint.com",
    license="MIT",
    url="https://github.com/datajoint/workflow-volume",
    keywords="neuroscience volumetric BossDB datajoint",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=requirements,
)
