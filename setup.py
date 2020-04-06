##############################################################################
#
# Copyright (c) 2008-2011 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'pyramid>=1.5.0', # various b/w compat choices
    'venusian>=1.0', # liftid / scope in callbacks
    'zope.configuration>=3.8.0dev', # dict actions
]

tests_require = install_requires + ['pyramid_mako', 'WebTest']

testing_extras = ['pyramid_mako', 'WebTest']

docs_extras = [
    'pylons-sphinx-themes',
    'repoze.sphinx.autointerface',
    'Sphinx >= 1.3.1',
    ]

setup(name='pyramid_zcml',
      version='1.1.0-dev0',
      description='Zope Config Markup Language support for Pyramid',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "License :: Repoze Public License",
        ],
      keywords='web wsgi pylons pyramid',
      author="Chris McDonough, Agendaless Consulting",
      author_email="pylons-discuss@googlegroups.com",
      url="https://docs.pylonsproject.org/projects/pyramid_zcml/en/latest/",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires,
      tests_require = tests_require,
      test_suite="pyramid_zcml",
      extras_require = {
          'testing': testing_extras,
          'docs': docs_extras,
          },
      entry_points = """
      [paste.paster_create_template]
      pyramid_starter_zcml=pyramid_zcml.scaffolds:StarterZCMLProjectTemplate
      [pyramid.scaffold]
      pyramid_starter_zcml=pyramid_zcml.scaffolds:StarterZCMLProjectTemplate
      """
      )
