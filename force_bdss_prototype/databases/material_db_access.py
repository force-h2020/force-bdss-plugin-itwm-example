# Transferred
import numpy as np


class Material_db_access:
    """
        Material Database singleton\n
        Provides generic access to an underlying material database
    """

    _instance = None

    @staticmethod
    def getInstance():
        """
        Returns the Material_db_access singleton instance

        Returns
        -------
        Material_db_access
            Material_db_access instance
        """
        if Material_db_access._instance == None:
            Material_db_access()
        return Material_db_access._instance

    def __init__(self):
        if Material_db_access._instance != None:
            raise Exception("This class is a singleton!")
        else:
            Material_db_access._instance = self

    def get_component_molec_mass(self, C):
        """
        Returns the molecular mass of the input component (currently not used)

        Parameters
        ----------
        C: dict("name", "manufacturer", "pdi")
            Dictionary containing the component information 

        Returns
        -------
        float
            The mass of the input component
        """
        mass = 1.
        return mass

    def get_pure_component_density(self, C):
        """
        Returns the density of the input component in particles per liter

        Parameters
        ----------
        C: dict("name", "manufacturer", "pdi")
            Dictionary containing the component information 

        Returns
        -------
        int
            The density in particles per liter
        """
        # Transferred to json
        # p in particles/l
        if C["name"] == "eductA":
            p = 5
        if C["name"] == "eductB":
            p = 10
        if C["name"] == "contamination":
            p = 55
        return p

    def get_arrhenius_params(self, C):
        """
        Returns the arrhenius parameters of the input component 

        Parameters
        ----------
        C: dict("name", "manufacturer", "pdi")
            Dictionary containing the component information 

        Returns
        -------
        (v, delta_H): tuple[float, float]
            A tuple containing the arrhenius parameters
        """
        # Transferred to json
        if C["products"][0]["name"] == "product":
            # delta H in kJ/mol
            delta_H = 1000 * 8.3144598e-3
            v = 2e-2
        else:
            delta_H = 4500 * 8.3144598e-3
            v = 2e-2
        return (v, delta_H)

    def get_supplier_cost_educt(self, C):
        """
        Returns the cost of the input component

        Parameters
        ----------
        C: dict("name", "manufacturer", "pdi")
            Dictionary containing the component information 

        Returns
        -------
        float
            The cost of the input component
        """
        cost = 1.
        return cost
