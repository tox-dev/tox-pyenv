# tox-pyenv
[![latest](https://img.shields.io/pypi/v/tox-pyenv.svg)](https://pypi.python.org/pypi/tox-pyenv)
[![Circle CI](https://circleci.com/gh/samstav/tox-pyenv/tree/master.svg?style=shield)](https://circleci.com/gh/samstav/tox-pyenv/tree/master)  

Plugin that tells [tox](https://tox.readthedocs.org/en/latest/) to use [`pyenv which`](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-which) to [find python executables](https://testrun.org/tox/latest/plugins.html#tox.hookspecs.tox_get_python_executable)

#### Your project's [circle.yml](https://circleci.com/docs/configuration)

In order for `tox` to have the versions of python you want available, set them using [`pyenv local`](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-local)

```yaml
dependencies:
  override:
    - pip install tox tox-pyenv
    - pyenv local 2.7.9 3.4.3 3.5.0
```

#### Corresponding [tox.ini](https://tox.readthedocs.org/en/latest/config.html)

```ini
[tox]
envlist = py27,py34,py35
```

The result of the setup above means running `tox` will run tests against python 2.7.9, python 3.4.3 and python 3.5.0
