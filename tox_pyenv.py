"""tox-pyenv

Plugin for the tox_get_python_executable using tox's plugin system:

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

import logging
import ntpath
import os
import re
import subprocess

from distutils.version import LooseVersion

import py
from tox import hookimpl as tox_hookimpl

# __about__
__title__ = 'tox-pyenv'
__summary__ = ('tox plugin that makes tox use `pyenv which` '
               'to find python executables')
__url__ = 'https://github.com/samstav/tox-pyenv'
__version__ = '1.1.0'
__author__ = 'Sam Stavinoha'
__email__ = 'smlstvnh@gmail.com'
__keywords__ = ['tox', 'pyenv', 'python']
__license__ = 'Apache License, Version 2.0'
# __about__


LOG = logging.getLogger(__name__)
PYTHON_VERSION_RE = re.compile(r'^(?:python|py)([\d\.]{1,8})$',
                               flags=re.IGNORECASE)


class ToxPyenvException(Exception):

    """Base class for exceptions from this plugin."""


class PyenvMissing(ToxPyenvException, RuntimeError):

    """The pyenv program is not installed."""


class NoSuitableVersionFound(ToxPyenvException):

    """Could not a find a python version that satisfies requirement."""


def _get_pyenv_known_versions():
    """Return searchable output from `pyenv versions`."""
    known_versions = _pyenv_run(['versions'])[0].split(os.linesep)
    return [v.strip() for v in known_versions if v.strip()]


def _pyenv_run(command, **popen_kwargs):
    """Run pyenv command with Popen.

    Returns the result tuple as (stdout, stderr, returncode).
    """
    try:
        pyenv_bin = getattr(
            py.path.local.sysfind('pyenv'), 'strpath', 'pyenv'
        )
        pyenv_bin = pyenv_bin or 'pyenv'
        cmd = [pyenv_bin] + command
        pipe = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            **popen_kwargs
        )
        out, err = pipe.communicate()
        out, err = out.strip(), err.strip()
    except OSError:
        LOG.warning(
            "pyenv doesn't seem to be installed, you probably "
            "don't want this plugin installed either."
        )
        raise
    else:
        returncode = pipe.poll()
        if returncode == 0:
            return out, err
        else:
            cmdstr = ' '.join([str(x) for x in cmd])
            LOG.error("The command `%s` executed by the tox-pyenv plugin failed. "
                      "STDERR: \"%s\"   STDOUT: \"%s\"", cmdstr, err, out)
            raise subprocess.CalledProcessError(returncode, cmdstr, output=err)


def _extrapolate_to_known_version(desired, known):
    """Given the desired version, find an acceptable available version."""
    match = PYTHON_VERSION_RE.match(desired)
    if match:
        match = match.groups()[0]
        if match in known:
            return match
        else:
            matches = sorted([LooseVersion(j) for j in known
                              if j.startswith(match)])
            if matches:
                # Select the latest.
                # e.g. python2 gets 2.7.10
                # if known_versions = ['2.7.3', '2.7', '2.7.10']
                return matches[-1].vstring
    raise NoSuitableVersionFound(
        'Given desired version {0}, no suitable version of python could '
        'be matched in the list given by `pyenv versions`.'.format(desired)
    )


def _set_env_and_retry(envconfig):
    # Let's be smart, and resilient to 'command not found'
    # especially if we can reasonably figure out which
    # version of python is desired, and that version of python
    # is installed and available through pyenv.
    desired_version = ntpath.basename(envconfig.basepython)
    LOG.debug("tox-pyenv is now looking for the desired python "
              "version (%s) through pyenv. If it is found, it will "
              "be enabled and this operation retried.", desired_version)

    def _enable_and_call(_available_version):
        LOG.debug('Enabling %s by setting $PYENV_VERSION to %s',
                  desired_version, _available_version)
        _env = os.environ.copy()
        _env['PYENV_VERSION'] = _available_version
        return _pyenv_run(
            ['which', envconfig.basepython], env=_env)[0]

    known_versions = _get_pyenv_known_versions()

    if desired_version in known_versions:
        return _enable_and_call(desired_version)
    else:
        match = _extrapolate_to_known_version(
            desired_version, known_versions)
        return _enable_and_call(match)


@tox_hookimpl
def tox_get_python_executable(envconfig):
    """Hook into tox plugins to use pyenv to find executables."""

    try:
        out, err = _pyenv_run(['which', envconfig.basepython])
    except OSError:
        # pyenv not installed or executable could not be found
        if not envconfig.tox_pyenv_fallback:
            raise
        LOG.error("tox-pyenv plugin failed, falling back. "
                  "To disable this behavior, set "
                  "tox_pyenv_fallback=False in your tox.ini or use "
                  " --tox-pyenv-no-fallback on the command line.")
        return
    except subprocess.CalledProcessError:
        try:
            return _set_env_and_retry(envconfig)
        except (subprocess.CalledProcessError, NoSuitableVersionFound):
            if not envconfig.tox_pyenv_fallback:
                raise
            LOG.debug("tox-pyenv plugin failed, falling back. "
                      "To disable this behavior, set "
                      "tox_pyenv_fallback=False in your tox.ini or use "
                      " --tox-pyenv-no-fallback on the command line.")
    else:
        return out


def _setup_no_fallback(parser):
    """Add the option, --tox-pyenv-no-fallback.

    If this option is set, do not allow fallback to tox's built-in
    strategy for looking up python executables if the call to `pyenv which`
    by this plugin fails. This will allow the error to raise instead
    of falling back to tox's default behavior.
    """

    cli_dest = 'tox_pyenv_fallback'
    halp = ('If `pyenv which {basepython}` exits non-zero when looking '
            'up the python executable, do not allow fallback to tox\'s '
            'built-in default logic.')
    # Add a command-line option.
    tox_pyenv_group = parser.argparser.add_argument_group(
        title='{0} plugin options'.format(__title__),
    )
    tox_pyenv_group.add_argument(
        '--tox-pyenv-no-fallback', '-F',
        dest=cli_dest,
        default=True,
        action='store_false',
        help=halp
    )

    def _pyenv_fallback(testenv_config, value):
        cli_says = getattr(testenv_config.config.option, cli_dest)
        return cli_says or value

    # Add an equivalent tox.ini [testenv] section option.
    parser.add_testenv_attribute(
        name=cli_dest,
        type="bool",
        postprocess=_pyenv_fallback,
        default=False,
        help=('If `pyenv which {basepython}` exits non-zero when looking '
              'up the python executable, allow fallback to tox\'s '
              'built-in default logic.'),
    )


@tox_hookimpl
def tox_addoption(parser):
    """Add command line options to the argparse-style parser object."""
    _setup_no_fallback(parser)
