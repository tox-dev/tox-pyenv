tox-pyenv
=========

| |latest|  |Circle CI|

Plugin that tells `tox <https://tox.readthedocs.org/en/latest/>`__ to
use `pyenv which <https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-which>`__
to `find python
executables <https://testrun.org/tox/latest/plugins.html#tox.hookspecs.tox_get_python_executable>`__

Your project's `circle.yml <https://circleci.com/docs/configuration>`__
#########################################################################

In order for ``tox`` to have the versions of python you want available,
set them using
`pyenv local <https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-local>`__

.. code:: yaml

    dependencies:
      override:
        - pip install tox tox-pyenv
        - pyenv local 2.7.9 3.4.3 3.5.0

The versions passed to ``pyenv local`` must be
`installed <https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-install>`__
for this to work. Check out the list of python versions that are
pre-installed in the CircleCI build environment:
https://circleci.com/docs/environment#python

Corresponding `tox.ini <https://tox.readthedocs.org/en/latest/config.html>`__
###############################################################################

.. code:: ini

    [tox]
    envlist = py27,py34,py35

The result of the setup above means running ``tox`` will run tests
against python 2.7.9, python 3.4.3 and python 3.5.0, assuming those
versions of python have been
`pyenv install <https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-install>`__\ed.

notes
########

If you want tox to *exclusively* use ``pyenv which`` to find
executables, you will need use the ``--tox-pyenv-no-fallback`` command
line option, or set ``tox_pyenv_fallback=False`` in your tox.ini. By
default, if ``tox-pyenv`` fails to find a python executable it will
fallback to tox's built-in strategy.

.. |latest| image:: https://img.shields.io/pypi/v/tox-pyenv.svg
   :target: https://pypi.python.org/pypi/tox-pyenv
.. |Circle CI| image:: https://circleci.com/gh/samstav/tox-pyenv/tree/master.svg?style=shield
   :target: https://circleci.com/gh/samstav/tox-pyenv/tree/master

