import numpy as np
from ..objectives.objectives import Objectives
from ..constraints.constraints import Constraints
from ..initializer.initializer import Initializer
from .MCOsolver import MCOsolver
from ..pareto_process.pareto_process_db import Pareto_process_db
from ..databases.process_db_access import Process_db_access
import kivy.core.window as window
from kivy.base import EventLoop
from kivy.cache import Cache

class MCOwrapper:
    """
    Wrapper for the MCO solver
    """

    # default constructor
    def __init__(self, R, C):
        # mco setup: trasform to impl. data structures.
        self.R = R
        self.C = C
        self.obj = Objectives(self.R, self.C) 
        _reset()
        self.constraints = Constraints(self.R)
        _reset()
        self.ini = Initializer.getInstance(self.R)
        obj_f = lambda y: self.obj.obj_calc(y)[0]
        obj_jac = lambda y: self.obj.obj_calc(y)[1]
        constr = self.constraints.get_editor_constraints() #<-- calls constraints editor
        X0 = self.ini.get_init_data_kin_model(self.R, self.C)
        p_db_access = Process_db_access.getInstance(R)
        self.C_supplier = p_db_access.get_C_supplier()
        # X0 structure:
        # 0: A concentration
        # 1: 0.5. B concentration
        # 2: 0. P concentration
        # 3: 0. S concentration
        # 4: 0.505. C concentration
        # 5: 335. Temperature
        # 6: 360. Reaction time
        y0 = self.ini.X_to_y(X0)
        self.mcosolver = MCOsolver(y0, constr, obj_f, obj_jac)

    def solve(self):
        """
        Executes the solve procedure in the underlying MCOsolver

        Returns
        -------
        numpy.array
            A numpy array containing all computed results
        """
        results = self.mcosolver.solve(N=10)
        res = np.empty((results.shape[0], results.shape[1] + 3))
        for i in range(results.shape[0]):
            y = results[i, :]
            O, _ = self.obj.obj_calc(y)
            res[i, :results.shape[1]] = results[i, :]
            res[i, results.shape[1]:] = O.flatten()
        res[:, results.shape[1]] = self.C_supplier * np.exp(res[:, results.shape[1]])
        self.pp_db = Pareto_process_db(res)
        self.pp_db.dump_data()
        return res

def _reset():
    #clears the Kivy EventLoop cache to avoid issues when executing the different GUIs in succession
    if not EventLoop.event_listeners:
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}
