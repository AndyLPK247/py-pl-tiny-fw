"""
This module contains custom assertion functions.
Assertions functions should be called ONLY from test functions for loose coupling.
Otherwise, be prepared for peculiar failures/aborts during tests
"""


# --------------------------------------------------
# Custom Assertion Functions
# --------------------------------------------------

def verify_config_data(data):
    """
    Verifies that the config data contains required values.
    This should be updated as the framework grows.
    :param data: dict
    :return: None
    """

    verify_exact_keys(data, ['base_url'])


def verify_exact_keys(dictionary, key_set):
    """
    Verifies that the dictionary has the exact key set.
    :param dictionary: dict
    :param key_set: collection of keys
    :return: None
    """

    assert isinstance(dictionary, dict)
    assert len(dictionary) == len(key_set)
    for k in key_set:
        assert k in dictionary


def verify_product_format(product):
    """
    Verifies that the product has the expected fields.
    If successful, product may be used safely.
    :param product: dict
    :return: None
    """

    verify_exact_keys(product, ['Description', 'Id', 'Name'])
    assert isinstance(product['Description'], str)
    assert isinstance(product['Id'], int)
    assert isinstance(product['Name'], str)


def verify_response_basics(response, status_code=200, encoding='utf-8'):
    """
    Verifies that the response was basically as expected.
    This should not be the only assertion performed.
    Other checks may be added in the future if they are shared by all calls.
    :param response: from requests
    :param status_code: expected status code (default: 200)
    :param encoding: expected encoding (default: utf-8)
    :return: None
    """

    assert response.status_code == status_code
    assert response.encoding == encoding
