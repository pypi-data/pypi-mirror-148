# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 21:19:54 2022

@author: MERT
"""




import unittest
from grifpackage import deneme


class TestDeneme(unittest.TestCase):

    def test_multiplication(self):
        self.assertEqual(deneme.multiplication(2, 2), 4)

    def test_division(self):
        self.assertEqual(deneme.division(4, 2), 2)

        

if __name__ == '__main__':
    unittest.main()