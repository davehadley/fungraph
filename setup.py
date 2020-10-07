from typing import Dict

from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("fungraph/_version.py") as fp:
    variables: Dict[str, str] = {}
    exec(fp.read(), variables)
    version = variables["__version__"]

setup(
    name="fungraph",
    version=version,
    description="Graph of lazily evaluated functions with automatically cached "
    "intermediates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davehadley/fungraph",
    author="David Hadley",
    author_email="d.r.hadley@warwick.ac.uk",
    license="MIT",
    packages=["fungraph", "fungraph.internal"],
    install_requires=[
        "dask>=2.20.0",
        "cloudpickle>=1.4.1",
        "filelock>=3.0.12",
        "toolz>=0.10.0",
        "distributed>=2.20.0",
        "joblib>=0.14.1",
    ],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: POSIX",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.6",
)
