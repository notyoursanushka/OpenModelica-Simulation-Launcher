"""conftest.py — makes the root package visible to pytest."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))