"""
Runner wrapper for tests/test_api_endpoints.py from workspace root.
"""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, '.BackEnd')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from tests.test_api_endpoints import *

if __name__ == '__main__':
    import unittest
    unittest.main()
