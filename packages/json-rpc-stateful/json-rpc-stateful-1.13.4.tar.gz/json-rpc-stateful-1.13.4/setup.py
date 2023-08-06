#!/usr/bin/env python
import os.path
import sys
from setuptools import setup, find_packages


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup_requires = ["pytest-runner"] if sys.argv in ['pytest', 'test'] else []

setup(
    name="json-rpc-stateful",
    version="1.13.4",
    packages=find_packages(),
    setup_requires=setup_requires,
    tests_require=["pytest"],

    # metadata for upload to PyPI
    author="Vladislav Rozhkov",
    author_email="rozhkov.2006@gmail.com",
    url="https://github.com/vladd11/json-rpc",
    description="JSON-RPC transport implementation",
    long_description=read('README.rst'),

    # Full list:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
)
