import setuptools as setuptools
from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytest-kexi",
    # the following makes a plugin available to pytest
    entry_points={"pytestkx": ["name_of_plugin = pytest_kexi.pytest_kexi"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)


