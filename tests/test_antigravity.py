import unittest

from antigravity_engine import simulate_antigravity_flux


class TestAntigravityEngine(unittest.TestCase):
    def test_simulate_antigravity_flux_output_format(self):
        """Test that the simulation returns the expected string format."""
        result = simulate_antigravity_flux(mass=1e24, radius=100)
        self.assertIn("Flux Density:", result)
        self.assertIn("Predicted Shift:", result)

    def test_calculate_flux_anomaly_exists(self):
        """
        TDD REFACTOR PHASE: Updating test to match new tuple return.
        """
        from antigravity_engine import calculate_flux_anomaly
        shift, density = calculate_flux_anomaly(mass=1e24, radius=100)
        self.assertIsInstance(shift, float)
        self.assertIsInstance(density, float)
        self.assertLess(shift, 0)
