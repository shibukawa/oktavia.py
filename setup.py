from setuptools import setup, find_packages
import sys, os

version = '0.4.3'

setup(name='oktavia',
      version=version,
      description="High performance pure Python/JavaScript search engine",
      long_description="""This is search engine is pure Python/JavaScript on-memory search engine.

* It uses FM-Index as an algorithm.
* It is good for eastern asian languages (CJK) because it doesn't use an invert index.
* It works on completely on memory.
* There are JavaScript index generator/search engine too. You can provide search feature to you web applications and static HTML.

""",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='search python javascript fmindex',
      author='Yoshiki Shibukawa',
      author_email='yoshiki@shibu.jp',
      url='https://github.com/shibukawa/oktavia.py/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
