# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_ninja']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2', 'docstring-parser>=0.14.1,<0.15.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'flask-ninja',
    'version': '1.0.0',
    'description': 'Flask Ninja is a web framework for building APIs with Flask and Python 3.9+ type hints.',
    'long_description': '# Flask Ninja\n\n**Flask Ninja** is a web framework for building APIs with Flask and Python 3.9+ type hints.',
    'author': 'Michal Korbela',
    'author_email': 'michal.korbela@kiwi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
