"""
This module is the standard pytest module for shared fixtures.
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pytest

from fw import assertions, config


# --------------------------------------------------
# Session-Scoped Fixtures
#
# These will run once before all tests.
# --------------------------------------------------

@pytest.fixture(scope="session")
def config_data():
    data = config.read_json_config()
    assertions.verify_config_data(data)
    return data
