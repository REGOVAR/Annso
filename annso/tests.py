#!python
# coding: utf-8

import unittest


from tests.test_core_file import TestCoreFile





# /!\ For a weird raison, unittest.main() doesn't work (no UT loaded) when we import the pirus.core object. So we run the tests manually

# Run tests
if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Load test to execute
    for test in [m for m in TestCoreFile.__dict__.keys() if str.startswith(m, "test_")]:
        suite.addTest(TestCoreFile(test))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)