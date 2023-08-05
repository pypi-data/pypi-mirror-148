
"""Pypi stuff."""

from setuptools import setup

setup(
    name="dupdict_mod",
    version="1.1",
    py_modules=['dupdict_mod'],

    # metadata for upload to PyPI
    author="Daniel Richard Stromberg",
    author_email="strombrg@gmail.com",
    description='Pure Python dictionary wrapper that allows duplicates',
    long_description='''
A Pure Python dictionary wrapper that allows duplicate keys is provided.

It passes pylint, pyflakes, pycodestyle and pydocstyle, is thoroughly unit tested, and runs
on CPython 3.3 - 3.10 and Pypy 3.9 7.3.9.
''',
    license="Apache v2",
    keywords="dictionary duplicate keys",
    url='http://stromberg.dnsalias.org/~strombrg/dupdict_mod/',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         ],
)
