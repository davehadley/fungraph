from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("fungraph/_version.py") as fp:
    version = {}
    exec(fp.read(), version)
    version = version["__version__"]

setup(name="fungraph",
      version=version,
      description="Graph of lazily evaluated functions with Automatically Cached Intermediates",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/davehadley/fungraph",
      author="David Hadley",
      author_email="d.r.hadley@warwick.ac.uk",
      license="MIT",
      packages=["fungraph"],
      install_requires=["dask>=2.20.0", "graphchain>=1.1.0"],
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