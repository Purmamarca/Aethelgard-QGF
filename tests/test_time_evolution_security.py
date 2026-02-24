"""
Security regression tests for AethelgardEngineTimeEvolution.
Focuses on input validation and resource exhaustion prevention.
"""

import unittest
import numpy as np
from aethelgard_time_evolution import AethelgardEngineTimeEvolution


class TestTimeEvolutionSecurity(unittest.TestCase):

    def test_init_validation(self):
        """Test validation in AethelgardEngineTimeEvolution.__init__."""
        # Valid cases should not raise
        try:
            AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=0.01)
            AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=1.0)
            AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=0.0001)
        except ValueError:
            self.fail("AethelgardEngineTimeEvolution raised ValueError unexpectedly on valid inputs")

        # Invalid dt
        with self.assertRaises(ValueError):
            AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=0.0)
        with self.assertRaises(ValueError):
            AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=-0.01)
        with self.assertRaises(ValueError):
            AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt="invalid")

    def test_evolve_validation(self):
        """Test validation in AethelgardEngineTimeEvolution.evolve_metric."""
        engine = AethelgardEngineTimeEvolution(grid_size=16, domain_size=5.0, dt=0.01)

        # Create valid inputs
        valid_mass = np.zeros((16, 16, 16))
        valid_entropy = np.zeros((16, 16, 16))

        # Valid call
        try:
            engine.evolve_metric(valid_mass, valid_entropy, time_steps=10)
        except ValueError:
            self.fail("evolve_metric raised ValueError unexpectedly")

        # Invalid time_steps
        with self.assertRaises(ValueError):
            engine.evolve_metric(valid_mass, valid_entropy, time_steps=0)
        with self.assertRaises(ValueError):
            engine.evolve_metric(valid_mass, valid_entropy, time_steps=-5)
        with self.assertRaises(ValueError):
            engine.evolve_metric(valid_mass, valid_entropy, time_steps=10001) # Too many
        with self.assertRaises(ValueError):
            engine.evolve_metric(valid_mass, valid_entropy, time_steps=10.5) # Not integer
