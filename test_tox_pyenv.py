from __future__ import print_function

import os
import platform
import subprocess
import sys
import unittest

try:
    unicode
except NameError:
    unicode = str


def touni(s, enc='utf8', err='strict'):
    if isinstance(s, bytes):
        return s.decode(enc, err)
    else:
        return unicode(s or ("" if s is None else s))


class TestThings(unittest.TestCase):

    def test_the_answer(self):

        self.assertEqual(42, 42)

    def test_is_precisely_correct_version(self):

        toxenvname = 'TOX_%s' % os.environ['TOX_ENV_NAME'].upper()
        expected_string = os.environ[toxenvname]
        print('\n\nTOX ENV NAME: %s' % toxenvname)
        if platform.python_implementation() == 'PyPy':
            a, b, c = sys.pypy_version_info[:3]
            actual_list = [a, b, c]
            expected_string = expected_string.split('-')[1]
            print('\nExpected version for this tox env: PyPy %s'
                  % expected_string)
            print('Actual version for this tox env: Python %s'
                  % platform.python_version())
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
