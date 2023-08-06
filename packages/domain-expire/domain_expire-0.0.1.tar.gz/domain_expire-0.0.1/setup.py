#!/usr/bin/env python

from distutils.core import setup

setup(name='domain_expire',
      version='0.0.1',
      description='check domain near expire date',
      author='Alexander.Li',
      author_email='superpowerlee@gmaial.com',
      url='https://github.com/ipconfiger/domain-expire',
      packages=['domain_expire'],
      install_requires=[
          'pytz',
          'pyopenssl'
      ]
      )
