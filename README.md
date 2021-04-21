py-pl-tiny-fw
=============

I developed this project for my interview at PrecisionLender in March 2018.
It is a small example test framework written in Python.
It tests a very simple REST API for two GET methods.
Although its scope is small, it is designed to be expandable.


APIs Under Test
---------------

http://pltestautomationsample.azurewebsites.net/api/product

The main endpoint returns a list of products.
Adding /\<id\> to the end will return a specific product.
Only GET methods are available.


Running Tests
-------------

Tests require Python 3, `pytest`, and `requests`.
Run `python -m pytest` from the root directory to discover and run all tests.


Directory Layout
----------------

* `fw` contains automation framework support code (like custom assertions)
* `services` contains service call support code
* `tests` contains the test cases and fixtures


Further Documentation
---------------------

* `README_dev.md` is for developers who will add tests to this suite as new features are added.
* `README_design.md` contains an overview of the framework (including approach, design, packages, and tools).
