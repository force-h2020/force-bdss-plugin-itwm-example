import unittest
import numpy as np

from force_bdss_prototype.attributes.attributes import Attributes

A = { "name": "eductA", "manufacturer": "", "pdi": 0 }
B = { "name": "eductB", "manufacturer": "", "pdi": 0 }
C = { "name": "contamination", "manufacturer": "", "pdi": 0 }
P = { "name": "product", "manufacturer": "", "pdi": 0 }
R = { "reactants": [A, B], "products": [P] }
nptype = type(np.array([]))

class AttributesTestCase(unittest.TestCase):

    def test_instance(self):
        attributes = Attributes(R, C)
        self.assertIsInstance(attributes, Attributes)

    def test_calc_return_type(self):
        attributes = Attributes(R, C)
        y = np.ones(4)
        self.assertEqual(type(attributes.calc_attributes(y)[0]), nptype)
        self.assertEqual(type(attributes.calc_attributes(y)[1]), nptype)

    def test_calc_return_shape(self):
        attributes = Attributes(R, C)
        y = np.ones(4)
        self.assertEqual(attributes.calc_attributes(y)[0].shape, (9, ))
        self.assertEqual(attributes.calc_attributes(y)[1].shape, (4, 9))
