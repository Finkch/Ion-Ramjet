# Tests vector

import unittest
from vector import *
import numpy as np


class TestStringMethods(unittest.TestCase):

    # Tests instantiation and calling
    def test_instantiate_and_call(self):
        vec = Vector(5, 4, 3)
        self.assertEqual(vec(), [5, 4, 3])

    def test_add(self):
        vec1 = Vector(5, 4, 3)
        vec2 = Vector(-1, -2, -3)
        result = vec1 + vec2

        self.assertEqual(result(), [4, 2, 0])

    def test_sub(self):
        vec1 = Vector(5, 4, 3)
        vec2 = Vector(-1, -2, -3)
        result = vec1 - vec2

        self.assertEqual(result(), [6, 6, 6])

    def test_mult(self):
        vec1 = Vector(5, 4, 3)
        mult = -3
        result1 = vec1 * mult
        result2 = mult * vec1

        self.assertEqual(result1(), result2())
        self.assertEqual(result1(), [-15, -12, -9])
        self.assertEqual(result2(), [-15, -12, -9])

    def test_div(self):
        vec1 = Vector(5, 4, 3)
        div1 = 60
        div2 = 10
        result1 = div1 / vec1
        result2 = vec1 / div2

        self.assertEqual(result1(), [12, 15, 20])
        self.assertEqual(result2(), [0.5, 0.4, 0.3])
    
    def test_pow(self):
        vec1 = Vector(5, 4, 3)
        power = 3
        result = vec1 ** power

        self.assertEqual(result(), [125, 64, 27])

    def test_neg(self):
        vec1 = Vector(5, 4, 3)
        result = -vec1

        self.assertEqual(result(), [-5, -4, -3])
    
    def test_hypo(self):
        vec1 = Vector(5, 4, 3)
        result = vec1.hypo()

        self.assertAlmostEqual(result, np.sqrt(5 ** 2 + 4 ** 2 + 3 ** 2))