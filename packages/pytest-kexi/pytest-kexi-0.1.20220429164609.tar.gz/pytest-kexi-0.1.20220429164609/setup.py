import setuptools as setuptools
from setuptools import setup


from datetime import datetime as dt

tdatetime = dt.now()
tstr = tdatetime.strftime('%Y%m%d%H%M%S')
print(tstr)
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytest-kexi",
    version="0.1.{}".format(tstr),
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["name_of_plugin = pytest_kexi.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
