"""
This module contains resource paths for services.
For consistency, all paths are accessed as functions.
That way, parametrized paths are easier to concat.
"""


# --------------------------------------------------
# Product Resource Paths
# --------------------------------------------------

def api_product():
    return '/api/product'


def api_product_id(i):
    return '/api/product/%s' % i
