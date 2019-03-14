import unittest

def suite():
    return unittest.TestLoader().discover("check_mate.tests", pattern="*.py")