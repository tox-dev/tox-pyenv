#!/usr/bin/env python

import os
from setuptools import setup
import subprocess
import sys


here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, 'tox_pyenv.py'), 'r') as abt:
    marker, about, abt = '# __about__', {}, abt.read()
    assert abt.count(marker) == 2
    abt = abt[abt.index(marker):abt.rindex(marker)]
    exec(abt, about)


# Add the commit hash to the keywords for sanity.
if any(k in ' '.join(sys.argv).lower() for k in ['upload', 'dist']):
    try:
        current_commit = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    else:
        if current_commit and len(current_commit) == 40:
            about['__keywords__'].append(current_commit[:8])


# pandoc --from=markdown_github --to=rst README.md --output=README.rst
with open(os.path.join(here, 'README.rst')) as rdme:
    LONG_DESCRIPTION = rdme.read()


ENTRY_POINTS = {
    'tox': [
        'pyenv = tox_pyenv',
    ]
}

INSTALL_REQUIRES = [
    'tox>=2.0'
]

TESTS_REQUIRE = [
    'mock>=2.0.0',
    'pycodestyle>=2.3.1',
    'pylint>=1.7.2',
]

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]


package_attributes = {
    'author': about['__author__'],
    'author_email': about['__email__'],
    'classifiers': CLASSIFIERS,
    'description': about['__summary__'],
    'entry_points': ENTRY_POINTS,
    'install_requires': INSTALL_REQUIRES,
    'keywords': ' '.join(about['__keywords__']),
    'license': about['__license__'],
    'long_description': LONG_DESCRIPTION,
    'name': about['__title__'],
    'tests_require': TESTS_REQUIRE,
    'py_modules': ['tox_pyenv'],
    'url': about['__url__'],
    'version': about['__version__'],
}

setup(**package_attributes)
