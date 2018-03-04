"""
This module contains Web API tests for the following API:
http://pltestautomationsample.azurewebsites.net/api/product

The source code for this API is located at:
https://github.com/LouisSheridan/SampleWebAPI

Based on the source code, it looks like there are two endpoints:
One for all products, and one for getting an individual product by ID.
It looks like only GET calls are available.

The tests are written using the pytest framework.
For simplicity, the tests are functions and not classes.
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pytest
import requests

from fw import assertions, config
from services import resources


# --------------------------------------------------
# Read Config Data
#
# NEVER HARD-CODE CONFIG DATA!
# ALWAYS READ IT FROM FILES OR INPUTS!
# --------------------------------------------------

CONFIG = config.read_json_config()
BASE_URL = CONFIG['base_url']


# --------------------------------------------------
# Tests for /api/product
# --------------------------------------------------

@pytest.mark.parametrize("url_ending", ['', '/'])
def test_api_product(url_ending):
    """
    This test verifies the list of products returned by the resource path.
    However, it deliberately does NOT validate specific values.
    Given the limited nature of this example, test data cannot be controlled.
    For a real test, it would be best to set up the system with specific test data.
    Since that is not possible, it is better verify data formats than data values.
    That makes the test far less fragile.
    Furthermore, this test makes sure the list is non-empty and that IDs are unique
        (which should be reasonable preconditions for the test's intent).
    """

    resource = resources.api_product()
    response = requests.get(BASE_URL + resource + url_ending)
    assertions.verify_response_basics(response)

    content = response.json()
    ids = []
    assert len(content) > 0
    for product in content:
        assertions.verify_product_format(product)
        assert product['Id'] not in ids
        ids.append(product['Id'])


# --------------------------------------------------
# Tests for /api/product/<id>
# --------------------------------------------------

@pytest.mark.parametrize("url_ending", ['', '/'])
def test_api_product_id_exists(url_ending):
    """
    This test verifies the retrieval of a single product by ID.
    Unlike the list test, this test is written to validate specific values.
    A test like this should be preceded by a setup operation to create the record.
    In that case, it would be appropriate to verify the actual values.
    """

    resource = resources.api_product_id(1)
    response = requests.get(BASE_URL + resource + url_ending)
    assertions.verify_response_basics(response)

    product = response.json()
    assertions.verify_product_format(product)
    assert product['Description'] == 'A blue car'
    assert product['Id'] == 1
    assert product['Name'] == 'Blue Car'


def test_api_product_id_dne():
    """
    This test verifies than an error is given when attempting to retrieve
        a product via an invalid ID.
    """

    resource = resources.api_product_id(99999)
    response = requests.get(BASE_URL + resource)
    assertions.verify_response_basics(response, status_code=500)

    content = response.json()
    assertions.verify_exact_keys(content, ['Message'])
    assert content['Message'] == 'An error has occurred.'
