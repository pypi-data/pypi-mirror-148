# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asserto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asserto',
    'version': '0.0.3a0',
    'description': 'A fluent DSL for python assertions.',
    'long_description': '![Asserto](.github/images/logo.png)\n\n![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)\n[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)\n[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/asserto/)\n\n## Asserto\n\nAsserto is a clean, fluent and powerful assertion library for python.  We recommend using `pytest` as a test\nrunner (as asserto has been developed using it internally) however any test runner will work just fine.  Using it\nin your framework (non-test) code is also fine as well!\n\nThe main features of asserto are (and will be):\n\n- Chaining and assertion fluency using a builder-esque API.\n- Hard assertions by default; but soft when used in a python context.\n- Clean, rich diffs to highlight problems and improve debuggability.\n- Dynamicism, access underlying attributes and methods on pretty much any object using `attr_is(expected)` syntax.\n- A robust set of APIs including all builtin types; files; regex and much, much more.\n- Extensibility; registering your own assertion functions is easy! consider sending us a patch for useful ones.\n- Automatic warnings in some cases of human error for assertions; i.e creating an instance but never checking anything.\n- Much much more.\n\n```python\nfrom asserto import asserto\n\ndef test_foo() -> None:\n    asserto("Hello").has_length(5).matches(r"\\w{5}$").ends_with("lo").starts_with("Hel")\n```\n\nIf you use pytest; a fixture is available for an `Asserto` factory function:\n\n```python\ndef test_bar(asserto) -> None:  # No imports; just use the fixture.\n    asserto("Hello").has_length(5).matches(r"\\w{4}$").ends_with("lo").starts_with("Hel")\n```\n\nIf you want to check many assertions in a single test without failing until after all:\n\n```python\ndef test_baz(asserto) -> None:\n    with asserto("Baz") as context:\n        # asserto when used in a python context is run in \'soft\' mode;\n        # upon exiting the context; congregated errors are subsequently raised (if any)\n        context.starts_with("B")\n        context.ends_with("z")\n        context.is_equal_to("Baz")\n        context.is_length(2)  # Uh oh a failure!\n```\n\nResults in:\n\n```shell\n    def test_foo(asserto) -> None:\n>       with asserto("Bar") as context:\nE       AssertionError: 1 Soft Assertion Failures\nE       [AssertionError("Length of: \'Bar\' was not equal to: 2")]\n```\n',
    'author': 'symonk',
    'author_email': 'jackofspaces@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
