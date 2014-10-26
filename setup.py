version = '0.5.0'

import sys, os
try:
    from setuptools import setup, Extension, Command, find_packages
except ImportError:
    from distutils.core import setup, Extension, Command, find_packages
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, \
    DistutilsPlatformError


IS_PYPY = hasattr(sys, 'pypy_translation_info')

# code from simplejson
if sys.platform == 'win32' and sys.version_info > (2, 6):
   # 2.6's distutils.msvc9compiler can raise an IOError when failing to
   # find the compiler
   # It can also raise ValueError http://bugs.python.org/issue7511
   ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError,
                 IOError, ValueError)
else:
   ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

class BuildFailed(Exception):
    pass

class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()



def run_setup(with_binary):
    if with_binary:
        kw = dict(
            ext_modules = [
                Extension("oktavia._bitvector", ["oktavia/_bitvector.cpp"]),
            ],
            cmdclass = dict(build_ext=ve_build_ext),
        )
    else:
        kw = dict()
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
          **kw)

try:
    run_setup(not IS_PYPY)
except BuildFailed:
    BUILD_EXT_WARNING = ("WARNING: The C extension could not be compiled, "
                         "speedups are not enabled.")
    print('*' * 75)
    print(BUILD_EXT_WARNING)
    print("Failure information, if any, is above.")
    print("I'm retrying the build without the C extension now.")
    print('*' * 75)

    run_setup(False)

    print('*' * 75)
    print(BUILD_EXT_WARNING)
    print("Plain-Python installation succeeded.")
    print('*' * 75)
