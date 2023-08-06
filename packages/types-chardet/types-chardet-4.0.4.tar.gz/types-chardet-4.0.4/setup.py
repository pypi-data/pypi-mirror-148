from setuptools import setup

name = "types-chardet"
description = "Typing stubs for chardet"
long_description = '''
## Typing stubs for chardet

This is a PEP 561 type stub package for the `chardet` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `chardet`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/chardet. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `f7aa41245e2bc688ae3fe6d5bd1008f0baf8d8e0`.
'''.lstrip()

setup(name=name,
      version="4.0.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/chardet.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['chardet-stubs'],
      package_data={'chardet-stubs': ['__init__.pyi', 'enums.pyi', 'langbulgarianmodel.pyi', 'langcyrillicmodel.pyi', 'langgreekmodel.pyi', 'langhebrewmodel.pyi', 'langhungarianmodel.pyi', 'langthaimodel.pyi', 'langturkishmodel.pyi', 'universaldetector.pyi', 'version.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
