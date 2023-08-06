from setuptools import setup

name = "types-emoji"
description = "Typing stubs for emoji"
long_description = '''
## Typing stubs for emoji

This is a PEP 561 type stub package for the `emoji` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `emoji`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/emoji. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `f7aa41245e2bc688ae3fe6d5bd1008f0baf8d8e0`.
'''.lstrip()

setup(name=name,
      version="1.2.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/emoji.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['emoji-stubs'],
      package_data={'emoji-stubs': ['__init__.pyi', 'core.pyi', 'unicode_codes/__init__.pyi', 'unicode_codes/en.pyi', 'unicode_codes/es.pyi', 'unicode_codes/it.pyi', 'unicode_codes/pt.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
