import numpy as np
import sys
import scipy.optimize as sp_opt


class MCOsolver:
    """
    The MCO workflow operates with five different dimensions and gradient matrices between these dimensions:
        - y-dimension = (V_a, C_e, T, t)\n
            Design space, contains of all design space parameters
        - x-dimension = (conc_A, conc_B, conc_P, conc_S, conc_C, T, t)\n
            Input dimension, contrains all input parameters for the physics simulation
        - X-dimension = (conc_A, conc_B, conc_P, conc_S, conc_C, T, t)\n
            Output dimension, contains the output parameters of the physics simulation
        - a-dimension = (V_a, C_e, T, t, conc_A, conc_B, conc_P, conc_S, conc_C)\n
            Attribute dimension, contains both the y-dimension and x-dimension
        - O-dimension = (Imp_conc, prod_cost, mat_cost)\n
            Objective space, contains all objectives for the MCO workflow
    """
    def __init__(self, y0, constr, obj_f, obj_jac):
        self.constr = constr
        self.y0 = y0
        self.obj_f = obj_f
        self.obj_jac = obj_jac
        self.w = np.array([0.4, 0.4, 0.2])
        self.res = np.zeros((100, 4))
        self.i = 0

    def solve(self, N=7):
        """
        Executes the MCO workflow and returns the results it computes.

        Parameters
        ----------
        N: int
            Number of data points per objective

        Returns
        -------
        numpy.array
            A numpy array containing all computed results
        """
        new_obj = lambda y: np.dot(self.w, self.obj_f(y))
        #if np.any(y == float("nan")) else False
        new_obj_jac = lambda y: np.dot(self.w, self.obj_jac(y))
        print("Calculating optimal parameters...")
        i = 0
        for self.w[0] in np.linspace(0, 1, N):
            for self.w[1] in np.linspace(0, 1 - self.w[0],
                                         int(N - round((N - 1)*self.w[0]))):
                self.w[2] = 1 - self.w[0] - self.w[1]
                i += 1
                progress(i, (N*N + N)/2)
                #if not np.any(self.w == 0):
                self.store_curr_res(self.KKTsolver(new_obj, new_obj_jac))
        return self.res[:self.i]

    def KKTsolver(self, new_obj, new_obj_jac):
        """
        Calculates new starting values for the simulation

        Parameters
        ----------
        new_obj: numpy.array
            Current objective results 
        new_obj_jac: numpy.array
            y_O gradient matrix 

        Returns
        -------
        numpy.array
            A numpy array containing new starting values
        """
        opt_res = sp_opt.minimize(new_obj, self.y0, method="SLSQP",
                                  jac=new_obj_jac , bounds=self.constr).x
        return opt_res

    def store_curr_res(self, y):
        """
        Stores the current objective results to the data array

        Parameters
        ----------
        y: numpy.array
            Current objective results 
        """
        if self.i >= self.res.shape[0]:
            res = np.zeros((2*self.res.shape[0], 4))
            res[:self.res.shape[0]] = self.res
            self.res = res
        self.res[self.i] = y
        self.i = self.i + 1

def progress(count, total, status=''):
    """
    Updates the progess bar on the terminal

    Parameters
    ----------
    count: int
        Current iteration
    total: int
        Total iterations
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
