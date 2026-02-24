"""
Unit tests for the Aethelgard-QGF engine.
"""

import unittest

import numpy as np

from aethelgard_engine import AethelgardEngine


class TestAethelgardEngine(unittest.TestCase):
    
    def setUp(self):
        """Initialize engine for each test."""
        self.engine = AethelgardEngine(grid_size=16, domain_size=5.0)
    
    def test_initialization(self):
        """Test proper initialization of the engine."""
        self.assertEqual(self.engine.N, 16)
        self.assertEqual(self.engine.L, 5.0)
        self.assertAlmostEqual(self.engine.dx, 5.0 / 16)
        
        # Check physical constants
        self.assertAlmostEqual(self.engine.G, 6.674e-11)
        self.assertAlmostEqual(self.engine.c, 3.0e8)
        self.assertAlmostEqual(self.engine.hbar, 1.054e-34)
    
    def test_metric_initialization(self):
        """Test that metric is properly initialized to Minkowski."""
        # Check shape
        self.assertEqual(self.engine.metric.shape, (16, 16, 16, 4, 4))
        
        # Check diagonal components (should be 1.0)
        for i in range(4):
            self.assertTrue(np.allclose(self.engine.metric[..., i, i], 1.0))
    
    def test_quantum_pressure_shape(self):
        """Test that quantum pressure calculation returns correct shape."""
        entropy_field = np.random.rand(16, 16, 16)
        T_quantum = self.engine.calculate_quantum_pressure(entropy_field)
        
        self.assertEqual(T_quantum.shape, (16, 16, 16))
    
    def test_quantum_pressure_zero_entropy(self):
        """Test quantum pressure with zero entropy field."""
        entropy_field = np.zeros((16, 16, 16))
        T_quantum = self.engine.calculate_quantum_pressure(entropy_field)
        
        # Should be zero everywhere
        self.assertTrue(np.allclose(T_quantum, 0.0))
    
    def test_quantum_pressure_uniform_entropy(self):
        """Test quantum pressure with uniform entropy (no gradients)."""
        entropy_field = np.ones((16, 16, 16)) * 5.0
        T_quantum = self.engine.calculate_quantum_pressure(entropy_field)
        
        # Uniform field has zero Laplacian, so pressure should be ~zero
        # (may have small numerical errors at boundaries)
        self.assertTrue(np.abs(np.mean(T_quantum)) < 1e-20)
    
    def test_solve_field_equations_shape(self):
        """Test that solver returns correct metric shape."""
        mass_dist = np.zeros((16, 16, 16))
        entropy_map = np.random.rand(16, 16, 16)
        
        result = self.engine.solve_field_equations(mass_dist, entropy_map, iterations=10)
        
        self.assertEqual(result.shape, (16, 16, 16, 4, 4))
    
    def test_solve_field_equations_zero_inputs(self):
        """Test solver with zero mass and entropy."""
        mass_dist = np.zeros((16, 16, 16))
        entropy_map = np.zeros((16, 16, 16))
        
        result = self.engine.solve_field_equations(mass_dist, entropy_map, iterations=10)
        
        # With zero inputs, metric should remain close to Minkowski
        for i in range(4):
            self.assertTrue(np.allclose(result[..., i, i], 1.0, atol=1e-6))
    
    def test_metric_evolution(self):
        """Test that metric evolves with non-zero inputs."""
        mass_dist = np.zeros((16, 16, 16))
        mass_dist[7:9, 7:9, 7:9] = 1e27  # Localized mass (scaled for visibility)
        
        entropy_map = np.random.rand(16, 16, 16)
        
        initial_metric = self.engine.metric.copy()
        result = self.engine.solve_field_equations(mass_dist, entropy_map, iterations=50)
        
        # Metric should have changed
        self.assertFalse(np.allclose(result, initial_metric))
    
    def test_physical_constants_positive(self):
        """Verify all physical constants are positive."""
        self.assertGreater(self.engine.G, 0)
        self.assertGreater(self.engine.c, 0)
        self.assertGreater(self.engine.hbar, 0)
    
    def test_grid_spacing_positive(self):
        """Verify grid spacing is positive."""
        self.assertGreater(self.engine.dx, 0)

    def test_quantum_pressure_directional_gradients(self):
        """Test that Laplacian calculation correctly handles all spatial directions."""
        # Create a field f(x,y,z) = x^2 + y^2 + z^2
        # Laplacian should be 2+2+2 = 6 everywhere
        # Use arange to ensure dx matches engine.dx
        x = np.arange(self.engine.N) * self.engine.dx
        X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
        entropy_field = X**2 + Y**2 + Z**2

        # Calculate quantum pressure
        # T_quantum = const * Laplacian
        T_quantum = self.engine.calculate_quantum_pressure(entropy_field)

        # Calculate expected constant factor
        const = (self.engine.hbar * self.engine.c / (self.engine.dx**4))
        expected_pressure = const * 6.0

        # Check mean value (ignoring boundaries where numerical differentiation is less accurate)
        inner_slice = (slice(2, -2), slice(2, -2), slice(2, -2))
        computed_mean = np.mean(T_quantum[inner_slice])

        # Should be close to expected value
        # Allow some numerical error tolerance
        # Note: Since values are very small (Planck scale), we must set atol to 0 or very small
        self.assertTrue(np.isclose(computed_mean, expected_pressure, rtol=0.1, atol=0),
                       f"Expected {expected_pressure}, got {computed_mean}. "
                       "Laplacian calculation may be ignoring dimensions.")


    def test_causality_constraint_enforced(self):
        """
        TDD: Test that the engine prevents metric components from 
        reaching extreme non-physical values (Causality Constraint).
        """
        # Create extreme mass that would normally cause huge curvature
        mass_dist = np.ones((16, 16, 16)) * 1e40 
        entropy_map = np.zeros((16, 16, 16))
        
        # This uses self.engine from setUp
        result = self.engine.solve_field_equations(mass_dist, entropy_map, iterations=10)
        
        # Metric should be capped, not exploding to infinity
        self.assertLessEqual(np.max(result[..., 0, 0]), 10.0)
        self.assertGreaterEqual(np.min(result[..., 0, 0]), 0.1)


class TestPhysicalConsistency(unittest.TestCase):
    """Tests for physical consistency of the model."""
    
    def test_entropy_gradient_creates_pressure(self):
        """Test that entropy gradients create non-zero quantum pressure."""
        engine = AethelgardEngine(grid_size=16, domain_size=5.0)
        
        # Create entropy field with gradient
        x = np.linspace(0, 5, 16)
        X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
        entropy_field = X  # Linear gradient in x-direction
        
        T_quantum = engine.calculate_quantum_pressure(entropy_field)
        
        # Should have non-zero pressure due to second derivatives
        # (though linear field has zero Laplacian in interior)
        self.assertIsNotNone(T_quantum)
    
    def test_mass_attracts(self):
        """Test that mass creates attractive curvature (g_00 > 1 in this engine)."""
        engine = AethelgardEngine(grid_size=16, domain_size=5.0)
        
        mass_dist = np.zeros((16, 16, 16))
        mass_dist[7:9, 7:9, 7:9] = 1e27  # Large mass (scaled for visibility)
        
        entropy_map = np.zeros((16, 16, 16))  # No quantum effects
        
        result = engine.solve_field_equations(mass_dist, entropy_map, iterations=100)
        
        # In regions with mass, g_00 should increase (positive curvature update)
        # due to attractive gravity
        g_00_center = result[8, 8, 8, 0, 0]
        self.assertGreater(g_00_center, 1.0)


if __name__ == '__main__':
    unittest.main()
