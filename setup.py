# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
version = open(os.path.join(here, 'VERSION.txt')).readline().rstrip()

setup(name='pyforth',
      version=version,
      description='Forth implementation in Python',
      long_description=README,
      classifiers=[],
      keywords='forth virtual machine',
      author='Jose Dinuncio',
      author_email='jdinunci@uc.edu.ve',
      url='http://github.com/jdinuncio/repoze.what.plugins.ini/tree/master',
      license='GPL',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=['nose'],
      test_suite="nose.collector",
      install_requires=[],
      entry_points="""\
      """,
      )
