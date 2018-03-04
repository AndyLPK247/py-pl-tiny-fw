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


# --------------------------------------------------
# "Constants"
# --------------------------------------------------

BASE_URL = "http://pltestautomationsample.azurewebsites.net"


# --------------------------------------------------
# Tests for /api/product
# --------------------------------------------------

def test_api_product():
    pass


# --------------------------------------------------
# Tests for /api/product/<id>
# --------------------------------------------------

@pytest.mark.parametrize("url_ending", ['', '/'])
def test_api_product_id_exists(url_ending):
    response = requests.get(BASE_URL + '/api/product/1' + url_ending)
    assert response.status_code == 200
    assert response.encoding == 'utf-8'

    content = response.json()
    assert len(content) == 3
    assert 'Description' in content
    assert content['Description'] == 'A blue car'
    assert 'Id' in content
    assert content['Id'] == 1
    assert 'Name' in content
    assert content['Name'] == 'Blue Car'


def test_api_product_id_dne():
    response = requests.get(BASE_URL + '/api/product/99999')
    assert response.status_code == 500
    assert response.encoding == 'utf-8'

    content = response.json()
    assert len(content) == 1
    assert 'Message' in content
    assert content['Message'] == 'An error has occurred.'
