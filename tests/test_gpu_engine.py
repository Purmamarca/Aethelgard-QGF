import unittest

import numpy as np

from aethelgard_engine_gpu import AethelgardEngineGPU


class TestAethelgardEngineGPU(unittest.TestCase):
    def setUp(self):
        # Even without a GPU, it should work via NumPy fallback
        self.engine = AethelgardEngineGPU(grid_size=16, domain_size=5.0, use_gpu=False)

    def test_initialization(self):
        self.assertEqual(self.engine.N, 16)
        # Check if metric initialization is correct (should be diagonal now)
        self.assertTrue(np.allclose(self.engine.metric[..., 0, 0], 1.0))
        # Off-diagonal should be 0.0
        self.assertTrue(np.allclose(self.engine.metric[..., 0, 1], 0.0))

    def test_causality_constraint_gpu(self):
        """
        TDD: Test that the GPU engine also enforces causality.
        """
        mass_dist = np.ones((16, 16, 16)) * 1e40
        entropy_map = np.zeros((16, 16, 16))
        
        result = self.engine.solve_field_equations(mass_dist, entropy_map, iterations=10)
        
        # Metric should be capped
        max_val = float(np.max(result[..., 0, 0]))
        self.assertLessEqual(max_val, 10.0)

    def test_calculate_quantum_pressure_gpu(self):
        """Test quantum pressure calculation logic."""
        entropy_field = np.ones((16, 16, 16)) * 1.0
        pressure = self.engine.calculate_quantum_pressure(entropy_field)
        self.assertTrue(np.allclose(pressure, 0.0))

    def test_solve_full_gpu(self):
        """Test a full solver run for variability."""
        mass_dist = np.random.rand(16, 16, 16) * 1e12
        entropy_map = np.random.rand(16, 16, 16) * 5.0
        result = self.engine.solve_field_equations(mass_dist, entropy_map, iterations=5)
        self.assertIsNotNone(result)
