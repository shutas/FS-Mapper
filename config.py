"""Configuration file for driver program."""

import os

# Global variables - adjust as necessary
INPUT_DIR_LAYERS = [".", "input"]
OUTPUT_DIR_LAYERS = [".", "output"]
DATABASE_DIR_LAYERS = [".", "database"]

# Global variables - don't change unless you know what you're doing
INPUT_DIR = os.path.join(*INPUT_DIR_LAYERS)
OUTPUT_DIR = os.path.join(*OUTPUT_DIR_LAYERS)
DATABASE_DIR = os.path.join(*DATABASE_DIR_LAYERS)

DATABASE = [] # List of ("regex pattern", "cell code")
BLACKLIST = set() # Set of "regex pattern"