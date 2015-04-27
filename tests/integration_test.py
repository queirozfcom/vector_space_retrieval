import unittest

from vsr.__main__ import run_all_modules

class TestStringMethods(unittest.TestCase):

    def test_running_all_projects_together(self):
        params = dict()

        params['USE_STEMMER']            = True
        params['TOKEN_LENGTH_THRESHOLD'] = 2
        params['ONLY_LETTERS']           = True
        params['IGNORE_STOP_WORDS']      = True

        run_all_modules(params)

if __name__ == '__main__':
    unittest.main()