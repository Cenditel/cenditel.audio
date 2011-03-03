# -*- coding: utf-8 -*-
"""
This module contains the tool of cenditel.audio
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('cenditel', 'audio', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(name='Cenditel Foundation Audio Format Specification',
      version=version,
      description="This package provide a aditional content type that provide audio streaming using HTML5",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Plone',
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone, product, content type, audio, html5',
      author='Victor Terán',
      author_email='elalcon89@gmail.com',
      maintainer='Leonardo J. Caballero G.',
      maintainer_email='leonardocaballero@gmail.com',
      url='http://svn.plone.org/svn/collective/cenditel.audio',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cenditel', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'cenditel.transcodedeamon',
          'cenditel.multimediaplayertheme',
          'collective.javascript.jqueryui==1.8.4'
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='cenditel.audio.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
