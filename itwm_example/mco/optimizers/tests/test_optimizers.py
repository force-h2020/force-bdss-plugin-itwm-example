from unittest import TestCase

from force_bdss.api import KPISpecification

from itwm_example.mco.mco_factory import MCOFactory
from itwm_example.mco.space_sampling.space_samplers import (
    UniformSpaceSampler,
    DirichletSpaceSampler,
)
from itwm_example.mco.tests.mock_classes import MockOptimizer
from itwm_example.mco.optimizers.optimizers import WeightedOptimizer


class TestWeightedOptimizer(TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = MCOFactory(self.plugin)
        self.mco_model = self.factory.create_model()

        self.kpis = [KPISpecification(), KPISpecification()]
        self.parameters = [1, 1, 1, 1]

        self.mco_model.kpis = self.kpis
        self.mco_model.parameters = [
            self.factory.parameter_factories[0].create_model()
            for _ in self.parameters
        ]

        self.optimizer = self.mco_model.optimizer

    def test_init(self):
        self.assertIsInstance(self.optimizer, WeightedOptimizer)
        self.assertEqual("Weighted_Optimizer", self.optimizer.name)
        self.assertIs(self.optimizer.single_point_evaluator, None)
        self.assertEqual("SLSQP", self.optimizer.algorithms)
        self.assertEqual(7, self.optimizer.num_points)
        self.assertEqual("Uniform", self.optimizer.space_search_mode)

    def test__space_search_distribution(self):
        for strategy, klass in (
            ("Uniform", UniformSpaceSampler),
            ("Dirichlet", DirichletSpaceSampler),
            ("Uniform", UniformSpaceSampler),
        ):
            self.optimizer.space_search_mode = strategy
            distribution = self.optimizer._space_search_distribution()
            self.assertIsInstance(distribution, klass)
            self.assertEqual(len(self.kpis), distribution.dimension)
            self.assertEqual(7, distribution.resolution)

    def test_scaling_factors(self):
        mock_optimizer = MockOptimizer(None, None)
        self.optimizer._weighted_optimize = mock_optimizer.optimize
        scaling_factors = self.optimizer.get_scaling_factors()
        self.assertEqual([0.1, 0.1], scaling_factors)

    def test_auto_scale(self):
        temp_kpis = [KPISpecification(), KPISpecification(auto_scale=False)]
        self.mco_model.kpis = temp_kpis

        mock_optimizer = MockOptimizer(None, None)
        self.optimizer._weighted_optimize = mock_optimizer.optimize

        scaling_factors = self.optimizer.get_scaling_factors()
        self.assertEqual([0.1, 1.0], scaling_factors)

    def test___getstate__(self):
        state = self.optimizer.__getstate__()
        self.assertDictEqual(
            {
                "name": "Weighted_Optimizer",
                "single_point_evaluator": None,
                "algorithms": "SLSQP",
                "num_points": 7,
                "space_search_mode": "Uniform",
            },
            state,
        )
