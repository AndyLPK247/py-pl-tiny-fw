"""
This module reads config data for test automation.
Config data should NEVER be hard-coded into test code.
It should always be read from somewhere else.
That way, tests can be set to run in any environment.
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import json


# --------------------------------------------------
# "Constants"
# --------------------------------------------------

DEFAULT_CONFIG_JSON_PATH = 'config.json'


# --------------------------------------------------
# Functions to Read Config Data
# --------------------------------------------------

def read_json_config(path='config.json'):
    with open(path) as config_file:
        return json.load(config_file)
