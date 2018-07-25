"""Configuration file for driver program."""

import os

# Global variables - adjust as necessary
INPUT_DIR = os.path.join(".", "input")
OUTPUT_DIR = os.path.join(".", "output")
DATABASE_DIR = os.path.join(".", "database")

# Global variables - don't change unless you know what you're doing
DATABASE = {} # Dictionary {"Criteria": "Cell Code"}