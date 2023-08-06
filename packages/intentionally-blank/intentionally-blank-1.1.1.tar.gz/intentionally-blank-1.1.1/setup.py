"""Setup for Intentionally Blank.
"""
import io
import os

from setuptools import setup, find_packages

SOURCE = "source"


def local_file(*name):
    "Find a file relative to this directory."
    return os.path.join(os.path.dirname(__file__), *name)


def read(name, **kwargs):
    "Read the contents of a file."
    with io.open(name, encoding=kwargs.get("encoding", "utf8")) as handle:
        return handle.read()


def read_version():
    "Read the `(version-string, version-info)` from `src/evo/version.py`."
    version_file = local_file(SOURCE, "intentionally_blank", "version.py")
    local_vars = {}
    with open(version_file) as handle:
        exec(handle.read(), {}, local_vars)  # pylint: disable=exec-used
    return (local_vars["__version__"], local_vars["__version_info__"])


LONG_DESCRIPTION = read(local_file("README.rst"), mode="rt")

version = read_version()[0]

setup(
    name="intentionally-blank",
    version=version,
    packages=find_packages(SOURCE),
    author="Sixty North AS",
    author_email="rob@sixty-north.com",
    description="A tool for indentation in text files",
    license="MIT",
    keywords="",
    package_dir={"": SOURCE},
    url="https://github.com/sixty-north/intentionally-blank",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=["click", "exit_codes", "stevedore", "asq", "more-itertools"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={"test": ["hypothesis", "pytest", "tox"], "dev": ["black", "bumpversion", "twine"],},
    entry_points={
        "console_scripts": ["intentionally-blank = intentionally_blank.cli:cli",],
        'intentionally_blank.formatter': [
            'identity = intentionally_blank.ext.formatters.identity:Formatter',
            'leading = intentionally_blank.ext.formatters.leading:Formatter',
            'empty = intentionally_blank.ext.formatters.empty:Formatter',
            'visible = intentionally_blank.ext.formatters.visible:Formatter',
            'eof-newline = intentionally_blank.ext.formatters.eof_newline:Formatter',
            'python-leading = intentionally_blank.ext.formatters.python_leading:Formatter',
            'remove-trailing = intentionally_blank.ext.formatters.remove_trailing:Formatter'
        ]
    },
    long_description=LONG_DESCRIPTION,
)
