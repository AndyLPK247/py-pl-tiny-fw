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

from fw import assertions


# --------------------------------------------------
# "Constants"
# --------------------------------------------------

BASE_URL = "http://pltestautomationsample.azurewebsites.net"


# --------------------------------------------------
# Tests for /api/product
# --------------------------------------------------

# @pytest.mark.parametrize("url_ending", ['', '/'])
# def test_api_product(url_ending):
#     response = requests.get(BASE_URL + '/api/product' + url_ending)
#     assertions.verify_response_basics(response)


# --------------------------------------------------
# Tests for /api/product/<id>
# --------------------------------------------------

@pytest.mark.parametrize("url_ending", ['', '/'])
def test_api_product_id_exists(url_ending):
    response = requests.get(BASE_URL + '/api/product/1' + url_ending)
    assertions.verify_response_basics(response)

    content = response.json()
    assertions.verify_product_format(content)
    assert content['Description'] == 'A blue car'
    assert content['Id'] == 1
    assert content['Name'] == 'Blue Car'


def test_api_product_id_dne():
    response = requests.get(BASE_URL + '/api/product/99999')
    assertions.verify_response_basics(response, status_code=500)

    content = response.json()
    assertions.verify_exact_keys(content, ['Message'])
    assert content['Message'] == 'An error has occurred.'
