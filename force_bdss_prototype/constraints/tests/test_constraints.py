import unittest
import numpy as np

from force_bdss_prototype.constraints.constraints import Constraints
from force_bdss_prototype.databases.process_db_access import Process_db_access


A = { "name": "eductA", "manufacturer": "", "pdi": 0 }
B = { "name": "eductB", "manufacturer": "", "pdi": 0 }
C = { "name": "contamination", "manufacturer": "", "pdi": 0 }
P = { "name": "product", "manufacturer": "", "pdi": 0 }
R = { "reactants": [A, B], "products": [P] }
nptype = type(np.array([]))
N = 4
p_db_access = Process_db_access.getInstance(R)
vr = p_db_access.get_reactor_vol()


class ConstraintsTestCase(unittest.TestCase):

    def test_instance(self):
        constraints = Constraints(R)
        self.assertIsInstance(constraints, Constraints)

    def test_get_lin_const_return_type(self):
        constraints = Constraints(R)
        lin_constraints = constraints.get_linear_constraints()
        self.assertIsInstance(lin_constraints, tuple)

    def test_get_lin_constr_return_lenght(self):
        constraints = Constraints(R)
        lin_constraints = constraints.get_linear_constraints()
        self.assertEqual(len(lin_constraints), N)

    def test_get_va_range_return_type(self):
        constraints = Constraints(R)
        self.assertIsInstance(constraints.get_linear_constraints()[0], tuple)

    def test_get_va_range_return_lenght(self):
        constraints = Constraints(R)
        self.assertEqual(len(constraints.get_linear_constraints()[0]), 2)

    def test_va_range(self):
        constraints = Constraints(R)
        va_range = constraints.get_linear_constraints()[0]
        self.assertTrue(va_range[0] <= va_range[1],
                        "first entry is bigger than second")
        self.assertTrue(va_range[0] >= 0, "va smaller than 0")
        self.assertTrue(va_range[1] <= vr,
                        "volume a bigger than volume of reactor")

    def test_get_contamination_range_return_type(self):
        constraints = Constraints(R)
        cont_range = constraints.get_linear_constraints()[1]
        self.assertIsInstance(cont_range, tuple)

    def test_get_contamination_range_return_lenght(self):
        constraints = Constraints(R)
        cont_range = constraints.get_linear_constraints()[1]
        self.assertEqual(len(cont_range), 2)

    def test_contamination_range(self):
        constraints = Constraints(R)
        cont_range = constraints.get_linear_constraints()[1]
        self.assertTrue(cont_range[0] <= cont_range[1],
                        "first component is bigger than second")
        self.assertTrue(cont_range[0] >= 0, "contamination smaller than 0")

    def test_get_temp_range_return_type(self):
        constraints = Constraints(R)
        temp_range = constraints.get_linear_constraints()[2]
        self.assertIsInstance(temp_range, tuple)

    def test_get_temp_range_return_lenght(self):
        constraints = Constraints(R)
        temp_range = constraints.get_linear_constraints()[2]
        self.assertEqual(len(temp_range), 2)

    def test_temp_range(self):
        constraints = Constraints(R)
        temp_range = constraints.get_linear_constraints()[2]
        self.assertTrue(temp_range[0] <= temp_range[1],
                        "first component is bigger than second")

    def test_max_reaction_time(self):
        constraints = Constraints(R)
        tau = constraints.get_linear_constraints()[3][0]
        self.assertTrue(tau >= 0, "time is smaller than 0")
