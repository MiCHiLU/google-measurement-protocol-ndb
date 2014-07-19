#! /usr/bin/env python
from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(name='google-measurement-protocol-ndb',
      author='ENDOH takanao',
      author_email='djmchl@gmail.com',
      description=('A Python implementation of'
                   ' Google Analytics Measurement Protocol'
                   ' for Google App Engine NDB'),
      license='BSD',
      version='0.1.3',
      packages=['google_measurement_protocol'],
      test_suite='google_measurement_protocol.tests',
      tests_require=['pytest-cov>=1.7,<1.8a0', 'minimock>=1.2,<1.3a0', 'prices>=0.5,<0.6a0'],
      classifiers=CLASSIFIERS,
      platforms=['any'])
