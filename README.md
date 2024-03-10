<img src=".readme/pytest-ai1899-plugin.jpeg" alt="pytest-ai1899-plugin" width="220">

------

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit)

What?
------
To enable seamless integration with ai1899 stack (https://github.com/Formartha/ai1899), a pytest plugin was created.
The plugin accepts query as an input or from pytest.ini directory and uses it to select testcases based on predefined citeria.

How to install?
----------
```
pip install pytest-ai1899
```

pytest.ini options examples:
-----------------------------------------------------

```
[pytest]
ai1899_endpoint = http://127.0.0.1/ai
ai1899_query = a test with data
ai1899_collection = Tests
ai1899_limit = 5
```