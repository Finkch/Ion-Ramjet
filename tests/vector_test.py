# Tests vector

import unittest
import vector as v


class TestStringMethods(unittest.TestCase):

    # Tests instantiation and calling
    def test_instantiate_and_call(self):
        vec = v.Vector(5, 4, 3)
        self.assertEqual(vec(), [5, 4, 3])