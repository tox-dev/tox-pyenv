"""tox-pyenv

Plugin that hijacks the tox_get_python_executable using
tox's plugin system:

    https://testrun.org/tox/latest/plugins.html
    https://testrun.org/tox/latest/plugins.html#tox.hookspecs.tox_get_python_executable

Modified to instead use `pyenv which` to locate the
appropriate python executable. This takes the place
of the standard behavior in tox. The built-in default
for the tox_get_python_exeucutable function
is the following (for sys.platform != 'win32'):

    @hookimpl
    def tox_get_python_executable(envconfig):
        return py.path.local.sysfind(envconfig.basepython)

which uses the 'py' package's sysfind():

    https://pylib.readthedocs.org/en/latest/path.html#py._path.local.LocalPath.sysfind

If `pyenv`'s shims are not at the very front of your path,
sysfind might lookup the global system version of python
instead of preferring a version specified by using `pyenv local`
or `pyenv global`. This plugin changes the way tox finds
your python executable to exclusively use `pyenv which`.

    https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-which

"""

import subprocess

from tox import hookimpl as tox_hookimpl


# __about__
__title__ = 'tox-pyenv'
__summary__ = ('tox plugin that makes tox use `pyenv which` '
               'to find python executables')
__url__ = 'https://github.com/samstav/tox-pyenv'
__version__ = '0.0.1'
__author__ = 'Sam Stavinoha'
__email__ = 'smlstvnh@gmail.com'
__keywords__ = ['tox', 'pyenv', 'python']
__license__ = 'Apache License, Version 2.0'
# __about__


class ToxPyenvException(Exception):

    """Base class for exceptions from this plugin."""


class PyenvMissing(ToxPyenvException, RuntimeError):

    """The pyenv program is not installed."""


class PyenvWhichFailed(ToxPyenvException):

    """Calling `pyenv which` failed."""


@tox_hookimpl
def tox_addoption(parser):

    tox_pyenv_group = parser.add_argument_group(
        title='tox-pyenv plugin options',
    )
    tox_pyenv_group.add_argument(
        '--tox-pyenv-fallback', '-F',
        default=False,
        action='store_true',
        help=('If `pyenv which {basepython}` exits non-zero when looking '
              'up the python executable, fallback to tox\'s built-in '
              'logic.'))


@tox_hookimpl
def tox_get_python_executable(envconfig):
    try:
        pipe = subprocess.Popen(
            ['pyenv', 'which', envconfig.basepython],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = pipe.communicate()
    except OSError:
        raise PyenvMissing(
            "pyenv doesn't seem to be installed, you probably "
            "don't want to be using this tox-pyenv plugin.")
    if pipe.poll() != 0:
        raise PyenvWhichFailed(err)
    return out.strip()
