import sys
import unittest

# Load and run tests
loader = unittest.TestLoader()
suite = loader.loadTestsFromName('test_aethelgard')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Exit with appropriate code
sys.exit(0 if result.wasSuccessful() else 1)
