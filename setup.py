# -*- coding: utf-8 -*-

version = '0.1'

from setuptools import setup, find_packages

long_description = ("")

setup(name='matinbonheur.core',
      version=version,
      description='Matin bonheur core package',
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
      ],
      keywords='',
      author="Gillian 'Schminitz' Sampont",
      author_email='gillian.sampont@gmail.com',
      url='https://github.com/schminitz/',
      license='gpl',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'Plone',
      ],
      extras_require={
      },
      entry_points={},
      )
