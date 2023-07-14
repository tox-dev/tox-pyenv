from __future__ import print_function

import errno
import os
import platform
import subprocess
import sys
import unittest

import mock

import tox_pyenv

try:
    unicode
except NameError:
    unicode = str


def touni(s, enc='utf8', err='strict'):
    if isinstance(s, bytes):
        return s.decode(enc, err)
    else:
        return unicode(s or ("" if s is None else s))


class MockTestenvConfig(object):
    def __init__(self, basepython):
        self.basepython = basepython
        self.tox_pyenv_fallback = True


class TestToxPyenvNoPyenv(unittest.TestCase):

    def setUp(self):
        def _mock_popen_func(cmd, *args, **kw):
            if all(x in cmd for x in ['which', '*TEST*']):
                raise OSError(errno.ENOENT, 'No such file or directory')
            self.fail('Unexpected call to Popen')
            # return self.popen_patcher.temp_original(*args, **kw)
        self.popen_patcher = mock.patch.object(
            tox_pyenv.subprocess, 'Popen', autospec=True,
            side_effect=_mock_popen_func,
        )
        self.popen_patcher.start()
        self.warning_patcher = mock.patch.object(
            tox_pyenv.LOG, 'warning', autospec=True,
        )
        self.warning_patcher.start()

    def tearDown(self):
        self.popen_patcher.stop()
        self.warning_patcher.stop()

    def test_logs_if_no_pyenv_binary(self):
        mock_test_env_config = MockTestenvConfig('*TEST*')
        tox_pyenv.tox_get_python_executable(mock_test_env_config)
        expected_popen = [
            mock.call(
                [mock.ANY, 'which', '*TEST*'],
                stderr=-1, stdout=-1,
                universal_newlines=True
            )
        ]
        self.assertEqual(
            tox_pyenv.subprocess.Popen.call_args_list,
            expected_popen
        )
        expected_warn = [
            mock.call("pyenv doesn't seem to be installed, you "
                      "probably don't want this plugin installed either.")
        ]
        self.assertEqual(tox_pyenv.LOG.warning.call_args_list, expected_warn)


class TestToxPyenvLogger(unittest.TestCase):

    def test_has_nullhandler(self):
        handlers = {str(type(handler)) for handler in tox_pyenv.LOG.handlers}
        self.assertTrue(any('NullHandler' in h for h in handlers))


class TestThings(unittest.TestCase):

    def test_the_answer(self):

        self.assertEqual(42, 42)

    def test_is_precisely_correct_version(self):

        toxenvname = 'TOX_%s' % os.environ['TOX_ENV_NAME'].upper().strip()
        expected_string = os.environ[toxenvname].strip(' "\'')
        print('\n\nTOX ENV NAME: %s' % toxenvname)
        if platform.python_implementation() == 'PyPy':
            actual_list = [str(_).strip() for _ in sys.pypy_version_info[:3]]
            expected_string = expected_string.split('-')[1].strip(' "\'')
            print('\nExpected version for this tox env: PyPy %s'
                  % expected_string)
            print('Actual version for this tox env: PyPy %s'
                  % '.'.join(actual_list))
        else:
            print('\nExpected version for this tox env: Python %s'
                  % expected_string)
            print('Actual version for this tox env: Python %s'
                  % platform.python_version())
            actual_list = list(platform.python_version_tuple())
        expected_list = expected_string.split('.')

        print('\n\nPYTHON VERSION (verbose)')
        print('*************************')
        print(sys.version)
        print('\n')
        self.assertEqual(actual_list, expected_list)

    def test_what_python(self):

        print('\nwhich python')
        subprocess.call('which python', stderr=subprocess.STDOUT, shell=True)
        print('\ntype python')
        subprocess.call('type python', stderr=subprocess.STDOUT, shell=True)
        print('\nwhereis python')
        subprocess.call('whereis python', stderr=subprocess.STDOUT, shell=True)
        print('\n')


if __name__ == '__main__':

    unittest.main(verbosity=3)
