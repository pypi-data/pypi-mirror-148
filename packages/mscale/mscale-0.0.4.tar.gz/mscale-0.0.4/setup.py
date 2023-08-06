import setuptools

import codecs
import os.path

# versioning handled by the first method on:
# https://packaging.python.org/guides/single-sourcing-package-version/


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mscale",
    version=get_version("src/mscale/__init__.py"),
    author="Sebastian Khan",
    author_email="sebastiank17@gmail.com",
    description="multi-scale neural network layers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SpaceTimeKhantinuum/mscale",
    project_urls={
        "Bug Tracker": "https://gitlab.com/SpaceTimeKhantinuum/mscale/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
