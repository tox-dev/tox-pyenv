#!/usr/bin/env python

from os.path import dirname as _dirn
from os.path import join as _join
from os.path import realpath as _realp
from setuptools import setup


with open(_join(_dirn(_realp(__file__)), 'tox_pyenv.py'), 'r') as abt:
    marker, about, abt = '# __about__', {}, abt.read()
    assert abt.count('# __about__') == 2
    abt = abt[abt.index(marker):abt.rindex(marker)]
    exec(abt, about)


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
    'classifiers': CLASSIFIERS,
    'description': about['__summary__'],
    'entry_points': ENTRY_POINTS,
    'install_requires': INSTALL_REQUIRES,
    'keywords': ' '.join(about['__keywords__']),
    'license': about['__license__'],
    'maintainer_email': about['__email__'],
    'name': about['__title__'],
    'py_modules': ['tox_pyenv'],
    'url': about['__url__'],
    'version': about['__version__'],
}

setup(**package_attributes)
