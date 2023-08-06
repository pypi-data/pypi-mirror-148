from gzip import READ
import setuptools
from pathlib import Path

setuptools.setup(
    name="sagarpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(["test", "data"])
)
