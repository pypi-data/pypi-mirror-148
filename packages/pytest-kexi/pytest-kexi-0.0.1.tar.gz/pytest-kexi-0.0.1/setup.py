from setuptools import setup

setup(
    name="pytest-kexi",
    packages=["pytest_kexi"],
    # the following makes a plugin available to pytest
    entry_points={"pytestkx": ["name_of_plugin = pytest_kexi.pytest_kexi"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)