import os
import sys

# Make the project root importable so tests can do `from src... import ...`
# and `from project import ...` regardless of where pytest is invoked.
sys.path.insert(0, os.path.dirname(__file__))
