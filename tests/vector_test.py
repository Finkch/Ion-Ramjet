# Tests vector

import unittest
from vector import *


class TestStringMethods(unittest.TestCase):

    # Tests instantiation and calling
    def test_instantiate_and_call(self):
        vec = Vector(5, 4, 3)
        self.assertEqual(vec(), [5, 4, 3])