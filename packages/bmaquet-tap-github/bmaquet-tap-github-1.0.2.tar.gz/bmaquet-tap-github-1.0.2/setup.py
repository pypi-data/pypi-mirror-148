#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='bmaquet-tap-github',
      version='1.0.2',
      url='https://github.com/BenjMaq/bmaquet-tap-github',
      description='Singer.io tap for extracting data from the GitHub API',
      author='Stitch',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_github'],
      install_requires=[
          'singer-python==5.12.0',
          'requests==2.20.0'
      ],
      extras_require={
          'dev': [
              'pylint',
              'ipdb',
              'nose',
          ]
      },
      entry_points='''
          [console_scripts]
          tap-github=tap_github:main
      ''',
      packages=['tap_github'],
      package_data = {
          'tap_github': ['tap_github/schemas/*.json']
      },
      include_package_data=True
)
