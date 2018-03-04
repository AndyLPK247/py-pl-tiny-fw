py-pl-tiny-fw
=============

This is a small test framework written in Python.
Those who know will know what it's about.


APIs Under Test
---------------
http://pltestautomationsample.azurewebsites.net/api/product

The main endpoint returns a list of products.
Adding /\<id\> to the end will return a specific product.
Only GET methods are available.


Running Tests
-------------

To run these tests, make sure Python 3 is installed.
Also, run `pip install pytest` and `pip install requests`.
It is recommended (but not necessary) to run tests in a virtual Python environment.
Then, run `python -m pytest` to discover and run all tests.


Considerations
--------------
* No 'service objects' - too small to be worthwhile, but service package.
* Slash or no slash? Doubles the runtime, but may be necessary to check
  a few at least.
* It would be best to have setup and cleanup populate dummy data.
* I don't feel comfortable explicitly verifying each field of each
  product in the list result. That would be fragile. In this case, it
  would be better to verify keys and formats. If I could setup my own
  data, then I would do explicit validations.
* Explain pytest's assertion introspection -> no need for logging yet.
* Separate packages for tests and framework.
* A service test should contain request spec, method call, and response
  validation all in one, because that is the fullness of the behavior.


TODO
----
* Write the two docs.