import numpy as np
from ..databases.process_db_access import Process_db_access
from ..databases.material_db_access import Material_db_access
from ..gui_apps.functionapp import FunctionApp
from ..attributes.attributes import Attributes
from sympy import symbols, Matrix, sympify, diff, evalf, lambdify

class Objectives:
    """ 
    Implementation of the Objective Dimension
    """
    # default constructur
    def __init__(self, R, C):
        self.R = R
        self.C = C
        self.p_db_access = Process_db_access.getInstance(self.R)
        self.m_db_access = Material_db_access.getInstance()
        self.O, self.grad_a_O = FunctionApp().run_with_output(self._function_editor_input(), -1)
        self.attributes = Attributes(R, C)
        self._obj_calc_init()

    def _obj_calc_init(self):
        #Sets up objective calculation
        #retrieve fixed values
        p_A_value = self.m_db_access.get_pure_component_density(self.R["reactants"][0])
        p_B_value = self.m_db_access.get_pure_component_density(self.R["reactants"][1])
        p_C_value = self.m_db_access.get_pure_component_density(self.C)
        V_r_value, W_value, const_A_value, cost_B_value, quad_coeff_value, C_supplier_value, cost_purification_value = self.p_db_access._get_process_params()
        #fixed value symbols
        p_A, p_B, p_C, V_r, W, const_A, cost_B, quad_coeff, C_supplier, cost_purification = symbols("p_A, p_B, p_C, V_r, W, const_A, cost_B, quad_coeff, C_supplier, cost_purification")
    
        #a setup
        V_a, C_e, T, t = symbols("V_a, C_e, T, t")
        conc_A, conc_B, conc_P, conc_S, conc_C = symbols("conc_A, conc_B, conc_P, conc_S, conc_C")
        self.a = [V_a, C_e, T, t, conc_A, conc_B, conc_P, conc_S, conc_C]

        #substitute fixed values
        self.O = self.O.subs(p_A, p_A_value).subs(p_B, p_B_value).subs(p_C, p_C_value).subs(V_r, V_r_value).subs(W, W_value).subs(const_A, const_A_value).subs(cost_B, cost_B_value).subs(quad_coeff, quad_coeff_value).subs(C_supplier,C_supplier_value).subs(cost_purification, cost_purification_value).evalf()
        self.grad_a_O = self.grad_a_O.subs(p_A, p_A_value).subs(p_B, p_B_value).subs(p_C, p_C_value).subs(V_r, V_r_value).subs(W, W_value).subs(const_A, const_A_value).subs(cost_B, cost_B_value).subs(quad_coeff, quad_coeff_value).subs(C_supplier,C_supplier_value).subs(cost_purification, cost_purification_value).evalf()
        
        self.O = lambdify(self.a, self.O)
        self.grad_a_O = lambdify(self.a, self.grad_a_O)

    def obj_calc(self, y):
        """
        Calculates the objectives and the y_O gradient matrix

        Parameters
        ----------
        y: numpy.array
            numpy.array containing the y-dimension values

        Returns
        -------
        (objectives, grad_y_O_Matrix) tuple[numpy.array, numpy.array]
            A tuple consisting of a 1D numpy array containing the calculated
            objective values and a 2D numpy array containing y_O gradient matrix
        """
        a, grad_y_a = self.attributes.calc_attributes(y)
        O = self.O(*a)
        grad_a_O = self.grad_a_O(*a)
        grad_y_O = np.dot(grad_y_a, grad_a_O)
        return (O, grad_y_O.T)

    def _function_editor_input(self):
        #functions: key: id, value[0]: description, value[1]: function, value[2]: isEditable
        functions = {
            "pc" : ["Production Cost","t * (T - 290)^2 * W", False],
            "mc" : ["Material Cost" , "mcA + mcB", False],
            "mcA" : ["Mat cost A" , "(cost_purification * (C_e / C_supplier -1)^2 + const_A) * V_a + V_r * quad_coeff * (V_a - 0.6 * V_r)**2", True],
            "mcB" : ["Mat cost B" , "(V_r - V_a) * cost_B", True],
            "imp" : ["Impurity Concentration" , "ln((conc_A + conc_B + conc_C + conc_S )/ C_supplier)", False]
        }
        
        attributes = {
            "V_a" : "volume of A",
            "C_e" : "impurity of A",
            "T" : "temperature",
            "t" : "reaction time",
            "conc_A" : "concentration of A",
            "conc_B" : "concentration of B",
            "conc_P" : "concentration of P",
            "conc_S" : "concentration of S",
            "conc_C" : "concentration of C"
        }
        
        fixed_parameters = {
            "p_A" : "pure density of A",
            "p_B" : "pure density of A",
            "p_C" : "pure density of A",
            "V_r" : "reactor volume",
            "W" : "heating cost",
            "const_A" : "description",
            "cost_B" : "description",
            "quad_coeff" : "description",
            "C_supplier" : "description",
            "cost_purification" : "description"
        }
    
        return [functions, attributes, fixed_parameters]