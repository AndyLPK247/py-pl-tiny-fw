Developers' Guide
=================

This file contains a brief guide to the `py-pl-tiny-fw` project
for developers who want to add more tests and expand the framework.


Overview
--------

`py-pl-tiny-fw` is a test automation project for integration-level service tests.
It is written in Python using the [pytest](https://docs.pytest.org/en/latest/) framework.
The main repository is located on GitHub at https://github.com/AndyLPK247/py-pl-tiny-fw.
Make sure any code changes undergo code review and meet the testing needs!


Setup
-----

The machine running these tests must have [Python 3](https://automationpanda.com/2017/02/07/which-version-of-python-should-i-use/) installed.
Also, run `pip install pytest` and `pip install requests` to install required packages.
If you are new to Python, read [the Wikibook on Python Programming](https://en.wikibooks.org/wiki/Python_Programming).
Also read the [pytest docs](https://docs.pytest.org/en/latest/).
It is also recommended to set up a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for writing and running tests.

To develop new tests, the dev machine will need [git](https://git-scm.com/) to clone the repository.
It is also strongly recommended to use an IDE or editor like PyCharm, Visual Studio Code, etc.


Running Tests
-------------

To run all tests, run `python -m pytest` from the root directory.
Run `pytest -h` to see more options.


The Tests
---------

All tests should be written in Python module under the `tests` directory.
(Note that this is a directory and not a Python package; hence, no `__init__.py` file.)
Pytest will "discover" any functions named "test_*" as test cases.
Each Python module should contain tests for one API set.
For example, `tests/test_api_product.py` contains tests for the `/api/product` resource paths.

A single test should focus on one main thing.
For service call testing, this means one main call: request spec, method call, and response validation.
Name each test after its target resource and any unique equivalence class of inputs.
Be complete in coverage, but don't add unnecessary input combos.
Make sure to add comments to tests to explain *what* and *why*.


The Service Calls
-----------------

Service calls are made using the [requests](http://docs.python-requests.org/en/master/) package.
Extra shared code to support service calls is in the `services` package.
Right now, the package contains only a module for resource path functions.
Add new functions for new resource paths - this module should be the single source of truth!

Right now, the service calls are very simple and can justifiably make direct calls using `requests`.
However, as new features are added, service calls may become more complicated.
Then, it would be necessary to implement a more robust Service Object Model pattern.


The Framework Package
---------------------

The `fw` package contains modules for test automation support.
It should contain reusable code for any test to potentially use.


Assertions
----------

Python has a basic `assert` statement that will yield an exception if its condition is false.
A custom message may also be added to it, but
pytest uses [advanced assertion introspection](https://docs.pytest.org/en/latest/assert.html)
so that most assertions will be automatically logged with actual values.
(This eliminates the need for most logging, though Python's standard [logging](https://docs.python.org/3/library/logging.html) could be added in the future.)

The `fw/assertions.py` module contains custom assertion functions to simplify and reuse common checks.
Add custom assertions here as necessary.

**Warning:** Make assertion calls ONLY from test case functions!
Do NOT make them from anywhere else in the code!
We want loose coupling and no dirty surprises from tests aborting at arbitrary points.


Config Data
-----------

[Config data](https://automationpanda.com/2017/08/05/handling-test-data-in-bdd/)
is configuration information that tells test automation how to run.
For example, the base URL for the endpoints under test is config data.
Never hard-code config data in the automation code!
Always pass it in as inputs or read it in from files.

The `fw/config.py` module contains logic to read and parse files.
Right now, all config data is read from a file named `config.json` in the root directory.
The reading (and validation with a custom assertion method) happens once before all tests in the session
in the `config_data` [fixture](https://docs.pytest.org/en/latest/fixture.html)
in the `tests/conftest.py` file.
Any pytest test function that declares the fixture by name in its arguments list will receive the parsed config data.
Config data can and should be expanded/refactored in the future to meet the needs as they come.


Future Enhancements
-------------------

This project is very small: its tests are still few, and its framework is minimal.
It is not presently set up to handle Web UI tests, though it could.
Request specification modules should be added to the `services` package if request specs become more complicated.
Logging could be added, but pytest + assertion introspection should be sufficient.
