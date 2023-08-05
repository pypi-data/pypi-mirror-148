
"""Get dupdict_mod onto pypi."""

from setuptools import setup

setup(
    name="dupdict_mod",
    version="1.1.1",
    py_modules=['dupdict_mod'],

    # metadata for upload to PyPI
    author="Daniel Richard Stromberg",
    author_email="strombrg@gmail.com",
    description='Pure Python dictionary wrapper that allows duplicates',
    long_description="""
A Pure Python dictionary wrapper that allows duplicate keys is provided.

It passes pylint, passes pep8, is thoroughly unit tested, and runs on CPython 3.3 - 3.10,
Pypy3 3.9 7.3.9.

It can wrap a python dict(), https://pypi.org/project/treap/ or https://pypi.org/project/red-black-tree-mod/ - among other
things.
""",
    license="Apache v2",
    keywords="dictionary duplicate keys",
    url='http://stromberg.dnsalias.org/~strombrg/dupdict_mod/',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 3",
         ],
)
