import numpy as np
from ..databases.material_db_access import Material_db_access
from ..databases.reaction_knowledge_access import Reaction_knowledge_access
from ..databases.process_db_access import Process_db_access


class Initializer:
    """
        Initializer singleton\n
        Provides access to the initial kinematic model and the material relation data
    """
    _instance = None

    @staticmethod 
    def getInstance(R):
        """
        Returns the Initializer singleton instance

        Parameters
        ----------
        R: dict(reactants, products)
            Dictionary of the reactants and products of the chemical process

        Returns
        -------
        Initializer
            Initializer instance
        """
        if Initializer._instance == None:
            Initializer(R)
        return Initializer._instance

    def __init__(self, R):
        if Initializer._instance != None:
            raise Exception("This class is a singleton!")
        else:
            Initializer._instance = self
            self.R = R
            self.m_db_access = Material_db_access.getInstance()
            self.p_db_access = Process_db_access.getInstance(self.R)
            self.react_knowledge = Reaction_knowledge_access.getInstance()

    def get_init_data_kin_model(self, R, C):
        """
        Returns the initial data for the kinematic model

        Parameters
        ----------
        R: dict(reactants, products)
            Dictionary of the reactants and products of the chemical process
        C: dict(contamination)
            Dictionary of the contamination in the first educt

        Returns
        -------
        numpy.array
            Numpy array containing the initial data for the kinematic model
        """
        # Transferred to json
        A = R["reactants"][0]
        B = R["reactants"][1]
        p_A = self.m_db_access.get_pure_component_density(A)
        p_B = self.m_db_access.get_pure_component_density(B)
        p_C = self.m_db_access.get_pure_component_density(C)
        #p_db_access = Process_db_access.getInstance(R)
        X = np.zeros(7)
        T_min, T_max = self.p_db_access.get_temp_range()
        X[5] = 0.5 * (T_max + T_min)
        C_min, C_max = self.p_db_access.get_contamination_range(A)
        C_bar = 0.5 * (C_max + C_min)
        E = p_C - C_bar
        E /= p_C / p_A + p_C / p_B - C_bar * p_C / (p_B * p_C)
        X[2] = 0
        X[3] = 0
        X[0] = E
        X[1] = E
        X[4] = C_bar * (1 - X[1] / p_B)
        tau = self.react_knowledge.estimate_reaction_time(R)
        X[6] = tau
        return X

    def get_material_relation_data(self, R):
        """
        Returns the material relation data

        Parameters
        ----------
        R: dict(reactants, products)
            Dictionary of the reactants and products of the chemical process

        Returns
        -------
        (M_v, M_delta_H): tuple[numpy.array, numpy.array]
            A tuple consisting of a numpy array containing the arrhenius
            parameters of the product and a numpy array containing the arrhenius
            parameters of the side product 
        """
        
        # Transferred to json
        S = self.react_knowledge.get_side_products(R)[0]
        R_S = { "reactants": R["reactants"], "products": [S] }
        vp, delta_Hp = self.m_db_access.get_arrhenius_params(R)
        vs, delta_Hs = self.m_db_access.get_arrhenius_params(R_S)
        M_v = np.array([vp, vs])
        M_delta_H = np.array([delta_Hp, delta_Hs])
        return (M_v, M_delta_H)

    def X_to_y(self, X):
        """
        Calculates y-dimension values from X-dimension values 

        Parameters
        ----------
        X: numpy.array
            Numpy array containing the X-dimension values 

        Returns
        -------
        numpy.array
            A numpy array containing y-dimension values
        """
        V_r = self.p_db_access.get_reactor_vol()
        p_B = self.m_db_access.get_pure_component_density(self.R["reactants"][1])
        y = np.zeros(4)
        y[0] = V_r - X[1] * V_r / p_B
        y[1] = V_r / y[0] * X[4]
        y[2] = X[5]
        y[3] = X[6]
        return y


