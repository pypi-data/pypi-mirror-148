from setuptools import setup

name = "types-atomicwrites"
description = "Typing stubs for atomicwrites"
long_description = '''
## Typing stubs for atomicwrites

This is a PEP 561 type stub package for the `atomicwrites` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `atomicwrites`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/atomicwrites. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `f7aa41245e2bc688ae3fe6d5bd1008f0baf8d8e0`.
'''.lstrip()

setup(name=name,
      version="1.4.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/atomicwrites.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['atomicwrites-stubs'],
      package_data={'atomicwrites-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
