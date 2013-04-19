#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='cltools',
      version='0.3.0',
      description='Set of decorators of to create transform a class into a command-line tool.',
      author='Arthibus Gisséhel',
      author_email='public-dev-cltools@gissehel.org',
      url='https://github.com/gissehel/cltools.git',
      packages=['cltools'],
      license='MIT',
      keywords='commandline tools cltools decorator',
      long_description=open('README.md').read(),
      install_requires=['supertools'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Topic :: System :: Shells',
          'Topic :: Terminals',
          'Topic :: Utilities',
      ],
)
