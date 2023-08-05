# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_reasoner',
 'fuzzy_reasoner.prover',
 'fuzzy_reasoner.prover.operations',
 'fuzzy_reasoner.types']

package_data = \
{'': ['*']}

install_requires = \
['immutables>=0.17,<0.18', 'numpy>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'fuzzy-reasoner',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'David Chanin',
    'author_email': 'chanindav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
