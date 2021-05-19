import unittest
import numpy as np

from force_bdss_prototype.databases.process_db_access import Process_db_access

A = { "name": "eductA", "manufacturer": "", "pdi": 0 }
B = { "name": "eductB", "manufacturer": "", "pdi": 0 }
P = { "name": "product", "manufacturer": "", "pdi": 0 }
R = { "reactants": [A, B], "products": [P] }
nptype = type(np.array([]))

class Process_db_accessTestCase(unittest.TestCase):

    def test_instance(self):
        p_db = Process_db_access.getInstance(R)
        self.assertIsInstance(p_db, Process_db_access)

    def test_contamination_range(self):
        p_db = Process_db_access.getInstance(R)
        cmin, cmax = p_db.get_contamination_range(A)
        self.assertTrue(cmin < cmax)

    def test_temp_range(self):
        p_db = Process_db_access.getInstance(R)
        tmin, tmax = p_db.get_temp_range()
        self.assertTrue(tmin < tmax)

    def test_reactor_vol(self):
        p_db = Process_db_access.getInstance(R)
        V_r = p_db.get_reactor_vol()
        self.assertEqual(type(V_r), float)