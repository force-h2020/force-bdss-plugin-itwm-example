import numpy as np


class Process_db_access:
    """
        Process database singleton\n
        Provides generic access to an underlying process database
    """

    _instance = None

    def getInstance(R):
        """
        Returns the Process_db_access singleton instance

        Returns
        -------
        Process_db_access
            Process_db_access instance
        """
        if Process_db_access._instance == None:
            Process_db_access(R)
        return Process_db_access._instance

    def __init__(self, R):
        if Process_db_access._instance != None:
            raise Exception("This class is a singleton!")
        else:
            Process_db_access._instance = self
            self.R = R
            self.V_r = 1000.
            self.W = 1e-8
            self.const_A = 5e-3
            self.cost_B = 4e-3
            self.quad_coeff = 1e-5
            self.C_supplier = .01 * 5
            self.cost_purification = 0.5e-3

    def get_contamination_range(self, A):
        """
        Returns the default contamination range of the first educt 

        Parameters
        ----------
        A: dict("name", "manufacturer", "pdi")
            Dictionary containing the component information of the first educt

        Returns
        -------
        (c_min, c_max): tuple[float, float]
            The default min and max values of the contamination of the first educt in mol/l
        """
        # Transferred to json
        # [C] in mol/l
        c_min = self.C_supplier * 1e-9
        c_max = self.C_supplier
        return (c_min, c_max)

    def get_temp_range(self):
        """
        Returns the default temperature range considered for the reaction

        Returns
        -------
        (T_min, T_max): tuple[float, float]
            The default min and max values of the temperature in Kelvin
        """
        # Transferred to json
        # T in Kelvin
        T_min = 270.
        T_max = 400.
        return (T_min, T_max)

    def get_reactor_vol(self):
        """
        Returns the default reactor volume

        Returns
        -------
        float
            The default reactor volume
        """
        # Transferred to json
        return self.V_r

    def get_C_supplier(self):
        """
        Returns the average default contamination of the first educt

        Returns
        -------
        float:
            The default contamination of the first educt in mol/l
        """
        return self.C_supplier

    def _get_process_params(self):
        return self.V_r, self.W, self.const_A, self.cost_B, self.quad_coeff, self.C_supplier, self.cost_purification
