#! /usr/bin/env python

from setuptools import setup, find_packages



setup(name='aimpy',
      version='0.1',
      description='Odds and ends in python',
      url='http://bitbucket.org/aimerson/aimpy',
      author='Alex Merson',
      author_email='alex.i.merson@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_dir={'aimpy':'aimpy'},
      zip_safe=False)

