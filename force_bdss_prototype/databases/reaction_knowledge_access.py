import numpy as np


class Reaction_knowledge_access:
    """
        Reaction knowledge database singleton\n
        Provides generic access to an underlying reaction knowledge database
    """

    _instance = None

    def getInstance():
        """
        Returns the Reaction_knowledge_access singleton instance

        Returns
        -------
        Reaction_knowledge_access
            Reaction_knowledge_access instance
        """
        if Reaction_knowledge_access._instance == None:
            Reaction_knowledge_access()
        return Reaction_knowledge_access._instance

    def __init__(self):
        if Reaction_knowledge_access._instance != None:
            raise Exception("This class is a singleton!")
        else:
            Reaction_knowledge_access._instance = self

    def get_side_products(self, R):
        """
        Returns the side product of the reaction

        Parameters
        ----------
        R: dict(reactants, products)
            Dictionary of the reactants and products of the chemical process

        Returns
        -------
        numpy.array
            A numpy array containing a dictionary with the component information
        """

        S = {"name": "sideproduct", "manufacturer": "", "pdi": 0}
        return np.array([S])

    def estimate_reaction_time(self, R):
        """
        Estimates the reaction time 

        Parameters
        ----------
        R: dict(reactants, products)
            Dictionary of the reactants and products of the chemical process

        Returns
        -------
        float
            The estimated reaction time in seconds
        """
        # Transferred to json
        # estimated reaction time in s
        e_time = 360.
        return e_time

