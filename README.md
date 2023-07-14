# tox-pyenv

> tox 4 delegates the Python discovery job to virtualenv: tox.wiki/en/latest/plugins.html#tox-get-python-executable
> A special tox plugin like this is no longer needed.

> How to migrate:

> Uninstall tox-pyenv.
> Install virtualenv-pyenv.
> Set the discovery mechanism to pyenv. Both export VIRTUALENV_DISCOVERY=pyenv in a shell and setenv = VIRTUALENV_DISCOVERY=pyenv in a tox config do the job. Another option is a virtualenv.ini config file: virtualenv.pypa.io/en/latest/cli_interface.html#conf-file


[![latest](https://img.shields.io/pypi/v/tox-pyenv.svg)](https://pypi.python.org/pypi/tox-pyenv)
[![Circle CI](https://circleci.com/gh/samstav/tox-pyenv/tree/master.svg?style=shield)](https://circleci.com/gh/samstav/tox-pyenv/tree/master)  

Plugin that tells [tox](https://tox.readthedocs.org/en/latest/) to use [`pyenv which`](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-which) to [find python executables](https://testrun.org/tox/latest/plugins.html#tox.hookspecs.tox_get_python_executable)

### Why does this exist?

See the full story here https://github.com/samstav/circleci-python-sandbox/issues/1


### Your project's [circle.yml](https://circleci.com/docs/configuration)

In order for `tox` to have the versions of python you want available, set them using [`pyenv local`](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-local)

```yaml
dependencies:
  override:
    - pip install tox tox-pyenv
    - pyenv local 2.7.9 3.4.3 3.5.0
```

The versions passed to `pyenv local` must be [installed](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-install) for this to work. See [CircleCI Preinstalled Python Versions](#circleci-preinstalled-python-versions) for a list.

### Corresponding [tox.ini](https://tox.readthedocs.org/en/latest/config.html)

```ini
[tox]
envlist = py27,py34,py35
```

The result of the setup above means running `tox` will run tests against python 2.7.9, python 3.4.3 and python 3.5.0, assuming those versions of python have been [`pyenv install`ed](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-install)

### Notes

If you want tox to _exclusively_ use `pyenv which` to find executables, you will need use the `--tox-pyenv-no-fallback` command line option, or set `tox_pyenv_fallback=False` in your tox.ini. By default, if `tox-pyenv` fails to find a python executable it will fallback to tox's built-in strategy.

### CircleCI Preinstalled Python Versions

Here is the list of python versions that are *pre-installed* in the CircleCI build environment (as of 09/27/2017):

```
$ pyenv versions
  system
  2.6.6
  2.6.8
  2.7
  2.7.10
  2.7.11
  2.7.3
  2.7.4
  2.7.5
  2.7.6
  2.7.7
  2.7.8
* 2.7.9 (set by /home/ubuntu/.pyenv/version)
  3.1.5
  3.2
  3.2.5
  3.3.0
  3.3.2
  3.3.3
  3.4.0
  3.4.1
  3.4.2
  3.4.3
  3.5.0
  pypy-2.2.1
  pypy-2.3.1
  pypy-2.4.0
  pypy-2.5.0
```

If the version you need isn't in the list, such as Python `3.6-dev` include an `install` step:

```
dependencies:
  override:
    - pip install tox tox-pyenv
    - pyenv install --skip-existing 3.6-dev
    - pyenv local 3.6-dev
```
