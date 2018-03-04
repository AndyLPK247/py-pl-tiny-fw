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
# Tests for /api/product
# --------------------------------------------------

def test_api_product():
    pass


# --------------------------------------------------
# Tests for /api/product/<id>
# --------------------------------------------------

def test_api_product_id_exists():
    pass


def test_api_product_id_dne():
    pass

