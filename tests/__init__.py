# tests/__init__.py
import os
import sys

# Add the project root to the Python path
# This allows importing modules from the main application
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)