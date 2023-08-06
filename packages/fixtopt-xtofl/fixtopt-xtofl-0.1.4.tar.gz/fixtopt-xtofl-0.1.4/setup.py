# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fixtopt']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.4,<8']

setup_kwargs = {
    'name': 'fixtopt-xtofl',
    'version': '0.1.4',
    'description': 'Pytest extension for adding test options',
    'long_description': '# fixtopt\n\nExtend your pytests with options that can be accessed as test fixtures.\n\nPytest allows declaring command line options for your tests.  You\nspecify this in a [test hook](https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_addoption)\ndefined in e.g. a file called [`conftest.py`](https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins),\ninside your test directory.\n\nAdd the options:\n\n```python\n# conftest.py\nfrom fixtopt import Option, register\n\ndef pytest_addoption(parser):\n    register(globals(), parser, (\n\n        Option(\n            name="message",\n            default="message.txt",\n            help="the message file"),\n\n        Option(\n            name="receiver",\n            default="World",\n            help="the receiver"),\n\n    ))\n```\n\nImport the options in your tests like you would import a fixture:\n\n```python\nimport my_mailclient\n\ndef test_a_person_receives_a_message(message, receiver):\n    with open(message) as f:\n        assert my_mailclient.receiver(f.read()) == receiver\n```\n\nAnd you can run your tests with the declared options:\n\n```shell\npytest . --message /path/to/messagefile --receiver mrs.X\n```\n\n',
    'author': 'xtofl',
    'author_email': 'xtofl@fixtopt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
