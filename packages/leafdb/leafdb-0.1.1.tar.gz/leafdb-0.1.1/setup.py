#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from leafdb import __version__

setup(
  name='leafdb',
  version=__version__,
  description='LeafDb library',
  author='Huaqing Ye',
  author_email='veginer@gmail.com',
  url='http://leafdb.leafpy.org/',
  py_modules=['leafdb'],
  #packages=['.'],
  long_description="LeafDb is a simple library for makeing raw SQL queries to most relational databases.",
  license="MIT license",
  platforms=["any"],
)
