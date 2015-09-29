#!/usr/bin/env python

from os.path import dirname as _dirn
from os.path import join as _join
from os.path import realpath as _realp
from setuptools import setup
import subprocess
import sys


with open(_join(_dirn(_realp(__file__)), 'tox_pyenv.py'), 'r') as abt:
    marker, about, abt = '# __about__', {}, abt.read()
    assert abt.count('# __about__') == 2
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


ENTRY_POINTS = {
    'tox': [
        'pyenv = tox_pyenv',
    ]
}

INSTALL_REQUIRES = [
    'tox>=2.0'
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
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
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
    'name': about['__title__'],
    'py_modules': ['tox_pyenv'],
    'url': about['__url__'],
    'version': about['__version__'],
}

setup(**package_attributes)
