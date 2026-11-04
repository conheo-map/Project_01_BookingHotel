"""
E2E Test Runner in .BackEnd/tests
"""
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
WORKSPACE_ROOT = os.path.dirname(ROOT_DIR)
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from tests.test_e2e_full_lifecycle import *

if __name__ == '__main__':
    import unittest
    unittest.main()
