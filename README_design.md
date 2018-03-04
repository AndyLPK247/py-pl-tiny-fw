Andy's Approach
===============

This file explains the approach I took to developing this framework.
It also includes an overview of tools used and an explanation of the test design.
I strongly recommend reading `README.md` and `README_dev.md` before reading this "behind-the-scenes" guide.


Why Python?
-----------

Personally, I love Python. I also strongly believe that Python is
[one of the best languages for test automation](https://automationpanda.com/2017/01/21/the-best-programming-language-for-test-automation/).

* It is easy to learn.
* It is concise.
* It is functional and object-oriented.
* It has many great testing frameworks and packages.
* It's command-line-friendly.
* It's scalable.

My second choice was Java, and my third choice was C#.


Why pytest?
-----------

Pytest is the framework that provides the basic structure for tests.
It is so simple yet so feature-rich!
* The framework is minimalist and doesn't get in the way.
* Each test is an independent function, which limits side effects.
* The command line is powerful for test discovery and filtering.
* Setup and cleanup are handled by very nimble fixtures.
* It can easily be extended with plugins for code coverage, BDD, etc.
* Reporting is pretty easy.
* Assertion introspection removes much of the need for deliberate logging (for small tests).
* It is one of the most popular Python test frameworks and will be well supported for a long time.


Automation Development
----------------------

I developed this project on a Mac.
I used JetBrains PyCharm as my IDE.
I also created a Python virtual environment to keep my packages local.

I put the repository in my public GitHub account to make it easy to share
and also because version control is like driving with a seat belt.
I made a series of small commits for good history.

I put a good bit of documentation in the project, too, mostly to explain what and why.
At the top level, I chose READMEs in Markdown so that they can be diff-ed line-by-line by Git
but still have some formatting.
I always comment my Python files with headers and docstrings.

The code took me about 3 hours total to design, implement, and test.
The documentation took me about 2 additional hours.
I could have done it quicker if I skipped the config data support.


Framework Layers
----------------

This framework has four basic layers:

1. Config Data
2. Test Cases
3. Service API Call Support
4. Framework Support

The layers provide abstraction and loose coupling.
Duplicate code is one of [the biggest challenges with test automation](https://automationpanda.com/2017/01/24/why-is-automation-full-of-duplicate-code/).
Ideally, each separate layer could be packaged and shared separately.
This would allow teams to share framework parts without the bloat of unrelated tests.

Since the product under test was a service API, I did not add Web UI support.
This could be added as its own layer (at the same level as Service API Call Support).


Assertions
----------

Assertions are core to any test framework.
There are many good assertion packages available.
However, pytest works best with the standard `assert` statement in Python's language.
This may seem peculiar - why not try a more "advanced" package?
The reason is that pytest is *designed* to use the basic `assert` statement.
Upon a failure, pytest will automatically introspect assert statements and log actual values.
This eliminates the need to provide custom failure messages (for the vast majority of assertions).
Plus, sometimes, the simple things are the best things:
rather than teach a bunch of engineers a new library,
make their work simple and handle things automatically for them.


Config Data
-----------

Config data is the data used to configure test automation.
It contains things like URLs, usernames, passwords, etc.
Config data should never be hard-coded into automation code.
Instead, it should be passed in as inputs or read from files.
Most contemporary frameworks don't support a mechanism for direct command-line inputs of arbitrary data.
Thus, file reading is the norm.
Given that this project is inherently limited in scope,
I chose to simply store the only piece of config data (the endpoint base URL)
in a JSON file in the root directory.
I also wrote a framework module (`fw/config.py`) to read in the file.
Config data files, formats, and read/write support would naturally be enhanced in the future,
but I took a Lean approach for now to keep it simple.


Service Calls
-------------

I used Python's [requests](http://docs.python-requests.org/en/master/) package for making service calls.
It's so concise and simple - even beginners can quickly master it.
The calls under test are so simple that they could be adequately tested by direct calls to `requests`.
In the future, as calls become more complicated, a Service Object Model should be considered (for reusable code).


Test Cases
----------

Despite the simplicity of the APIs, the test case design required some interesting decisions and trade-offs.
There were two main GET-method APIs to test: one to get a list of products, and one to get an individual product.
Since they were together in what I consider to be the same "API set", I put them all in one carefully-named Python module.

All tests follow the same format:

1. Build the request spec
2. Call the API
3. Validate the response

This is the "behavior" of an API call.
Service API tests at the integration level should do little more than this.
Some tests may need additional calls for setup and cleanup,
but those should not be the main behavior for the test case's focus.
Thus, each test should be unique for an endpoint and its equivalence class of inputs.
Each test also reuses common framework parts.
I included a negative test for a bad ID to make sure it gets a reasonable error message,
but I chose not to include a negative test for resource path misspelling because, to me, that would add little value.

The first challenge was considering how to handle the test data.
The trouble here was mostly due to inherent assignment limitations.
The service was pre-populated with dummy data, whereas a "real" service would have real data.
It is a testing best practice that setup/cleanup routines would set up and tear down test data in the service for the test.
For a CRUD-like service, this would most likely mean C for setup and D for cleanup.
That way, the test case is in control of the data, and assertions can be made for explicit values.
Hence, my stumbling block: Do I treat the dummy data in the system as if it is the test data?
Or, should I presume that, even under "real" circumstances, the data would be out of my control?
So, given limited information, I did both for the sake of example.
In `test_api_product_id`, I presumed that the values should be taken as test values, and I validated them explicitly.
In `test_api_product`, I presumed that values would be out of my control,
and I validated the parent-child structure, the formats of values (string or int), and the uniqueness of IDs.
Not checking explicit values in this case makes the test less fragile.

The second challenge was deciding what to do with the trailing slash ("/").
It may seem trivial, but it's one of those things that should be checked.
Some APIs are written to require it, while others support calls either way.
Many times, it's just added by the underlying API framework in the product code.
The expectation for the slash is something I'd ask a developer about.
Presuming that the endpoints are the same with or without it,
I parametrized tests to cover both ways.
At the very least, some tests (if not all) should make sure the slash doesn't matter.
Both endpoint versions would be "publicly" available, and thus systems could call either one.
That warrants at least a basic check.
Now, running every single test both ways would double the total test execution time,
which may become too much in the future.
Two ways to address that problem would be
(1) pick-and-choose only a few endpoints to check, or
(2) add a boolean option to the config data to run all tests with or without the slash.
(I strongly oppose making the slash's appearance random-50/50 because functional tests should be deterministic.)

The third challenge was the Accept format: JSON or XML?
JSON is much easier to handle in Python, but XML is nevertheless available.
This is very similar to the trailing slash problem.
However, whereas the slash is easy to parametrize, the accept format is not.
The Python logic required to parse the two formats are much different.
I chose to make all "standard" tests use JSON,
and then I wrote a one-off `test_xml_response` test that tests one API with XML.
With a Testing Pyramid perspective,
the response format is something that would be best to handle at the unit level.
The service itself is simply writing the same data in two different ways,
and the data itself should be the same.
I would also seek to verify that JSON/XML output is handled by an internal framework or methods that should be unit-tested.
Thus, rather than bloat testing at the service layer,
it would be better to do only a few spot checks for alternative accept formats.
To me, this is less of a risk than the trailing slash
because accept formats use the same endpoint URL while trailing slashes technically use different URLs.
Furthermore, the trailing slash can only be genuinely tested as an integration point and not at the unit level.
A boolean config data option to select accept format type for all tests could also be added,
but that would require additional service package logic to parse formats generically,
and I consider that beyond the scope of this project.

For both the trailing slash or the accept format,
I would want to talk with developers to make the best decision.
I would also be agreeable to change the design decisions I explained above with more information or reasonable persuasion.
