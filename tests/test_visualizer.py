import unittest

import numpy as np

from interactive_visualizer import InteractiveVisualizer


class TestInteractiveVisualizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We don't want to start the actual Dash server in tests
        # but we want to test the data generation logic
        cls.viz = InteractiveVisualizer(grid_size=16, domain_size=5.0)

    def test_initialization(self):
        self.assertEqual(self.viz.grid_size, 16)
        self.assertIsNotNone(self.viz.app)

    def test_blackhole_scenario_generation(self):
        """Test that black hole scenario generates valid data."""
        self.viz._create_blackhole_scenario()
        self.assertIsNotNone(self.viz.metric)
        self.assertEqual(self.viz.metric.shape, (16, 16, 16, 4, 4))
        # g00 should be >= 1.0 (clamped) due to mass
        self.assertGreaterEqual(np.mean(self.viz.metric[..., 0, 0]), 1.0)

    def test_supernova_scenario_generation(self):
        """
        TDD GREEN: Verify that supernova scenario generates valid data.
        """
        self.viz._create_supernova_scenario()
        self.assertIsNotNone(self.viz.metric)
        self.assertGreaterEqual(np.mean(self.viz.metric[..., 0, 0]), 1.0)
