# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docstring_parser', 'docstring_parser.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'docstring-parser',
    'version': '0.14',
    'description': 'Parse Python docstrings in reST, Google and Numpydoc format',
    'long_description': "docstring_parser\n================\n\n[![Build](https://github.com/rr-/docstring_parser/actions/workflows/build.yml/badge.svg)](https://github.com/rr-/docstring_parser/actions/workflows/build.yml)\n\nParse Python docstrings. Currently support ReST, Google, Numpydoc-style and\nEpydoc docstrings.\n\nExample usage:\n\n```python\n>>> from docstring_parser import parse\n>>>\n>>>\n>>> docstring = parse(\n...     '''\n...     Short description\n...\n...     Long description spanning multiple lines\n...     - First line\n...     - Second line\n...     - Third line\n...\n...     :param name: description 1\n...     :param int priority: description 2\n...     :param str sender: description 3\n...     :raises ValueError: if name is invalid\n...     ''')\n>>>\n>>> docstring.long_description\n'Long description spanning multiple lines\\n- First line\\n- Second line\\n- Third line'\n>>> docstring.params[1].arg_name\n'priority'\n>>> docstring.raises[0].type_name\n'ValueError'\n```\n\nRead [API Documentation](https://rr-.github.io/docstring_parser/).\n\n# Contributing\n\nTo set up the project:\n```sh\npip install --user poetry\n\ngit clone https://github.com/rr-/pycrcmanip.git\ncd pycrcmanip\n\npoetry install\npoetry run pre-commit install\n```\n\nTo run tests:\n```\npoetry run pytest\n```\n",
    'author': 'Marcin Kurczewski',
    'author_email': 'dash@wind.garden',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rr-/docstring_parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
