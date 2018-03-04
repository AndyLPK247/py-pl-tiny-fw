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
# --------------------------------------------------

CONFIG = config.read_json_config()
BASE_URL = CONFIG['base_url']


# --------------------------------------------------
# Tests for /api/product
# --------------------------------------------------

@pytest.mark.parametrize("url_ending", ['', '/'])
def test_api_product(url_ending):
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
    resource = resources.api_product_id(1)
    response = requests.get(BASE_URL + resource + url_ending)
    assertions.verify_response_basics(response)

    product = response.json()
    assertions.verify_product_format(product)
    assert product['Description'] == 'A blue car'
    assert product['Id'] == 1
    assert product['Name'] == 'Blue Car'


def test_api_product_id_dne():
    resource = resources.api_product_id(99999)
    response = requests.get(BASE_URL + resource)
    assertions.verify_response_basics(response, status_code=500)

    content = response.json()
    assertions.verify_exact_keys(content, ['Message'])
    assert content['Message'] == 'An error has occurred.'
