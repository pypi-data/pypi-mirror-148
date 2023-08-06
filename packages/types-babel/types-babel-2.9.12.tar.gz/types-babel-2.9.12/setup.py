from setuptools import setup

name = "types-babel"
description = "Typing stubs for babel"
long_description = '''
## Typing stubs for babel

This is a PEP 561 type stub package for the `babel` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `babel`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/babel. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `f7aa41245e2bc688ae3fe6d5bd1008f0baf8d8e0`.
'''.lstrip()

setup(name=name,
      version="2.9.12",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/babel.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pytz'],
      packages=['babel-stubs'],
      package_data={'babel-stubs': ['__init__.pyi', '_compat.pyi', 'core.pyi', 'dates.pyi', 'languages.pyi', 'lists.pyi', 'localedata.pyi', 'localtime/__init__.pyi', 'localtime/_unix.pyi', 'localtime/_win32.pyi', 'messages/__init__.pyi', 'messages/catalog.pyi', 'messages/checkers.pyi', 'messages/extract.pyi', 'messages/frontend.pyi', 'messages/jslexer.pyi', 'messages/mofile.pyi', 'messages/plurals.pyi', 'messages/pofile.pyi', 'numbers.pyi', 'plural.pyi', 'support.pyi', 'units.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
