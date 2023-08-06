# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_to_pypika']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.48.9,<0.49.0', 'sly>=0.4,<0.5']

setup_kwargs = {
    'name': 'sql-to-pypika',
    'version': '0.1.2',
    'description': 'Convert raw SQL to Pypika Objects',
    'long_description': '# sql_to_pypika\n\n[![Tests Status](https://github.com/pahwaranger/sql_to_pypika/workflows/Tests/badge.svg?branch=master&event=push)](https://github.com/pahwaranger/sql_to_pypika/actions/workflows/test.yml?query=event%3Apush+branch%3Amaster) [![codecov](https://codecov.io/gh/pahwaranger/sql_to_pypika/branch/master/graph/badge.svg?token=7T2VXRNGON)](https://codecov.io/gh/pahwaranger/sql_to_pypika) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nHelper util for converting raq SQL expressions to PyPika objects. This is neither comprehensive nor perfect. My hope with creating a repo for this is that if people are interested then we can expand on this from here.\n\n## Usage\n\n```py\ntables = [("foo", "foo"), ("bar", "b")]\nevaluator = ExpressionEvaluator(tables)\nresult = evaluator.eval("foo.fizz = 1")\n\nprint(result)  # "foo"."fizz"=1\'\ntype(result)   # pypika.terms.BasicCriterion\n\nresult = evaluator.eval("bar.fizz = 1")\nprint(result)  # "b"."fizz"=1\'\ntype(result)   # pypika.terms.BasicCriterion\n```\n\n## Disclaimer\n\nThe logic was initially created by @twheys, the creator of PyPika ([gist](https://gist.github.com/twheys/5635a932ca6cfce0d114a86fb55f6c80)) via [this conversation](https://github.com/kayak/pypika/issues/325).\n\nI went ahead and cleaned it up and added some tests so I could use it for my own needs.\n\n## Dev / CI\n\nThis repo utilize Poetry, for package management. I recommend reading the Poetry install instructions [here](https://python-poetry.org/docs/#installation).\n\nYou can then simply run:\n\n```sh\npoetry install\n```\n\nWe use `pytest` and `Black` for testing and linting respectively. You can use the scripts in the scripts folder to run them.\n',
    'author': 'Amit Pahwa',
    'author_email': 'amit@amitpahwa.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pahwaranger/sql_to_pypika',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
